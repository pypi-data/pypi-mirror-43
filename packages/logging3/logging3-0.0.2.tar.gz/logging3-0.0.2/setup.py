import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logging3",
    version="0.0.2",
    author="Philipp Mayer",
    author_email="dev@paradoxon.at",
    description="Useful logging enhancement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmayer/logging3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
