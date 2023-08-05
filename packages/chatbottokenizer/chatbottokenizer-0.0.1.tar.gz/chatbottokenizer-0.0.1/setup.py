import setuptools
import unittest

with open("README.md", "r") as fh:
    long_description = fh.read()


def ts():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setuptools.setup(
    name="chatbottokenizer",
    version="0.0.1",
    author="Max Harley",
    author_email="maxh@maxh.io",
    test_suite='setup.ts',
    description="Tokenizer for chat bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t94j0/chatbot-tokenizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
