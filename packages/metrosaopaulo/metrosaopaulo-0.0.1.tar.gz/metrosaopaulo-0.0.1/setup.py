import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metrosaopaulo",
    version="0.0.1",
    author="Julio Manuel Blanco Perez",
    author_email="jblancoperez@gmail.com",
    description="Get São Paulo Metro Status descriptions from Official Site",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jblancoperez/metrosaopaulo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

