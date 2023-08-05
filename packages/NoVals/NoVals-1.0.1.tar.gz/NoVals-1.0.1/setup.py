import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NoVals",
    version="1.0.1",
    author="Morgan Saville",
    author_email="gbt505@hotmail.com",
    description="Throws an error if any literals are in the source code, to help with verifying NoVals Code Golf solutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThePythonist/NoVals",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
