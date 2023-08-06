import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="A-share",
    version="0.0.1",
    author="Charles",
    author_email="xindeng3@gmail.com",
    description="package for A-share of mainland China",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xindzju",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)