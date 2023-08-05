import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hostname_resolver",
    version="0.1.0",
    author="Daniel Paz Avalos",
    author_email="me@dpazavalos.dev",
    description="A bulk hostname resolver, against known TLDs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpazavalos/bulk-hostname-scanner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
