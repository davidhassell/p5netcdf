import fsspec
import netCDF4
import numpy as np
import pyfive
import pytest
import xarray

import p5netcdf


def test_p5netcdf_attributes(data_dir):
    """Check that attributes are parsed correctly."""
    dataset = data_dir / "test.nc"
    with (
        netCDF4.Dataset(dataset) as n,
        p5netcdf.Dataset(dataset, backend="pyfive") as p,
    ):
        nq = n["/forecast/model/q"]
        pq = p["/forecast/model/q"]

        assert sorted(pq.attrs) == sorted(nq.ncattrs())

        for attr, pvalue in pq.attrs.items():
            nvalue = nq.getncattr(attr)

            assert type(pvalue) is type(nvalue)

            if isinstance(pvalue, (np.ndarray, np.integer, np.floating)):
                assert pvalue.dtype == nvalue.dtype
                assert np.allclose(pvalue, nvalue)
            else:
                assert pvalue == nvalue


def test_p5netcdf_dimensions(data_dir):
    """Check that dimensions are parsed correctly."""
    dataset = data_dir / "test.nc"
    with (
        netCDF4.Dataset(dataset) as n,
        p5netcdf.Dataset(dataset, backend="pyfive") as p,
    ):
        for group in ("/", "/forecast", "/forecast/model"):
            pg = p[group]
            ng = n if group == "/" else n[group]

            assert set(ng.dimensions) == set(pg.dimensions)

            for name, pdim in pg.dimensions.items():
                ndim = ng.dimensions[name]
                assert pdim.isunlimited() == ndim.isunlimited()
                assert pdim.group().path == ndim.group().path

                for attr in ("name", "size"):
                    assert getattr(pdim, attr) == getattr(ndim, attr)


def test_p5netcdf_variables(data_dir):
    """Check that variables are parsed correctly."""
    dataset = data_dir / "test.nc"
    with (
        netCDF4.Dataset(dataset) as n,
        p5netcdf.Dataset(dataset, backend="pyfive") as p,
    ):
        for group in ("/", "/forecast", "/forecast/model"):
            pg = p[group]
            ng = n if group == "/" else n[group]

            assert set(ng.variables) == set(pg.variables)

            for name, pvar in pg.variables.items():
                nvar = ng.variables[name]

                assert pvar.chunking() == nvar.chunking()
                assert len(pvar.get_dims()) == len(nvar.get_dims())
                assert np.ma.allclose(pvar[...], nvar[...])

                if pvar.shape:
                    assert len(pvar) == len(nvar)
                else:
                    with pytest.raises(TypeError):
                        len(pvar)

                for attr in (
                    "name",
                    "size",
                    "shape",
                    "ndim",
                    "dtype",
                    "dimensions",
                ):
                    assert getattr(pvar, attr) == getattr(nvar, attr)

                for pdim, ndim in zip(*(pvar.get_dims(), nvar.get_dims())):
                    assert pdim.name == ndim.name
                    assert pdim.group().path == ndim.group().path


def test_p5netcdf_groups(data_dir):
    """Check that groups are parsed correctly."""
    dataset = data_dir / "test.nc"
    with (
        netCDF4.Dataset(dataset) as n,
        p5netcdf.Dataset(dataset, backend="pyfive") as p,
    ):
        for group in ("/", "/forecast", "/forecast/model"):
            pg = p[group]
            ng = n if group == "/" else n[group]

            pattrs = pg.attrs
            nattrs = {k: ng.getncattr(k) for k in ng.ncattrs()}
            assert pattrs == nattrs
            assert pg.path == ng.path


def test_p5netcdf_Dataset_file_like(data_dir):
    """Check Dataset with a file-like input."""
    dataset = data_dir / "test.nc"
    file_like = fsspec.filesystem("local").open(dataset, "rb")

    with p5netcdf.Dataset(file_like) as pfl, p5netcdf.Dataset(dataset) as p:
        assert (
            pfl["forecast/model/q"].dimensions
            == p["forecast/model/q"].dimensions
        )


def test_p5netcdf_Dataset_pyfive_like(data_dir):
    """Check Dataset with a pyfive.File input."""
    dataset = data_dir / "test.nc"
    py5_file = pyfive.File(dataset)
    with p5netcdf.Dataset(py5_file) as py5, p5netcdf.Dataset(dataset) as p:
        assert (
            py5["forecast/model/q"].dimensions
            == p["forecast/model/q"].dimensions
        )


