Introduction
============

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
 
- Currently supported Python backends are `pyfive`, `netCDF4`, `zarr`,
  `scipy.io.netcdf_file`, `xarray`, `ppfive`, and `h5py`.

- Currently supported dataset formats that can be read by at least one
  of those backends are ``netCDF-4``, ``netCDF-3``, ``Zarr v3``,
  ``Zarr v2``, ``Kerchunk``, ``PP``, and ``fields file`` (the last two
  are formats used at the UK Met Office).

- Additionally, a dataset can be defined by a `pyfive`-like or
  `xarray`-like object in memory.

Here is a simple example of how to use `xnetcdf` to open a dataset
and inspect its contents:

.. code-block:: python

    import xnetcdf as xn

    # Open a dataset in any of the formats:
    # netCDF-4, netCDF-3, Zarr v3, Zarr v2, Kerchunk, PP, fields file
    with xn.Dataset('path/to/your/dataset') as nc:
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
