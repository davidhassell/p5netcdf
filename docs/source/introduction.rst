Introduction
============

`xnetcdf` is an open source library for representing datasets, in a
variety of formats and accessed through a variety of Python backends,
with a common netCDF API that follows the `netCDF Enhanced Data Model
<https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html>`_.

A dataset is mapped to a `xnetcdf.Dataset` object, which contains
netCDF groups (`xnetcdf.Group` objects), netCDF dimensions
(`xnetcdf.Dimension` objects), netCDF variables (`xnetcdf.Variable`
objects), and attributes. A variable is associated with dimensions and
may contain attributes; and a group may contain other groups,
dimensions, variables, and attributes.
 
- Currently supported Python backends are `pyfive`, `netCDF4`, `zarr`,
  `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

- Currently supported dataset formats that can be read by at least one
  of the backends are `netCDF-4
  <https://docs.unidata.ucar.edu/nug/current/netcdf_introduction.html>`_,
  `netCDF-3
  <https://docs.unidata.ucar.edu/nug/current/netcdf_introduction.html>`_,
  `Zarr v3 <https://zarr-specs.readthedocs.io/en/latest/specs.html>`_,
  `Zarr v2
  <https://zarr-specs.readthedocs.io/en/latest/v2/v2.0.html>`_,
  `Kerchunk <https://fsspec.github.io/kerchunk>`_, PP, and fields file
  (the last two are UK Met Office formats).

- Additionally, a dataset can be defined by a `pyfive`-like or
  `xarray`-like object in memory.

Here is a simple example of how to use `xnetcdf` to open a dataset
and inspect its contents:

.. code-block:: python

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('path/to/your/dataset')  # Open the dataset
   >>> print(nc)  # Inspect the dataset contents
   path/to/your/dataset: <xnetcdf.Dataset: /, 3 dimensions, 6 variables, 0 groups>
       Dimensions:
           lat: <xnetcdf.Dimension: /lat, size=5>
           bounds2: <xnetcdf.Dimension: /bounds2, size=2>
           lon: <xnetcdf.Dimension: /lon, size=8>
       Variables:
           lat_bnds: <xnetcdf.Variable: /lat_bnds, shape=(5, 2), dimensions=(/lat, /bounds2)>
           lat: <xnetcdf.Variable: /lat, shape=(5,), dimensions=(/lat,)>
           lon_bnds: <xnetcdf.Variable: /lon_bnds, shape=(8, 2), dimensions=(/lon, /bounds2)>
           lon: <xnetcdf.Variable: /lon, shape=(8,), dimensions=(/lon,)>
           time: <xnetcdf.Variable: /time, shape=(), dimensions=()>
           q: <xnetcdf.Variable: /q, shape=(5, 8), dimensions=(/lat, /lon)>
   >>> nc['lat'].attrs  # Get a variable's attributes
   {'bounds': 'lat_bnds',
    'standard_name': 'latitude',
    'units': 'degrees_north'}
   >>> nc['lat'][...]  # Get a variable's data array
   array([-75., -45.,   0.,  45.,  75.])

See :ref:`Quick_start` for more examples.

API
---

The `xnetcdf` API has been been designed to be "largely consistent"
with the APIs of `netCDF4`, `pyfive` and `h5netcdf`. This means that,
whilst `xnetcdf` can't be used as a perfect drop-in for any of these
three libraries, most attributes and methods of each one of them can
be found in `xnetcdf`, and with the same behaviour.

For instance, `xnetcdf.Variable` instances have a
`~xnetcdf.Variable.chunks` attribute and a
`~xnetcdf.Variable.chunking` method -- the former is also found in the
`pyfive` and `h5netcdf` libraries, the latter in the `netCDF4`
library.

Performance
-----------

TODO `xnetcdf` is "structure- and attribute-eager", meaning that
during `Dataset` instantiation, the entire netCDF group, variable, and
dimension structure is parsed; along with all group and variable
attributes. Variable data array access is always via access to the
underlying backend library (see the *backend* and *dataset*
parameters). Some `Variable` and `Group` properties and methods might
also access the underlying backend for structural metadata, but only
for the first request, after which the result is cached (see the
*structural_metadata_strategy* parameter).
