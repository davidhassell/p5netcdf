NetCDF Variable
===============

The examples on this page use the ``test.nc`` dataset
(`download 28 KB
<https://raw.githubusercontent.com/davidhassell/xnetcdf/main/tests/data/test.nc>`_).

.. _Variable-name:

Variable name
-------------

The name of an `xnetcdf.Variable` instance is accessed with the
`~xnetcdf.Variable.name` and `~xnetcdf.Variable.path` attributes,
providing the name relative to the parent group and the absolute path
name respectively.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> v = nc['/forecast/model/q']  # Select a variable
   >>> v
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> v.name
   'q'
   >>> g.path
   '/forecast/model/q'

.. _Variable-data:

Variable data
-------------

The data array of an `xnetcdf.Variable` instance is accessed by direct
indexing, following whatever indexing rules are allowed by the
underlying backend object.

The requested subspace is always returned as a `numpy` array.

.. note:: Since the interpretation of the indices is handled entirely
          by the underlying backend object, the same indices may
          define a different subspace for different underlying
          backends.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> v = nc['/forecast/model/q']  # Select a variable
   >>> v
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> v.shape  # Inspect the data shape
   (5, 8)
   >>> v[...]  # Get the entire data array
   array([[0.007, 0.034, 0.003, 0.014, 0.018, 0.037, 0.024, 0.029],
          [0.023, 0.036, 0.045, 0.062, 0.046, 0.073, 0.006, 0.066],
          [0.11 , 0.131, 0.124, 0.146, 0.087, 0.103, 0.057, 0.011],
          [0.029, 0.059, 0.039, 0.07 , 0.058, 0.072, 0.009, 0.017],
          [0.006, 0.036, 0.019, 0.035, 0.018, 0.037, 0.034, 0.013]],
         dtype=float32)
   >>> q[:,  [1, 3, 2]]  # Get a subspace of the data array
   array([[0.034, 0.014, 0.003],
          [0.036, 0.062, 0.045],
          [0.131, 0.146, 0.124],
          [0.059, 0.07 , 0.039],
          [0.036, 0.035, 0.019]], dtype=float32)

.. _Variable-attributes:

Variable attributes
-------------------

The attributes of an `xnetcdf.Variable` instance are accessed with the
`~xnetcdf.Variable.attrs` attribute.  following whatever indexing
rules are allowed by the underlying backend object.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> v = nc['/forecast/lon']  # Select a variable
   >>> v
   lon: <xnetcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
   >>> v.attrs  # Get the attributes
   {'bounds': '/forecast/lon_bnds',
    'standard_name': 'longitude',
    'units': 'degrees_east'}

Attributes follow the netCDF conventions that assign special meaning
to selected attributes, treating them as internal attributes that may
be required to define the dataset structure.

These attributes are ``CLASS``, ``NAME``, ``REFERENCE_LIST``,
``DIMENSION_LIST``, ``DIMENSION_LABELS``, and ``_ARRAY_DIMENSIONS``,
as well as any attributes that start with ``_Netcdf4``, ``_nc``, or
``_NC``; and will not appear in the attribute collection.

.. _Variable-dimensions:

Variable dimensions
-------------------

The dimensions of an `xnetcdf.Variable` instance are accessed with the
`~xnetcdf.Variable.dimensions` and `~xnetcdf.Variable.dimension_paths`
attributes, and the `~xnetcdf.Variable.get_dims` method. The
attributes return the dimension names as relative or absolute path
names respectively. The method returns the `xnetcdf.Dimension`
objects. In each case, the dimension order corresponds to the axes of
the variable's data array.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> v = nc['/forecast/model/q']  # Select a variable
   >>> v
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> v.dimensions
   ('lat', 'lon')
   >>> v.dimension_paths
   ('/forecast/model/lat', '/forecast/lon')
   >>> v.get_dims()
   (lat: <xnetcdf.Dimension: /forecast/model/lat, size=5>,
    lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>)

.. _Variable-group:

Variable group
--------------

The parent group in which the an `xnetcdf.Variable` instance is
defined is accessed with the `~xnetcdf.Variable.group`
method. 

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> v = nc['/forecast/model/q']  # Select a variable
   >>> v
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> v.group()
   model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>

