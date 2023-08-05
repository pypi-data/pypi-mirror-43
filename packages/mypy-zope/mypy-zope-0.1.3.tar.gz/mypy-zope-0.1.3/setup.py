from setuptools import setup, find_packages

long_description = """
# Plugin for mypy to support zope.interface

The goal is to be able to make zope interfaces to be treated as types in mypy
sense.

For feature description and usage instructions, see https://github.com/Shoobx
/mypy-zope.
"""

setup(
    name="mypy-zope",
    version="0.1.3",
    author="Andrey Lebedev",
    author_email="andrey.lebedev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Plugin for mypy to support zope interfaces",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["mypy>=0.660", "zope.interface", "zope.schema"],
    extras_require={"test": ["pytest>=4.0.0,<4.1.0", "pytest-cov", "lxml"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    include_package_data=True,
    zip_safe=False,
)
