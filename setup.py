import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-campbell-logger",
    version="0.0.1",
    author="Oliver Archner",
    author_email="oliver.archner@uni-bayreuth.de",
    description="Campbell Scientific logger clients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayceer/python-campbell-logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests','pytz'] 
)