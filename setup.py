import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regpyhdfe", # Replace with your own username
    version="0.0.8",
    author="Andrius Buinovskij",
    author_email="andriusb@ethz.ch",
    description="Simple wrapper for PyHDFE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lod531/regPyHDFE",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyhdfe",
        "pandas", 
        "numpy", 
        "statsmodels", 
        "patsy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
