import os

import setuptools


class get_numpy_include(os.PathLike):
    """Helper class to determine the numpy include path. This postpones importing numpy until it was installed."""

    def __str__(self):
        import numpy
        return numpy.get_include()

    def __fspath__(self):
        return str(self)


pimpy_c_ext = setuptools.Extension(
    name="pimpy_c",
    sources=["pimpy_c/transformations.pyx"],
    include_dirs=[get_numpy_include()],
    language="c++"
)
pimpy_c_ext.cython_c_in_temp = True


with open("README.rst", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="pimpy",
    version="0.1.0",
    author="Philip Schill",
    author_email="philip.schill@gmx.de",
    url="https://gitlab.com/pschill/pimpy",
    description="Contains selected image processing functions",
    long_description=long_description,
    python_requires=">=3.6",
    packages=["pimpy"],
    ext_modules=[pimpy_c_ext],
    setup_requires=[
        "cython >= 0.29"
    ],
    install_requires=[
        "numpy >= 1.15",
        "scipy >= 1.1"
    ],
    tests_require=[
        "imageio >= 2.4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
