import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yieldcurve",
    version="0.0.1",
    author="Vladimir Emelianov",
    author_email="vlademelianov@gmail.com",
    description="Estimates yield curves using various methodologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlademel/yieldcurve",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)