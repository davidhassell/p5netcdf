Datasets and backends
=====================

A dataset may be provided to `xnetcdf.Dataset` in a variety of forms,
and this form will be passed to the backends. An attempt to open given
dataset is made by the backends in the order in which they are
provided, stopping after the first successful read. The output from
this final backend is then used to create `xnetcdf`'s common netCDF
API.

The 

* String-like (such as `str` or `pathlib.Path`)

  A string provides the name of the dataset, and may be a file or
  directory on a local or remote file system.
  
* File-like (such as `io.BufferedReader` or the result of an `fsspec`
  file system open)

  A file-like object the name of the dataset, and may be a file or
  directory on a local or remote file system.
  

* Directory-like (such as `fsspec.mapping.FSMap`)

  Todo

* `pyfive`-like (i.e. `pyfive.File`, or an object registered as a
  subclass of `pyfive.File`)

  TODO

* `xarray`-like (i.e. `xarray.Dataset` or `xarray.DataTree`, or an
  object registered as a subclass of either of those)

  TODO

Note that:

.. code-block:: python

   >>> nc = xnetcdf.File('dataset', backend='pyfive')

is identical to:

.. code-block:: python

   >>> p = pyfive.File('dataset')
   >>> nc = xnetcdf.Dataset(p)

Also:

.. code-block:: python

   >>> nc = xnetcdf.Dataset('dataset', backend='xarray')

is identical to:

.. code-block:: python

   >>> x = xarray.open_datatree(
   ...     'dataset', mask_and_scale=False, decode_cf=False
   ... )
   >>> nc = xnetcdf.Dataset(x)
