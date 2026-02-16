"""Shim for older pip versions that don't support pyproject.toml builds.

All canonical metadata lives in pyproject.toml. This file duplicates
the essentials so `pip install -e .` works on pip < 21.
"""
from setuptools import setup, find_packages

setup(
    name="cmstuff",
    version="1.1.0",
    description="Common Python shortcuts and utilities that speed up debug workflows",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Williams",
    author_email="williamusanga22@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
