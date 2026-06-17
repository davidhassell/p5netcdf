[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18599472.svg)](https://doi.org/XX.XXXX/zenodo.XXXXXXXX)
[![Documentation Status](https://app.readthedocs.org/projects/p5netcdf/badge/?version=latest)](https://p5netcdf.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/NCAS-CMS/p5netcdf/actions/workflows/pytest.yml/badge.svg)](https://github.com/NCAS-CMS/p5netcdf/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/NCAS-CMS/p5netcdf/graph/badge.svg?token=3In5JuzeGK)](https://codecov.io/gh/NCAS-CMS/p5netcdf)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/p5netcdf/badges/version.svg)](https://anaconda.org/conda-forge/p5netcdf)

**[Latest documentation on Read the Docs](https://app.readthedocs.org/projects/p5netcdf/builds/)**

# p5netcdf

`p5netcdf` is an open source library for representing datasets in a
variety of formats accessed through a variety of Python backends, all
with a common netCDF-4 API.

A dataset is mapped to a ``Dataset`` object, which contains netCDF
groups (`Group` objects), dimensions (`Dimension` objects), variables
(`Variable` objects), and attributes. In turn a variable is associated
with dimensions and may contain attributes; and group may contain
other groups, dimensions, variables, and attributes.
 
- Currently supported are dataset formats are `netCDF-4`, `netCDF-3`,
`Zarr3`, `Zarr2`, `Kerchunk`, `PP`, and `fields file` (the last two
being formats used at the UK Met Office).

- Currently supported Python backends are `pyfive`, `netCDF4`,
`zarr`, `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

`p5netcdf` aims to support the same API as
[`h5py`](https://github.com/h5py/h5py) for reading files.

Feature requests or bug reports should be reported in the
[Issues](https://github.com/NCAS-CMS/p5netcdf/issues).

## Dependencies

`p5netcdf` is tested against Python versions 3.10 to 3.14.  It may
also work with other Python versions.

The only dependency to run the software, besides Python, is `numpy`.

## Install

p5netcdf can be installed using `pip` using the command::

    pip install p5netcdf

`conda` packages are also available from conda-forge::

    conda install -c conda-forge p5netcdf

To install from source in your home directory use::

    pip install --user ./p5netcdf

The library can also be imported directly from the `p5netcdf` source
root directory::

    pip install -e . 

### Conda-forge feedstock

Package repository [conda-forge feedstock](https://github.com/conda-forge/p5netcdf-feedstock)

## Development

### git

You can check out the latest `p5netcdf` souces with the command::

    git clone https://github.com/NCAS-CMS/p5netcdf.git

### testing

`p5netcdf` comes with a test suite in the `tests` directory.  These
tests can be exercised using the `pytest` command from the root
directory (requires installation of the `pytest` package).

### Documentation

Build locally with Sphinx:

    $ sphinx-build -Ea doc doc/build

### Codecov

Test coverage assessement is done using
[codecov](https://app.codecov.io/gh/NCAS-CMS/p5netcdf/)
