import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycompute",
    version="1.0",
    author="Narasimha Prasanna HN",
    author_email="narasimhaprasannahn@gmail.com",
    description="A computation graph library with support for parallelism , numerical and string computations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Narasimha1997/bzCompute",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)