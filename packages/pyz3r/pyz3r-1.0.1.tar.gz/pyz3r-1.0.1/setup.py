import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pyz3r",
    version="1.0.1",
    author="Thomas Prescott",
    author_email="tcprescott@gmail.com",
    description="A python module for interacting with alttpr.com, such as generating new z3r games, and patching existing games.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tcprescott/pyz3r",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
)