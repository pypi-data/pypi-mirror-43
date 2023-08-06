import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fractals",
    version="0.0.1",
    author="Fomys",
    author_email="fomys@gmx.us",
    description="A simple fractal generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fomys/Fractals",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)