[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/DOI/XX.XXXX/zenodo.XXXXXXX.svg)](https://doi.org/XX.XXXX/zenodo.XXXXXXXX)
[![Documentation Status](https://app.readthedocs.org/projects/xnetcdf/badge/?version=latest)](https://xnetcdf.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/NCAS-CMS/xnetcdf/actions/workflows/pytest.yml/badge.svg)](https://github.com/NCAS-CMS/xnetcdf/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/NCAS-CMS/xnetcdf/graph/badge.svg?token=3In5JuzeGK)](https://codecov.io/gh/NCAS-CMS/xnetcdf)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/xnetcdf/badges/version.svg)](https://anaconda.org/conda-forge/xnetcdf)

**[Read the documentation](https://app.readthedocs.org/projects/xnetcdf/builds/)**

# xnetcdf

`xnetcdf` is an open source library for representing datasets in a
variety of formats and accessed through a variety of Python backends,
with a common netCDF API that follows the [netCDF Enhanced Data
Model](https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html).


A dataset is mapped to a `Dataset` object, which contains netCDF
groups (`Group` objects), dimensions (`Dimension` objects), variables
(`Variable` objects), and attributes. A variable is associated with
dimensions and may contain attributes; and a group may contain other
groups, dimensions, variables, and attributes.
 
- Currently supported dataset formats are `netCDF-4`, `netCDF-3`,
`Zarr3`, `Zarr2`, `Kerchunk`, `PP`, and `fields file` (the last two
being formats used at the UK Met Office).

- Currently supported Python backends are `pyfive`, `netCDF4`,
`zarr`, `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

- Additionally, a dataset can be defined by a `pyfive`-like or
`xarray`-like object in memory.

The `xnetcdf` API has been been designed to be "largely consistent"
with the APIs of `netCDF4`, `pyfive` and `h5netcdf`. This means that,
whilst `xnetcdf` can't be used as a perfect drop-in for any of these
three libraries, most attributes and methods of each one of them can
be found in `xnetcdf`, and with the same behaviour. For instance,
`xnetcdf` variables have a `chunks` attribute and a `chunking`
method - the former is also found in the `pyfive` and `h5netcdf`
libraries, the latter in the `netCDF4` library.

Feature requests or bug reports should be reported in the
[issues](https://github.com/NCAS-CMS/xnetcdf/issues).

## Dependencies

`xnetcdf` is tested against Python versions 3.10 to 3.14.  It may
also work with other Python versions.

The only dependency to required run the software, besides Python, is
`numpy`. However, the backend libraries `pyfive`, `netCDF4`, `zarr`,
`scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`, can only be
used if they are also installed.

## Install

xnetcdf can be installed using `pip` using the command:

    pip install xnetcdf

or, to also install all of the backend libraries:

    pip install xnetcdf[all]

`conda` packages, which also install all of the backend libraries, are
also available from conda-forge:

    conda install -c conda-forge xnetcdf

To install from source in your home directory use:

    pip install --user ./xnetcdf

The library can also be imported directly from the `xnetcdf` source
root directory:

    pip install -e . 

### Conda-forge feedstock

Package repository [conda-forge
feedstock](https://github.com/conda-forge/xnetcdf-feedstock)

## Development

### Testing

`xnetcdf` comes with a test suite in the `tests` directory.  These
tests can be exercised using the `pytest` command from the root
directory (requires installation of the `pytest` package).

### Documentation

Build locally with Sphinx:

    $ sphinx-build -Ea doc doc/build

### Codecov

Test coverage assessement is done using
[codecov](https://app.codecov.io/gh/NCAS-CMS/xnetcdf/)
