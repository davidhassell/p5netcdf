[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/DOI/XX.XXXX/zenodo.XXXXXXX.svg)](https://doi.org/XX.XXXX/zenodo.XXXXXXXX)
[![Documentation Status](https://app.readthedocs.org/projects/xnetcdf/badge/?version=latest)](https://xnetcdf.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/NCAS-CMS/xnetcdf/actions/workflows/pytest.yml/badge.svg)](https://github.com/NCAS-CMS/xnetcdf/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/NCAS-CMS/xnetcdf/graph/badge.svg?token=3In5JuzeGK)](https://codecov.io/gh/NCAS-CMS/xnetcdf)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/xnetcdf/badges/version.svg)](https://anaconda.org/conda-forge/xnetcdf)

**[Read the documentation](https://xnetcdf.readthedocs.io)**

# xnetcdf

`xnetcdf` is an open source library for representing datasets, in a
variety of formats and accessed through a variety of Python backends,
with a common netCDF API that follows the `netCDF Enhanced Data Model
<https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html>`_.

A dataset is mapped to a `xnetcdf.Dataset` object, which contains
netCDF groups (`xnetcdf.Group` objects), dimensions
(`xnetcdf.Dimension` objects), variables (`xnetcdf.Variable` objects),
and attributes. A variable is associated with dimensions and may
contain attributes; and a group may contain other groups, dimensions,
variables, and attributes.
 
- Currently supported dataset formats are ``netCDF-4``, ``netCDF-3``,
  ``Zarr v3``, ``Zarr v2``, ``Kerchunk``, ``PP``, and ``fields file``
  (the last two are 
  formats used at the UK Met Office).

- Currently supported Python backends are `pyfive`, `netCDF4`, `zarr`,
  `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

- Additionally, a dataset can be defined by a `pyfive`-like or
  `xarray`-like object in memory.

Here is a simple example of how to use `xnetcdf` to open a dataset
and inspect its contents:

``` python
import xnetcdf

# Open a dataset in any of the formats:
# netCDF-4, netCDF-3, Zarr v3, Zarr v2, Kerchunk, PP, fields file
with xnetcdf.Dataset('path/to/your/dataset') as nc:
    # A one-line summary of the dataset
    print(repr(nc))

    # A longer summary of the dataset
    print(nc)

    # Use the structure() method for a more detailed view
    nc.structure()

    # The dataset attributes
    print(nc.attrs)

    # Access a variable
    if 'temperature' in nc.variables:
        var = nc.variables['temperature']
        print(var)

        # Print the variable attributes
        print(var.attrs)

        # Print the data array from the variable
        print(var[...])
    
    # Use the dump() method for an even more detailed view
    nc.dump()

    # Use the dump() method with "data=True" for yet more detail
    nc.dump(data=True)

    # Use the ncdump() to emulate `$ ncdump -h path/to/your/dataset`
    nc.ncdump()
```

See the
[documentation](https://xnetcdf.readthedocs.io/en/latest/quickstart/)
for more information and examples.

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

## Contributing

See the [Contributing
page](https://xnetcdf.readthedocs.io/en/latest/contributing/) of the
documentation for details.

## Development

### Testing

Run the test suite (requires installation of the `pytest` package):

``` shell
$ cd xnetcdf
$ pytest
```
   
`xnetcdf` comes with a test suite in the `tests` directory.  These
tests can be exercised using the `pytest` command from the root
directory (requires installation of the `pytest` package).

### Documentation

Build locally with Sphinx:

    $ cd xnetcdf/docs
	$ make html
	
View the documentation locally at `xnetcdf/docs/build/html/index.html`.
