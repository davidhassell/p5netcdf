NetCDF Dimension
================

The examples on this page use the ``test.nc`` dataset
(`download 28 KB
<https://raw.githubusercontent.com/davidhassell/xnetcdf/main/tests/data/test.nc>`_).

.. _Dimension-name:

Dimension name
--------------

The name of an `xnetcdf.Dimension` instance is accessed with the
`~xnetcdf.Dimension.name` and `~xnetcdf.Dimension.path` attributes,
providing the name relative to the parent group and the absolute path
name respectively.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> d = nc['forecast'].dimensions['lon']  # Select a dimension
   >>> d
   lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>
   >>> d.name
   'lon'
   >>> d.path
   '/forecast/lon'

.. _Dimension-size:

Dimension size
--------------

The size of an `xnetcdf.Dimension` instance is accessed with the
`~xnetcdf.Dimension.size` attribute, and the unlimited status is
accessed with the `~xnetcdf.Dimension.isunlimited` method.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> d = nc['forecast'].dimensions['lon']  # Select a dimension
   >>> d
   lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>
   >>> d.group()
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> d.isunlimited()
   True

.. _Dimension-group:

Dimension group
---------------

The parent group in which the an `xnetcdf.Dimension` instance is
defined is accessed with the `~xnetcdf.Dimension.group` method.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> d = nc['forecast'].dimensions['lon']  # Select a dimension
   >>> d
   lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>
   >>> d.group()
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
