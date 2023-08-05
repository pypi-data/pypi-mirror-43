from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(
    name="mediathek",
    version="0.0.1",
    url="https://github.com/Lanseuo/mediathek",
    description="Crawler for German TV media centers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Lucas Hild",
    author_email="contact@lucas-hild.de",
    packages=find_packages(),
    install_requires=["requests"]
)