def test_p5netcdf_Dataset_xarray_like(data_dir):
    """Check Dataset with an xarray.DataTree input."""
    dataset = data_dir / "test.nc"
    xr_dataset = xarray.open_datatree(
        dataset, mask_and_scale=False, decode_cf=False
    )
    with p5netcdf.Dataset(xr_dataset) as x, p5netcdf.Dataset(dataset) as p:
        # Verify it works correctly
        assert x.backend == "xarray"
        assert (
            x["forecast/model/q"].dimensions
            == p["forecast/model/q"].dimensions
        )

        # Test that we can access the same data
        assert np.array_equal(
            x["forecast/model/q"][...], p["forecast/model/q"][...]
        )

        # Test attributes are preserved
        assert (
            x["forecast/model/q"].attrs["standard_name"] == "specific_humidity"
        )


def test_p5netcdf_Dataset__repr__(data_dir):
    """Test Dataset.__repr__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            repr(p)
            == f"<p5netcdf.Dataset: {p.filename}, 1 dimension, 1 variable, 1 group>"
        )


def test_p5netcdf_Dataset__str__(data_dir):
    """Test Dataset.__str__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            str(p)
            == f"""<p5netcdf.Dataset: {p.filename}, 1 dimension, 1 variable, 1 group>
    Dimensions:
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
    Groups:
        forecast: <p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>"""
        )


def test_p5netcdf_Dataset_bad_file():
    """Test Dataset with not a netCDF file."""
    with pytest.raises(Exception):
        p5netcdf.Dataset(3.14)


def test_p5netcdf_Dataset_backend_selection(data_dir):
    """Test Dataset with specific backend selection."""
    dataset = data_dir / "test.nc"
    # Test single backend
    with p5netcdf.Dataset(dataset, backend="pyfive") as p:
        assert p.backend == "pyfive"

    # Test backend list
    with p5netcdf.Dataset(dataset, backend=["pyfive", "netCDF4"]) as p:
        assert p.backend == "pyfive"

    # Test invalid backend
    with pytest.raises(ValueError):
        p5netcdf.Dataset(dataset, backend="invalid_backend")


def test_p5netcdf_Dataset_verbose(data_dir):
    """Test Dataset with verbose output."""
    dataset = data_dir / "test.nc"

    for v in (0, 1, -1):
        with p5netcdf.Dataset(dataset, verbose=v) as _:
            # Should not raise an error
            pass


def test_p5netcdf_Dataset_dump(data_dir):
    """Test Dataset.dump."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            p.dump(display=False)
            == f"""<p5netcdf.Dataset: {p.filename}, 1 dimension, 1 variable, 1 group>
    Attributes:
        Conventions: 'CF-1.13'
        global_attr_1: np.float64(3.14)
        global_attr_2: 'foo'
    Dimensions:
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                units: 'days since 2018-12-01'
                standard_name: 'time'
    Groups:
        <p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
            Dimensions:
                lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
            Variables:
                lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>
                lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
                    Attributes:
                        units: 'degrees_east'
                        standard_name: 'longitude'
                        bounds: '/forecast/lon_bnds'
            Groups:
                <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
                    Attributes:
                        group_attr_1: np.int64(12)
                        group_attr_2: 'bar'
                    Dimensions:
                        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
                    Variables:
                        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
                        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                            Attributes:
                                units: 'degrees_north'
                                standard_name: 'latitude'
                                bounds: '/forecast/model/lat_bnds'
                        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                            Attributes:
                                list7: array([2, 3])
                                int: np.int64(49)
                                int8: np.int8(49)
                                int16: np.int16(49)
                                int32: np.int32(49)
                                int64: np.int64(49)
                                float: np.float64(49.0)
                                float32: np.float32(49.0)
                                float64: np.float64(49.0)
                                uint8: np.uint8(49)
                                uint16: np.uint16(49)
                                uint32: np.uint32(49)
                                uint64: np.uint64(49)
                                list1: array([2, 3], dtype=int8)
                                list2: array([2, 3], dtype=int16)
                                list3: array([2, 3])
                                list4: array([2, 3], dtype=int32)
                                list5: array([2., 3.], dtype=float32)
                                list6: array([2., 3.])
                                list8: np.int32(2)
                                list9: array([], dtype=int32)
                                list10: array([], dtype=float64)
                                list11: ['a', 'bb', 'ccc']
                                list12: ['a', '1', '2.5']
                                list13: 'a'
                                list14: ['a', 'bb']
                                string1: '1'
                                string2: 'a'
                                string3: 'kg m-2'
                                string4: ''
                                string5: ' '
                                string6: ''
                                string7: ''
                                string8: ''
                                string9: ''
                                coordinates: 'time'
                                cell_methods: 'area: mean'
                                standard_name: 'specific_humidity'"""
        )


def test_p5netcdf_Dataset_close(data_dir):
    """Test Dataset.close."""
    dataset = data_dir / "test.nc"
    p = p5netcdf.Dataset(dataset, backend="pyfive")
    assert not p._grp._fh.closed
    p.close()
    assert p._grp._fh.closed

    py5 = pyfive.File(dataset)
    p = p5netcdf.Dataset(py5)
    assert not p._grp._fh.closed
    p.close()
    assert not p._grp._fh.closed


def test_p5netcdf_Dataset_filename(data_dir):
    """Test Dataset.filename."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p.filename == str(dataset)


