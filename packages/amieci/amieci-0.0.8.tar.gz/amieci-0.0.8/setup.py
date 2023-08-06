import os

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def version():
    "get version from VERSION file"
    version_file = open(os.path.join(ROOT_DIR, 'amieci/VERSION'))
    return version_file.read().strip()


setup(
    name="amieci",
    version=version(),
    description="The python API for amie",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.amie.ai",
    author="johannes beil",
    author_email="jb@amie.dk",
    license="private",
    packages=["amieci"],
    package_data={'amieci': ['amieci/*']},
    include_package_data=True,
    install_requires=["requests", "pandas"],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
