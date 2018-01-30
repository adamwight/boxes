import os.path
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]


setup(
    name="boxes",
    version="0.2",
    packages=["boxes"],
    author="Adam Wight",
    author_email="adamw@ludd.net",
    description="Text GUI for DigitalOcean cloud management",
    long_description=read('README.md'),
    license="GPLv3.0",
    url="https://github.com/adamwight/boxes",
    entry_points={
        "console_scripts": [
            "boxes = boxes.boxes:main",
        ],
    },
    install_requires=requirements("requirements.txt"),
)