def test_p5netcdf_Dataset_ncdump(data_dir):
    """Test Dataset.ncdump."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        cdl = p.ncdump(display=False)
        assert isinstance(cdl, str)
        assert "netcdf" in cdl
        assert "dimensions:" in cdl
        assert "variables:" in cdl
        assert "bounds2 = 2" in cdl
        assert "time" in cdl
        assert "forecast" in cdl


def test_p5netcdf_Dataset_cache_metadata(data_dir):
    """Test Dataset.cache_metadata."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        # Test maximal caching
        p.cache_structural_metadata("maximal")

        # Test minimal caching
        p.cache_structural_metadata("minimal")

        # Test invalid strategy
        with pytest.raises(ValueError):
            p.cache_structural_metadata("invalid")


def test_p5netcdf_Dataset_getncattr(data_dir):
    """Test Dataset.getncattr."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p.getncattr("global_attr_1") == 3.14

    # Test non-existing attribute should raise AttributeError
    with pytest.raises(AttributeError):
        p.getncattr("nonexistent_attr")


def test_p5netcdf_Dataset_library(data_dir):
    """Test Dataset.library."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="pyfive") as p:
        assert p.library is pyfive


def test_p5netcdf_Dataset_all_properties(data_dir):
    """Test Dataset.all_dimensions, all_variables, all_groups."""
    # Test all_dimensions
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        all_dims = p.all_dimensions
        assert isinstance(all_dims, dict)
        assert "/bounds2" in all_dims
        assert "/forecast/lon" in all_dims
        assert "/forecast/model/lat" in all_dims

        # Test all_variables
        all_vars = p.all_variables
        assert isinstance(all_vars, dict)
        assert "/time" in all_vars
        assert "/forecast/lon" in all_vars
        assert "/forecast/model/q" in all_vars

        # Test all_groups
        all_groups = p.all_groups
        assert isinstance(all_groups, dict)
        assert "/" in all_groups
        assert "/forecast" in all_groups
        assert "/forecast/model" in all_groups


def test_p5netcdf_Dataset_protocol_is_local(data_dir):
    """Test Dataset.protocol and is_local properties."""
    # For local files
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p.protocol == "file"
        assert p.is_local

    # Test with fsspec file-like object
    file_like = fsspec.filesystem("local").open(dataset, "rb")
    with p5netcdf.Dataset(file_like) as p:
        assert p.protocol == "file"
        assert p.is_local


def test_p5netcdf_Dataset_dataset_open_log(data_dir):
    """Test Dataset.dataset_open_log."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        log = p.dataset_open_log(display=False)
        assert isinstance(log, str)
        assert "Successfully read" in log


def test_p5netcdf_Dataset_enter_exit(data_dir):
    """Test Dataset in context manager."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="pyfive") as p:
        assert p.attrs["global_attr_2"] == "foo"
        assert not p._grp._fh.closed

    assert p._grp._fh.closed

    py5 = pyfive.File(dataset)
    assert not py5._fh.closed
    with p5netcdf.Dataset(py5) as p:
        assert p.attrs["global_attr_2"] == "foo"

    assert not py5._fh.closed


