import setuptools

from quickdone import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickdone",
    version=__version__,
    author="quickdone",
    author_email="donequick@outlook.com",
    description="A handy toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donequick/quickdone",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'xlrd',
        'pandas'
    ],
    python_requires='>=3.7.2'
)