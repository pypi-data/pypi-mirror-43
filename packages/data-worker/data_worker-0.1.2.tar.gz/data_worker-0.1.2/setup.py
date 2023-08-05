# https://packaging.python.org/tutorials/packaging-projects/
# 1. Change version
# 2. python3 setup.py sdist bdist_wheel
# 3. python3 -m twine upload dist/*

import setuptools
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'

with open(ROOT_DIR + "README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='data_worker',
    version='0.1.2',
    author="Kevin O'Brien",
    author_email="Kevin.OBrien@Synechron.com",
    description="An API wrapper for all data sources used by Synechron's Data Science team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Kevin.OBrien/data_worker",
    packages=setuptools.find_packages(ROOT_DIR),
    classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