def test_p5netcdf_Dimension__repr__(data_dir):
    """Test Dimension.__repr__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert repr(dim) == "<p5netcdf.Dimension: /bounds2, size=2>"

        dim = p["forecast"].dimensions["lon"]
        assert (
            repr(dim)
            == "<p5netcdf.Dimension: /forecast/lon, size=8, unlimited>"
        )


def test_p5netcdf_Dimension_size(data_dir):
    """Test Dimension.size."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert not dim.isunlimited()
        assert dim.size == 2

        dim = p["forecast"].dimensions["lon"]
        assert dim.isunlimited()
        assert len(dim) == 8


def test_p5netcdf_Dimension__len__(data_dir):
    """Test Dimension.__len__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert not dim.isunlimited()
        assert len(dim) == 2

        dim = p["forecast"].dimensions["lon"]
        assert dim.isunlimited()
        assert len(dim) == 8


def test_p5netcdf_Dimension_isunlimited(data_dir):
    """Test Dimension.isunlimited."""
    dataset = data_dir / "test.nc"
    print(dataset)
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert isinstance(dim.isunlimited(), bool)
        assert not dim.isunlimited()

        dim = p["forecast"].dimensions["lon"]
        assert isinstance(dim.isunlimited(), bool)
        assert dim.isunlimited()


def test_p5netcdf_Dimension_name(data_dir):
    """Test Dimension.name."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert dim.name == "bounds2"

        dim = p["forecast"].dimensions["lon"]
        assert dim.name == "lon"


def test_p5netcdf_Dimension_path(data_dir):
    """Test Dimension.path."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        dim = p.dimensions["bounds2"]
        assert dim.path == "/bounds2"

        dim = p["forecast"].dimensions["lon"]
        assert dim.path == "/forecast/lon"


def test_p5netcdf_Dimension_group(data_dir):
    """Test Dimension.group."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        dim = group.dimensions["bounds2"]
        assert dim.group() is group

        group = p["/forecast"]
        dim = group.dimensions["lon"]
        assert dim.group() is group

        group = p["/forecast/model"]
        dim = group.dimensions["lat"]
        assert dim.group() is group


def test_p5netcdf_Dimension_parent(data_dir):
    """Test Dimension.group."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        dim = group.dimensions["bounds2"]
        assert dim.parent is group

        group = p["/forecast"]
        dim = group.dimensions["lon"]
        assert dim.parent is group

        group = p["/forecast/model"]
        dim = group.dimensions["lat"]
        assert dim.parent is group


def test_p5netcdf_Dimension_backend(data_dir):
    """Test Dimension.backend."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="pyfive") as p:
        assert p.dimensions["bounds2"].backend == "pyfive"


def test_p5netcdf_Dimension_library(data_dir):
    """Test Dimension.library."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="pyfive") as p:
        assert p.dimensions["bounds2"].library is pyfive


def test_p5netcdf_Variable__repr__(data_dir):
    """Test Variable.__repr__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["time"]
        assert (
            repr(var) == "<p5netcdf.Variable: /time, shape=(), dimensions=()>"
        )

        var = p["forecast/lon"]
        assert (
            repr(var)
            == "<p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>"
        )

        var = p["/forecast/model/q"]
        assert (
            repr(var)
            == "<p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>"
        )


def test_p5netcdf_Variable_maxshape(data_dir):
    """Test Variable_maxshape."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["time"]
        assert var.maxshape == ()

        var = p["forecast/lon"]
        assert var.maxshape == (None,)

        var = p["forecast/lon_bnds"]
        assert var.maxshape == (None, 2)


def test_p5netcdf_Variable_name(data_dir):
    """Test Variable.name."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["time"]
        assert var.name == "time"

        var = p["/forecast/model/q"]
        assert var.name == "q"


def test_p5netcdf_Variable_path(data_dir):
    """Test Variable.path."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["time"]
        assert var.path == "/time"

        var = p["/forecast/model/q"]
        assert var.path == "/forecast/model/q"


def test_p5netcdf_Variable_chunking(data_dir):
    """Test Variable.chunking."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/lat"]
        assert var.chunking() == "contiguous"

        var = p["/forecast/model/q"]
        assert var.chunking() == [5, 3]


def test_p5netcdf_Variable_chunks(data_dir):
    """Test Variable.chunks."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/lat"]
        assert var.chunks is None

        var = p["/forecast/model/q"]
        assert var.chunks == (5, 3)


def test_p5netcdf_Variable_dtype(data_dir):
    """Test Variable.dtype."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.dtype == "int32"

        var = p["/forecast/lon"]
        assert var.dtype == "float64"

        var = p["/forecast/model/q"]
        assert var.dtype == "float32"


