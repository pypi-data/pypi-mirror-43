from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["tqdm>=4.23.4", "numpy>=1.16.2"]

setup(
    name="coomatrix",
    version="0.0.1",
    author="Gaurav Singh",
    author_email="gs8763076@gmail.com",
    description="This package calculates the Co-occurence matrix.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/calculatecooccurencematrix/coomatrix",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
