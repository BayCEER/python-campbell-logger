import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-campbell-logger",
    version="1.1.0",
    author="Oliver Archner",
    author_email="oliver.archner@uni-bayreuth.de",
    description="Client for Campbell Scientific loggers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayceer/python-campbell-logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=['requests'] 
)