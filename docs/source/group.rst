NetCDF Group
==============

The examples on this page use the ``test.nc`` dataset
(`download 28 KB
<https://raw.githubusercontent.com/davidhassell/xnetcdf/main/tests/data/test.nc>`_).

.. _Group-name:

Group name
----------

The name of an `xnetcdf.Group` instance is accessed with the
`~xnetcdf.Group.name` and `~xnetcdf.Group.path` attributes, providing
the name relative to the parent group and the absolute path name
respectively.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> g = nc['forecast/model']  # Select a group
   >>> g
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> g.name
   'model'
   >>> g.path
   '/forecast/model'

.. _Group-indexing:

Group indexing
--------------

A group or variable object, anywhere in the group hierarchy, can be
accessed by indexing an `xnetcdf.Group` instance with the object's
name.

The name can be provided as an absolute path name or a path name that
is relative to the root group. Relative path names may include ``.``
and ``..`` elements to indicate positions in the group
hierarchy. Consecutive ``/`` characters are reduced to a single ``/``,
and a trailing ``/`` character is always allowed.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> g = nc['forecast']  # Select a group
   >>> g
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> g['model']
   model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
   >>> g['lon']
   lon: <xnetcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
   >>> g['..']
   /home/david/xnetcdf/tests/data/test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> g['./model/q']
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> g['/time']
   time: <xnetcdf.Variable: /time, shape=(), dimensions=()>

An `xnetcdf.Dataset` that contains the root group is also an
`xnetcdf.Group` instance, so see :ref:`Dataset-indexing` for more
examples.


.. _Group-attributes:

Group attributes
----------------

The attributes of an `xnetcdf.Group` instance are accessed with the
`~xnetcdf.Group.attrs` attribute.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> g = nc['/forecast/model']  # Select a group
   >>> g
   model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
   >>> g.attrs  # Get the attributes
   {'group_attr_1': np.int64(12),
    'group_attr_2': 'bar'}

Attributes are derived from the underlying backend object, and not
directly from the dataset on disk. An attribute that exists in a
dataset on disk but has been hidden by the underlying backend object
will not be available to `xnetcdf`. For instance, a backend that
follows the CF conventions might remove ``coordinates`` and ``bounds``
attributes.

Attributes that have special structural meanings according to the
netCDF-4 conventions will not appear in the attribute collection.
These attributes are ``CLASS``, ``NAME``, ``REFERENCE_LIST``,
``DIMENSION_LIST``, ``DIMENSION_LABELS``, and ``_ARRAY_DIMENSIONS``,
as well as any attributes that start with ``_Netcdf4``, ``_nc``, or
``_NC``.

.. _Group-sub-groups:

Group sub-groups
----------------

The sub-groups of an `xnetcdf.Group` instance are accessed with the
`~xnetcdf.Group.groups` attribute that returns the `xnetcdf.Group`
objects defined in the current group.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> g = nc['/forecast']  # Select a group
   >>> g
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> g.groups  # Get the groups defined in the this group
   {'model': model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>}

.. _Group-variables:

Group variables
---------------

The variables of an `xnetcdf.Group` instance are accessed with the
`~xnetcdf.Group.variables` attribute that returns the
`xnetcdf.Variable` objects defined in the current group.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> g = nc['/forecast']  # Select a group
   >>> g
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> g.variables  # Get the variables defined in the this group
   {'lon_bnds': lon_bnds: <xnetcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>,
    'lon': lon: <xnetcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>}

.. _Group-dimensions:

Group dimensions
----------------

The dimensions of an `xnetcdf.Group` instance are accessed with the
`~xnetcdf.Group.dimensions` attribute that returns the
`xnetcdf.Dimension` objects defined in the current group.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Group('test.nc')  # Open the dataset
   >>> g = nc['/forecast']  # Select a group
   >>> g
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> nc.dimensions  # Get the dimensions defined in the root group
   {'lon': lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>}
