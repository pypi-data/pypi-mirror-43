from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="testing_pubsub",
    version="0.0.6",
    author="Steven Harlow",
    author_email="stharlow@gmail.com",
    description="Run a temporary instance of Cloud PubSub emulator for Python tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peachfinance/testing_pubsub",
    packages=find_packages(),
    install_requires=['google.cloud'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