def test_p5netcdf_Variable_orthogonal_indexing(data_dir):
    """Test Variable.__orthogonal_indexing__ property."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/q"]
        assert isinstance(var.__orthogonal_indexing__, bool)


def test_p5netcdf_Variable_dimension_paths(data_dir):
    """Test Variable.dimension_paths property."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.dimension_paths == ()

        var = p["/forecast/lon"]
        assert var.dimension_paths == ("/forecast/lon",)

        var = p["/forecast/model/q"]
        assert var.dimension_paths == ("/forecast/model/lat", "/forecast/lon")


def test_p5netcdf_Variable_shards(data_dir):
    """Test Variable.shards property."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/q"]
        # For non-zarr datasets, shards should be None
        assert var.shards is None


def test_p5netcdf_Variable_ndim(data_dir):
    """Test Variable.ndim."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        var.ndim == 0

        var = p["/forecast/lon"]
        assert var.ndim == 1

        var = p["/forecast/model/q"]
        assert var.ndim == 2


def test_p5netcdf_Variable_shape(data_dir):
    """Test Variable.shape."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.shape == ()

        var = p["/forecast/lon"]
        assert var.shape == (8,)

        var = p["/forecast/model/q"]
        assert var.shape == (5, 8)


def test_p5netcdf_Variable_size(data_dir):
    """Test Variable.size."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.size == 1

        var = p["/forecast/lon"]
        assert var.size == 8

        var = p["/forecast/model/q"]
        assert var.size == 40


def test_p5netcdf_Variable__len__(data_dir):
    """Test Variable.__len__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        with pytest.raises(TypeError):
            len(var)

        var = p["/forecast/lon"]
        assert len(var) == 8

        var = p["/forecast/model/q"]
        assert len(var) == 5


def test_p5netcdf_Variable_dimensions(data_dir):
    """Test Variable.dimensions."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.dimensions == ()

        var = p["/forecast/lon"]
        assert var.dimensions == ("lon",)

        var = p["/forecast/model/q"]
        assert var.dimensions == ("lat", "lon")


def test_p5netcdf_Variable_get_dims(data_dir):
    """Test Variable.__len__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.get_dims() == ()

        var = p["/forecast/lon"]
        assert len(var.get_dims()) == 1
        assert var.get_dims() == (p["/forecast"].dimensions["lon"],)

        var = p["/forecast/model/q"]
        assert len(var.get_dims()) == 2
        assert var.get_dims() == (
            p["/forecast/model"].dimensions["lat"],
            p["/forecast"].dimensions["lon"],
        )


def test_p5netcdf_Variable_parent(data_dir):
    """Test Variable.parent."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.parent is p

        var = p["/forecast/lon"]
        assert var.parent is p["/forecast"]

        var = p["/forecast/model/q"]
        assert var.parent is p["/forecast/model"]


def test_p5netcdf_Variable_group(data_dir):
    """Test Variable.group."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/time"]
        assert var.group() is p

        var = p["/forecast/lon"]
        assert var.group() is p["/forecast"]

        var = p["/forecast/model/q"]
        var.group() is p["/forecast/model"]


def test_p5netcdf_Variable_getValue(data_dir):
    """Test Variable.getValue."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        # Test scalar variable
        var = p["/time"]
        assert var.getValue() == 31

        # Test non-scalar variable should raise IndexError
        var = p["/forecast/lon"]
        with pytest.raises(IndexError):
            var.getValue()


def test_p5netcdf_Variable_getncattr(data_dir):
    """Test Variable.getncattr."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/q"]

        # Test existing attribute
        assert var.getncattr("standard_name") == "specific_humidity"
        assert var.getncattr("int") == 49

        # Test non-existing attribute should raise AttributeError
        with pytest.raises(AttributeError):
            var.getncattr("nonexistent_attr")


def test_p5netcdf_Variable_ncattrs(data_dir):
    """Test Variable.ncattrs."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        var = p["/forecast/model/q"]
        attrs = var.ncattrs()
        assert isinstance(attrs, list)
        assert "standard_name" in attrs
        assert "int" in attrs
        assert set(attrs) == set(var.attrs.keys())


