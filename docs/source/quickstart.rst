Getting Started
===============

Installation
------------

p5netcdf can be installed using ``pip`` using the command:

.. code-block:: console

    pip install p5netcdf

or, to also install all of the backend libraries:

.. code-block:: console

    pip install p5netcdf[all]

``conda`` packages, which also install all of the backend libraries, are
also available from conda-forge:

.. code-block:: console

    conda install -c conda-forge p5netcdf

To install from source in your home directory use:

.. code-block:: console

    pip install --user ./p5netcdf

The library can also be imported directly from the ``p5netcdf`` source
root directory:

.. code-block:: console

    pip install -e . 

Usage
-----

Here is a simple example of how to use ``p5netcdf`` to open a netCDF file and inspect its contents:

.. code-block:: python

    import p5netcdf

    # Open a netCDF file (replace with a path to your file)
    with p5netcdf.Dataset('path/to/your/file.nc') as nc:
        # Print a summary of the dataset
        print(nc)

        # Use the dump() method for a detailed view
        nc.dump()

        # Access a variable
        if 'temperature' in nc.variables:
            temp_var = nc.variables['temperature']
            print(temp_var)

            # Read data from the variable
            data = temp_var[:]
            print(data.shape)
