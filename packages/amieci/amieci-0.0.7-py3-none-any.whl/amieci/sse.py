import codecs
import json
import logging
import os
import queue
import re
import threading
import time
import warnings

import requests
import six

LOG_LEVEL = os.environ.get("AMIECI_LOGLEVEL", "INFO")
LOG_MSG_FORMAT = "amieci %(levelname)s: %(message)s"
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)

#specs https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation

END = re.compile(r'\r\n\r\n|\r\r|\n\n')
SSEFIELDS = re.compile('(?P<name>[^:]*):?( ?(?P<value>.*))?')


class SSEClient():
    def __init__(self,
                 url,
                 last_id=None,
                 retry=3000,
                 session=None,
                 chunk_size=1024,
                 **kwargs):
        self.url = url
        self.last_id = last_id
        self.retry = retry
        self.chunk_size = chunk_size

        # Optional support for passing in a requests.Session()
        self.session = session

        # Any extra kwargs will be fed into the requests.get call later.
        self.requests_kwargs = kwargs

        # The SSE spec requires making requests with Cache-Control: nocache
        if 'headers' not in self.requests_kwargs:
            self.requests_kwargs['headers'] = {}
        self.requests_kwargs['headers']['Cache-Control'] = 'no-cache'
        self.requests_kwargs['headers']['Accept'] = 'text/event-stream'

        # Keep data here as it streams in
        self.buf = u''

        self._connect()

    def _connect(self):
        if self.last_id:
            self.requests_kwargs['headers']['Last-Event-ID'] = self.last_id

        self.resp = self.session.get(
            self.url, stream=True, **self.requests_kwargs)
        self.resp_iterator = self.resp.iter_content(chunk_size=self.chunk_size)

        self.resp.raise_for_status()

    def _event_complete(self):
        return re.search(END, self.buf) is not None

    def __iter__(self):
        return self

    def __next__(self):
        # guess encoding from response
        decoder = codecs.getincrementaldecoder(
            self.resp.encoding)(errors='replace')
        while not self._event_complete():
            try:
                next_chunk = next(self.resp_iterator)
                if not next_chunk:
                    raise EOFError()
                self.buf += decoder.decode(next_chunk)

            except (StopIteration, requests.RequestException, EOFError,
                    six.moves.http_client.IncompleteRead) as exception:
                print(exception)
                time.sleep(self.retry / 1000.0)
                self._connect()

                # The SSE spec only supports resuming from a whole message, so
                # if we have half a message we should throw it out.
                head, sep, _ = self.buf.rpartition('\n')
                self.buf = head + sep
                continue

        # note: buffer may contain more bytes then on full event, depending on cunk size
        (event_string, self.buf) = re.split(END, self.buf, maxsplit=1)
        event = parse_event(event_string)

        # If the server requests a specific retry delay, we need to honor it.
        if event.retry:
            self.retry = event.retry

        # last_id should only be set if included in the message.  It's not
        # forgotten if a message omits it.
        if event.id:
            self.last_id = event.id

        return event

    if six.PY2:
        next = __next__


class Event():
    def __init__(self, data='', event='', id=None, retry=None) -> None:
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry

    def __str__(self):
        return self.data


def parse_event(buffer: str) -> Event:
    """
        Given a possibly-multiline string representing an SSE message, parse it
        and return a Event object.
        """
    event = Event()
    for line in buffer.splitlines():
        match = SSEFIELDS.match(line)
        if match is None:
            # Malformed line.  Discard but warn.
            warnings.warn('Invalid SSE line: "%s"' % line, SyntaxWarning)
            continue

        name = match.group('name')
        if name == '':
            #If the line starts with a U+003A COLON character (:) Ignore the line.
            continue
        value = match.group('value')

        if name == 'data':
            # If we already have some data, then join to it with a newline.
            # Else this is it.
            if event.data:
                event.data = '%s\n%s' % (event.data, value)
            else:
                event.data = value
        elif name == 'event':
            event.event = value
        elif name == 'id':
            event.id = value
        elif name == 'retry':
            event.retry = int(value)

    return event


class SSE(threading.Thread):
    """SSE is a threading client that puts a parsed event from
    the url into the specified queue
    """

    def __init__(
            self,
            session: requests.Session,
            url: str,
            garden: queue.Queue,
    ) -> None:
        super().__init__()
        self.garden = garden
        self._client = SSEClient(url, session=session)

    def run(self):
        for event in self._client:
            resp = json.loads(event.data)
            try:
                self.garden.put_nowait(resp['trees'])
            except queue.Full:
                # cheap trick: if the queue is full just read one note
                # the assumption is that the queue has maxsize = j1
                self.garden.get_nowait()
                self.garden.put_nowait(resp['trees'])

            LOGGER.info("Got a new garden %r", resp)
