from setuptools import setup, find_packages

setup(
    name="hydrogen",
    version="0.3.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[],
)
