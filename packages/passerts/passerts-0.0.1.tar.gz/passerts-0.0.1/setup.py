import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passerts",
    version="0.0.1",
    author="Eric Yang",
    author_email="eric.uvw@gmail.com",
    description="A collection of assertion and check utilities",
    long_description="A collection of assertion and check utilities",
    long_description_content_type="text/markdown",
    url="https://github.com/pointertoeric/passerts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
