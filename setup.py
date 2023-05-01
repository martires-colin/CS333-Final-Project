from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'CS333 Final Project'
LONG_DESCRIPTION = 'CS333 Testing and DevOps Final Project @ University of Nevada, Reno.'

# Setting up
setup(
    name="CS333-Final-Project",
    version=VERSION,
    author="Colin Martires",
    author_email="cmartires@nevada.unr.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ]
)