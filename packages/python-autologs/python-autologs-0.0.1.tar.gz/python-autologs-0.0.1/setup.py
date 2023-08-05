import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-autologs",
    version="0.0.1",
    author="Meni Yakove",
    author_email="myakove@gmail.com",
    description="Auto generate logs for functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myakove/python-autologs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
