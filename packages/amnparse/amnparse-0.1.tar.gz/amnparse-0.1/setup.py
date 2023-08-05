import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="amnparse",
    version="0.1",
    author="The Munshi Group",
    author_email="support@munshigroup.com",
    description="Parser libraries used by the AmmuNation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/munshigroup/amnparse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)