NetCDF Dataset
==============

The examples on this page use the ``test.nc`` dataset
(`download 28 KB
<https://raw.githubusercontent.com/davidhassell/xnetcdf/main/tests/data/test.nc>`_).

.. _Dataset-definition:

Dataset definition
------------------

The original dataset definition used to instantiate an
`xnetcdf.Dataset` is available with the `~xnetcdf.Dataset.dataset`
attribute, and the name of the dataset is accessed with the
`~xnetcdf.Dataset.dataset_name` attribute.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.dataset
   'test.nc'
   >>> nc.dataset_name
   'test.nc'

.. code-block:: python
   :caption: Example

   >>> import fsspec
   >>> import xnetcdf
   >>> file_like = fsspec.filesystem('file').open('tests/data/test.nc', 'rb')
   >>> nc = xnetcdf.Dataset(file_like)
   >>> nc.dataset
   <fsspec.implementations.local.LocalFileOpener at 0x77dd401ab1f0>
   >>> nc.dataset is fh
   True
   >>> nc.dataset_name
   'test.nc'

.. _Dataset-backend:

Dataset backend
---------------

The backend library and and the backend object that is accessing the
dataset are availabl via the `xnetcdf.Dataset` attributes
`~xnetcdf.Dataset.backend_library` and
`~xnetcdf.Dataset.backend_accessor` repsectively.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.backend_library
   <module 'pyfive' from 'pyfive/pyfive/__init__.py'>
   >>> nc.backend_accessor
   <HDF5 file "test.nc" (mode r)>

A log of which backend libraries were used, successfully or
unsuccessfuly, to read the data set is available with the
`~xnetcdf.Dataset.dataset_read_log` method.
   
.. _Dataset-indexing:

Dataset indexing
----------------

A group or variable object, anywhere in the group hierarchy, can be
accessed by indexing an `xnetcdf.Dataset` instance with the object's
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
   >>> nc.attrs  # Get the attributes
   >>> nc['forecast']
   forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
   >>> nc['forecast/model']
   model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
   >>> nc['time']
   time: <xnetcdf.Variable: /time, shape=(), dimensions=()>
   >>> nc['forecast/lon']
   lon: <xnetcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
   >>> nc['forecast/model/q']
   q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
   >>> nc['time'] is nc['/time'] is nc['./time'] is nc['forecast/../time']
   True
   >>> nc['forecast'] is nc['/forecast/model/..']
   True
   >>> nc['./forecast/lon'] is nc['/forecast//model/../lon']
   True

.. _Dataset-attributes:

Dataset attributes
------------------

The attributes of an `xnetcdf.Dataset` instance are accessed with the
`~xnetcdf.Dataset.attrs` attribute.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.attrs  # Get the attributes
   {'Conventions': 'CF-1.13',
    'global_attr_1': np.float64(3.14),
    'global_attr_2': 'foo'}

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

.. _Dataset-groups:

Dataset groups
--------------

The groups of an `xnetcdf.Dataset` instance are accessed with the
`~xnetcdf.Dataset.groups` and `~xnetcdf.Dataset.all_groups`
attributes. The former returns the the `xnetcdf.Group` objects defined
in the root group, and the latter returns all `xnetcdf.Group` objects
wherever they appear in the group hierarchy.

.. code-block:: python

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.groups  # Get the groups defined in the root group
   {'forecast': forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>}
   >>> nc.all_groups  # Get all groups
   {'/': /home/david/xnetcdf/tests/data/test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>,
    '/forecast': forecast: <xnetcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>,
    '/forecast/model': model: <xnetcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>}

.. _Dataset-variables:

Dataset variables
-----------------

The variables of an `xnetcdf.Dataset` instance are accessed with the
`~xnetcdf.Dataset.variables` and `~xnetcdf.Dataset.all_variables`
attributes. The former returns the `xnetcdf.Variable` objects defined
in the root group, and the latter returns all `xnetcdf.Variable`
objects wherever they appear in the group hierarchy.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.variables  # Get the variables defined in the root group
   {'time': time: <xnetcdf.Variable: /time, shape=(), dimensions=()>}
   >>> nc.all_variables  # Get all variables
   {'/time': time: <xnetcdf.Variable: /time, shape=(), dimensions=()>,
    '/forecast/lon_bnds': lon_bnds: <xnetcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>,
    '/forecast/lon': lon: <xnetcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>,
    '/forecast/model/lat_bnds': lat_bnds: <xnetcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>,
    '/forecast/model/lat': lat: <xnetcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>,
    '/forecast/model/q': q: <xnetcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>}

.. _Dataset-dimensions:

Dataset dimensions
------------------

The dimensions of an `xnetcdf.Dataset` instance are accessed with the
`~xnetcdf.Dataset.dimensions` and `~xnetcdf.Dataset.all_dimensions`
attributes. The former returns the `xnetcdf.Dimension` objects defined
in the root group, and the latter returns all `xnetcdf.Dimension`
objects wherever they appear in the group hierarchy.

.. code-block:: python
   :caption: Example

   >>> import xnetcdf
   >>> nc = xnetcdf.Dataset('test.nc')  # Open the dataset
   >>> nc
   test.nc: <xnetcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
   >>> nc.dimensions  # Get the dimensions defined in the root group
   {'bounds2': bounds2: <xnetcdf.Dimension: /bounds2, size=2>}
   >>> nc.all_dimensions  # Get all dimensions		
   {'/bounds2': bounds2: <xnetcdf.Dimension: /bounds2, size=2>,
    '/forecast/lon': lon: <xnetcdf.Dimension: /forecast/lon, size=8, unlimited>,
    '/forecast/model/lat': lat: <xnetcdf.Dimension: /forecast/model/lat, size=5>}
