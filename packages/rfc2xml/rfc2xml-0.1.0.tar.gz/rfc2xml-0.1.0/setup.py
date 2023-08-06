import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rfc2xml",
    version="0.1.0",
    author="David Southgate",
    author_email="d@davidsouthgate.co.uk",
    description="Tool to process an RFC or Internet Standard into XML or a DOM structure for document processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/davidksouthgate/rfc2xml/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
