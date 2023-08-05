import setuptools
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


with open(ROOT_DIR + "README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='data_worker',
    version='0.1',
    # packages=['data_worker'],
    author="Kevin O'Brien",
    author_email="Kevin.OBrien@Synechron.com",
    description="An API wrapper for all data sources used by Synechron's Data Science team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Kevin.OBrien/data_worker",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