def test_p5netcdf_Group__repr__(data_dir):
    """Test Group.__repr__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            repr(p["/forecast"])
            == "<p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>"
        )

        assert (
            repr(p["/forecast/model"])
            == "<p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>"
        )


def test_p5netcdf_Group__str__(data_dir):
    """Test Group.__str__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            str(p["/forecast"])
            == """<p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
    Dimensions:
        lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
    Variables:
        lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>
        lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
    Groups:
        model: <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>"""
        )

        assert (
            str(p["/forecast/model"])
            == """<p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
    Dimensions:
        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
    Variables:
        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>"""
        )


def test_p5netcdf_Group_dump(data_dir):
    """Test Group.dump."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert (
            p["/forecast"].dump(display=False)
            == """<p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
    Dimensions:
        lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
    Variables:
        lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>
        lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
            Attributes:
                units: 'degrees_east'
                standard_name: 'longitude'
                bounds: '/forecast/lon_bnds'
    Groups:
        <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
            Attributes:
                group_attr_1: np.int64(12)
                group_attr_2: 'bar'
            Dimensions:
                lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
            Variables:
                lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
                lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                    Attributes:
                        units: 'degrees_north'
                        standard_name: 'latitude'
                        bounds: '/forecast/model/lat_bnds'
                q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                    Attributes:
                        list7: array([2, 3])
                        int: np.int64(49)
                        int8: np.int8(49)
                        int16: np.int16(49)
                        int32: np.int32(49)
                        int64: np.int64(49)
                        float: np.float64(49.0)
                        float32: np.float32(49.0)
                        float64: np.float64(49.0)
                        uint8: np.uint8(49)
                        uint16: np.uint16(49)
                        uint32: np.uint32(49)
                        uint64: np.uint64(49)
                        list1: array([2, 3], dtype=int8)
                        list2: array([2, 3], dtype=int16)
                        list3: array([2, 3])
                        list4: array([2, 3], dtype=int32)
                        list5: array([2., 3.], dtype=float32)
                        list6: array([2., 3.])
                        list8: np.int32(2)
                        list9: array([], dtype=int32)
                        list10: array([], dtype=float64)
                        list11: ['a', 'bb', 'ccc']
                        list12: ['a', '1', '2.5']
                        list13: 'a'
                        list14: ['a', 'bb']
                        string1: '1'
                        string2: 'a'
                        string3: 'kg m-2'
                        string4: ''
                        string5: ' '
                        string6: ''
                        string7: ''
                        string8: ''
                        string9: ''
                        coordinates: 'time'
                        cell_methods: 'area: mean'
                        standard_name: 'specific_humidity'"""
        )

        assert (
            p["/forecast/model"].dump(display=False)
            == """<p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
    Attributes:
        group_attr_1: np.int64(12)
        group_attr_2: 'bar'
    Dimensions:
        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
    Variables:
        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
            Attributes:
                units: 'degrees_north'
                standard_name: 'latitude'
                bounds: '/forecast/model/lat_bnds'
        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
            Attributes:
                list7: array([2, 3])
                int: np.int64(49)
                int8: np.int8(49)
                int16: np.int16(49)
                int32: np.int32(49)
                int64: np.int64(49)
                float: np.float64(49.0)
                float32: np.float32(49.0)
                float64: np.float64(49.0)
                uint8: np.uint8(49)
                uint16: np.uint16(49)
                uint32: np.uint32(49)
                uint64: np.uint64(49)
                list1: array([2, 3], dtype=int8)
                list2: array([2, 3], dtype=int16)
                list3: array([2, 3])
                list4: array([2, 3], dtype=int32)
                list5: array([2., 3.], dtype=float32)
                list6: array([2., 3.])
                list8: np.int32(2)
                list9: array([], dtype=int32)
                list10: array([], dtype=float64)
                list11: ['a', 'bb', 'ccc']
                list12: ['a', '1', '2.5']
                list13: 'a'
                list14: ['a', 'bb']
                string1: '1'
                string2: 'a'
                string3: 'kg m-2'
                string4: ''
                string5: ' '
                string6: ''
                string7: ''
                string8: ''
                string9: ''
                coordinates: 'time'
                cell_methods: 'area: mean'
                standard_name: 'specific_humidity'"""
        )


def test_p5netcdf_Group__getitem__(data_dir):
    """Test Group.__getitem__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p[""] is p
        assert p["/"] is p
        assert p["//"] is p
        assert p["/."] is p
        assert p["."] is p
        assert p["./"] is p
        assert p["./."] is p
        assert p["/./."] is p
        assert p["/././"] is p
        assert p["forecast"] is p["/forecast"]
        assert p["forecast"] is p["/forecast/"]
        assert p["forecast/model"] is p["forecast"]["model"]
        assert p["/forecast/model/"] is p["/forecast"]["model/"]
        assert p["forecast"]["/forecast/model/"] is p["/forecast/model"]
        assert p["forecast"]["/"] is p["/"]
        assert p["forecast"][""] is p["/forecast"]
        assert p["forecast"]["."] is p["/forecast"]
        assert p["forecast"]["./"] is p["/forecast"]
        assert p["forecast"]["/forecast"] is p["/forecast"]
        assert p["forecast"]["/forecast/model/q"] is p["/forecast/model/q"]
        assert p["/forecast/model/q/"] is p["/forecast/model/q"]
        assert p["/forecast//model///q////"] is p["/forecast/model/q"]
        assert p["/forecast/model/q"] is p["/forecast"]["model"]["q"]
        assert p["forecast/.."] is p["/"]
        assert p["/forecast/.."] is p["/"]
        assert p["/forecast/./.."] is p["/"]
        assert p["./forecast/./.."] is p["/"]
        assert p["./forecast/./../forecast/model/.."] is p["/forecast"]
        assert p["/forecast"][""] is p["/forecast"]
        assert p["/forecast"]["."] is p["/forecast"]
        assert p["/forecast"]["./"] is p["/forecast"]
        assert p["/forecast"][".."] is p
        assert p["/forecast"]["../"] is p

        # Test bad paths from the root group
        current_group = p["/"]
        for bad_group in (
            "/..",
            "./..",
            "/bad_group",
            "bad_group",
            "/forecast/bad_group",
            "/forecast/model/q/subgroup",
            "/forecast/model/q/..",
            "/forecast/model/q/.",
            "/forecast/model/q/./",
        ):
            with pytest.raises(KeyError):
                current_group[bad_group]

        # Test bad paths from a sub-group
        current_group = p["/forecast"]
        for bad_group in (
            "../..",
            "./../..",
            "../bad_group",
            "../model/.././bad_group",
            "/bad_group",
            "bad_group",
            "/forecast/bad_group",
            "/forecast/model/q/subgroup",
            "/forecast/model/q/..",
            "/forecast/model/q/.",
            "/forecast/model/q/./",
            "model/bad_group",
            "model/q/subgroup",
        ):
            with pytest.raises(KeyError):
                current_group[bad_group]


