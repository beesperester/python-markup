from setuptools import setup, find_packages

setup(
    name="hydrogen",
    version="0.1.0",
    packages=find_packages("src/hydrogen"),
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
    ],
)
