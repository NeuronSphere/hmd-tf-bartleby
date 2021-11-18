import pathlib

from setuptools import find_packages, setup

setup(
    name="module_name",
    version="0.0.1",
    description="Runs the document generation transform",
    author="Kate Walls",
    author_email="kate.walls@hmdlabs.io",
    license="unlicensed",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