def test_p5netcdf_Group__iter__(data_dir):
    """Test Group.__iter__."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert tuple(group) == ("forecast", "time")

        group = p["/forecast"]
        assert tuple(group) == ("model", "lon_bnds", "lon")

        group = p["/forecast/model"]
        assert tuple(group) == ("lat_bnds", "lat", "q")


def test_p5netcdf_Group_keys(data_dir):
    """Test Group.keys."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert tuple(group.keys()) == ("forecast", "time")

        group = p["/forecast"]
        assert tuple(group.keys()) == ("model", "lon_bnds", "lon")

        group = p["/forecast/model"]
        assert tuple(group.keys()) == ("lat_bnds", "lat", "q")


def test_p5netcdf_Group_values(data_dir):
    """Test Group.values."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert tuple(group.values()) == (group["forecast"], group["time"])

        group = p["/forecast"]
        assert tuple(group.values()) == (
            group["model"],
            group["lon_bnds"],
            group["lon"],
        )

        group = p["/forecast/model"]
        assert tuple(group.values()) == (
            group["lat_bnds"],
            group["lat"],
            group["q"],
        )


def test_p5netcdf_Group_items(data_dir):
    """Test Group.items."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert tuple(group.items()) == (
            ("forecast", group["forecast"]),
            ("time", group["time"]),
        )

        group = p["/forecast"]
        assert tuple(group.items()) == (
            ("model", group["model"]),
            ("lon_bnds", group["lon_bnds"]),
            ("lon", group["lon"]),
        )

        group = p["/forecast/model"]
        assert tuple(group.items()) == (
            ("lat_bnds", group["lat_bnds"]),
            ("lat", group["lat"]),
            ("q", group["q"]),
        )


def test_p5netcdf_Group_name(data_dir):
    """Test Group.name."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert group.name == ""

        group = p["/forecast"]
        assert group.name == "forecast"

        group = p["/forecast/model"]
        assert group.name == "model"


def test_p5netcdf_Group_path(data_dir):
    """Test Group.path."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        for path in ("/", "/forecast", "/forecast/model"):
            group = p[path]
            assert group.path == path


