import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kewhois",
    version="0.0.1",
    author="Felix Mutugi",
    author_email="stunnerszone@gmail.com",
    description="A Kenyan whois lookup client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeveloperFelix/kewhois",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)