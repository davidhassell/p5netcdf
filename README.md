[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/DOI/XX.XXXX/zenodo.XXXXXXX.svg)](https://doi.org/XX.XXXX/zenodo.XXXXXXXX)
[![Documentation Status](https://app.readthedocs.org/projects/p5netcdf/badge/?version=latest)](https://p5netcdf.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/NCAS-CMS/p5netcdf/actions/workflows/pytest.yml/badge.svg)](https://github.com/NCAS-CMS/p5netcdf/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/NCAS-CMS/p5netcdf/graph/badge.svg?token=3In5JuzeGK)](https://codecov.io/gh/NCAS-CMS/p5netcdf)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/p5netcdf/badges/version.svg)](https://anaconda.org/conda-forge/p5netcdf)

**[Read the documentation](https://app.readthedocs.org/projects/p5netcdf/builds/)**

# p5netcdf

`p5netcdf` is an open source library for representing with a common
netCDF API that follows the [netCDF Enhanced Data
Model](https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html),
datasets in a variety of formats accessed through a variety of Python
backends.

A dataset is mapped to a `Dataset` object, which contains netCDF
groups (`Group` objects), dimensions (`Dimension` objects), variables
(`Variable` objects), and attributes. In turn, a variable is
associated with dimensions and may contain attributes; and a group may
contain other groups, dimensions, variables, and attributes.
 
- Currently supported are dataset formats are `netCDF-4`, `netCDF-3`,
`Zarr3`, `Zarr2`, `Kerchunk`, `PP`, and `fields file` (the last two
being formats used at the UK Met Office).

- Currently supported Python backends are `pyfive`, `netCDF4`,
`zarr`, `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

- Additionally, a dataset can be defined by a `pyfive`-like or
`xarray`-like object in memory.

The `p5netcdf` API has been been designed to be "largely consistent"
with the APIs of `netCDF4`, `pyfive` and `h5netcdf`. This means that,
whilst `p5netcdf` can't be used as a perfect drop-in for any of these
three libraries, most attributes and methods of each one of them can
be found in `p5netcdf`, and with the same behaviour. For instance,
`p5netcdf` variables have a `chunks` attribute and a `chunking`
method - the former is also found in the `pyfive` and `h5netcdf`
libraries, the latter in the `netCDF4` library.

Feature requests or bug reports should be reported in the
[issues](https://github.com/NCAS-CMS/p5netcdf/issues).

## Dependencies

`p5netcdf` is tested against Python versions 3.10 to 3.14.  It may
also work with other Python versions.

The only dependency to required run the software, besides Python, is
`numpy`. However, the backend libraries `pyfive`, `netCDF4`, `zarr`,
`scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`, can only be
used if they are also installed.

## Install

p5netcdf can be installed using `pip` using the command:

    pip install p5netcdf

or, to also install all of the backend libraries:

    pip install p5netcdf[all]

`conda` packages, which also install all of the backend libraries, are
also available from conda-forge:

    conda install -c conda-forge p5netcdf

To install from source in your home directory use:

    pip install --user ./p5netcdf

The library can also be imported directly from the `p5netcdf` source
root directory:

    pip install -e . 

### Conda-forge feedstock

Package repository [conda-forge
feedstock](https://github.com/conda-forge/p5netcdf-feedstock)

## Development

### Testing

`p5netcdf` comes with a test suite in the `tests` directory.  These
tests can be exercised using the `pytest` command from the root
directory (requires installation of the `pytest` package).

### Documentation

Build locally with Sphinx:

    $ sphinx-build -Ea doc doc/build

### Codecov

Test coverage assessement is done using
[codecov](https://app.codecov.io/gh/NCAS-CMS/p5netcdf/)