def test_p5netcdf_Group_parent(data_dir):
    """Test Group.parent."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        group = p
        assert group.parent is None

        group = p["/forecast"]
        assert group.parent is p

        group = p["/forecast/model"]
        assert group.parent is p["/forecast"]


def test_p5netcdf_Group_is_sub_group(data_dir):
    """Test Group.is_sub_group."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p.is_sub_group(p)
        assert p["forecast"].is_sub_group(p["forecast"])
        assert p["forecast"].is_sub_group(p)
        assert p["forecast/model"].is_sub_group(p)
        assert p["forecast/model"].is_sub_group(p["forecast"])

        assert not p.is_sub_group(p["forecast"])
        assert not p.is_sub_group(p["forecast/model"])
        assert not p["forecast"].is_sub_group(p["forecast/model"])


def test_p5netcdf_Group_is_ancestor_group(data_dir):
    """Test Group.is_ancestor_group."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        assert p.is_ancestor_group(p)
        assert p.is_ancestor_group(p["forecast"])
        assert p.is_ancestor_group(p["forecast/model"])
        assert p["forecast"].is_ancestor_group(p["forecast"])
        assert p["forecast"].is_ancestor_group(p["forecast/model"])

        assert not p["forecast"].is_ancestor_group(p)
        assert not p["forecast/model"].is_ancestor_group(p)
        assert not p["forecast/model"].is_ancestor_group(p["forecast"])


def test_p5netcdf_zarr_backend(data_dir):
    """Test Zarr backend functionality."""
    dataset = data_dir / "test.zarr3"
    with p5netcdf.Dataset(dataset) as p:
        assert p.backend == "zarr"
        # Test that basic operations work
        assert isinstance(p.dimensions, dict)
        assert isinstance(p.variables, dict)


def test_p5netcdf_kerchunk_backend(data_dir):
    """Test Kerchunk backend functionality."""
    dataset = str(data_dir / "test.kerchunk")
    mapper = fsspec.filesystem("reference", fo=dataset).get_mapper()
    with p5netcdf.Dataset(mapper) as p:
        assert p.backend == "zarr"
        # Test that basic operations work
        assert isinstance(p.dimensions, dict)
        assert isinstance(p.variables, dict)


def test_p5netcdf_zarr_dimension_search(data_dir):
    """Test zarr_dimension_search parameter."""
    dataset = data_dir / "test.zarr3"
    # Test different search strategies
    for strategy in ["closest_ancestor", "furthest_ancestor", "local"]:
        with p5netcdf.Dataset(dataset, zarr_dimension_search=strategy) as p:
            assert p.backend == "zarr"


def test_p5netcdf_Group_getncattr(data_dir):
    """Test Group.getncattr."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        # Test root group attributes
        assert p.getncattr("global_attr_1") == 3.14

        # Test subgroup attributes
        model_group = p["/forecast/model"]
        assert model_group.getncattr("group_attr_1") == 12
        assert model_group.getncattr("group_attr_2") == "bar"

        # Test non-existing attribute should raise AttributeError
        with pytest.raises(AttributeError):
            p.getncattr("nonexistent_attr")


def test_p5netcdf_Group_ncattrs(data_dir):
    """Test Group.ncattrs."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        # Test root group
        attrs = p.ncattrs()
        assert isinstance(attrs, list)
        assert "Conventions" in attrs
        assert "global_attr_1" in attrs
        assert set(attrs) == set(p.attrs.keys())

        # Test subgroup
        model_group = p["/forecast/model"]
        attrs = model_group.ncattrs()
        assert "group_attr_1" in attrs
        assert "group_attr_2" in attrs
        assert set(attrs) == set(model_group.attrs.keys())


def test_p5netcdf_edge_cases(data_dir):
    """Test various edge cases and error conditions."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset) as p:
        # Test Group.__len__
        assert len(p) == 2  # forecast group + time variable
        assert len(p["/forecast"]) == 3  # model group + 2 variables

        # Test Group.get() method (inherited from Mapping)
        assert p.get("time") is p["time"]
        assert p.get("nonexistent") is None
        assert p.get("nonexistent", "default") == "default"

        # Test Variable array access with different indices
        var = p["/forecast/lon"]
        assert var[0] == 22.5
        assert np.array_equal(var[:2], [22.5, 67.5])

        # Test scalar variable indexing
        time_var = p["/time"]
        assert time_var[()] == 31
