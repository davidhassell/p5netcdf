Introduction
============

`p5netcdf` is an open source library for representing with a common
netCDF API that follows the `netCDF Enhanced Data
Model <https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html>`_,
datasets in a variety of formats accessed through a variety of Python
backends.

A dataset is mapped to a ``Dataset`` object, which contains netCDF
groups (``Group`` objects), dimensions (``Dimension`` objects), variables
(``Variable`` objects), and attributes. In turn, a variable is
associated with dimensions and may contain attributes; and a group may
contain other groups, dimensions, variables, and attributes.
 
- Currently supported are dataset formats are ``netCDF-4``, ``netCDF-3``,
  ``Zarr3``, ``Zarr2``, ``Kerchunk``, ``PP``, and ``fields file`` (the last two
  being formats used at the UK Met Office).

- Currently supported Python backends are ``pyfive``, ``netCDF4``,
  ``zarr``, ``scipy.io.netcdf_file``, ``xarray``, ``ppfive``, and ``h5py``.

- Additionally, a dataset can be defined by a ``pyfive``-like or
  ``xarray``-like object in memory.

The `p5netcdf` API has been been designed to be "largely consistent"
with the APIs of ``netCDF4``, ``pyfive`` and ``h5netcdf``. This means that,
whilst `p5netcdf` can't be used as a perfect drop-in for any of these
three libraries, most attributes and methods of each one of them can
be found in `p5netcdf`, and with the same behaviour. For instance,
`p5netcdf` variables have a ``chunks`` attribute and a ``chunking``
method - the former is also found in the ``pyfive`` and ``h5netcdf``
libraries, the latter in the ``netCDF4`` library.

Feature requests or bug reports should be reported in the
`issues <https://github.com/NCAS-CMS/p5netcdf/issues>`_.
