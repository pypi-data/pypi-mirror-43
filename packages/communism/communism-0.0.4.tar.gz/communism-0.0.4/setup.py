import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="communism",
    version="0.0.4",
    author="Karl Marx",
    author_email="dacurse0@gmail.com",
    description="The best package on PyPi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)
