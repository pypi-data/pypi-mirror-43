import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyColored",
    version="1.0",
    author="Patrik Repan",
    author_email="repan.patrik.dev@gmail.com",
    description="Awesome Python package that allows you to format and color your text!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrHedryX/PyColored",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
