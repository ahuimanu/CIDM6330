from setuptools import find_packages, setup

"""
More on packaging: https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

setup(
    name="flaskr",
    version="0.0.4",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
    ],
)
