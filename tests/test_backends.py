import fsspec
import numpy as np
import pyfive
import xarray as xr

import p5netcdf


def test_p5netcdf_netCDF4(data_dir):
    """Test netCDF4 functionality."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend='netCDF4') as p:
        assert p.backend == "netCDF4"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
    Attributes:
        Conventions: 'CF-1.13'
        global_attr_1: np.float64(3.14)
        global_attr_2: 'foo'
    Dimensions:
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'
    Groups:
        forecast: <p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
            Dimensions:
                lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
            Variables:
                lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>
                lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
                    Attributes:
                        bounds: '/forecast/lon_bnds'
                        standard_name: 'longitude'
                        units: 'degrees_east'
            Groups:
                model: <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
                    Attributes:
                        group_attr_1: np.int64(12)
                        group_attr_2: 'bar'
                    Dimensions:
                        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
                    Variables:
                        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
                        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                            Attributes:
                                bounds: '/forecast/model/lat_bnds'
                                standard_name: 'latitude'
                                units: 'degrees_north'
                        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                            Attributes:
                                cell_methods: 'area: mean'
                                coordinates: 'time'
                                float: np.float64(49.0)
                                float32: np.float32(49.0)
                                float64: np.float64(49.0)
                                int: np.int64(49)
                                int16: np.int16(49)
                                int32: np.int32(49)
                                int64: np.int64(49)
                                int8: np.int8(49)
                                list1: array([2, 3], dtype=int8)
                                list10: array([], dtype=float64)
                                list11: ['a', 'bb', 'ccc']
                                list12: ['a', '1', '2.5']
                                list13: 'a'
                                list14: ['a', 'bb']
                                list2: array([2, 3], dtype=int16)
                                list3: array([2, 3])
                                list4: array([2, 3], dtype=int32)
                                list5: array([2., 3.], dtype=float32)
                                list6: array([2., 3.])
                                list7: array([2, 3])
                                list8: np.int32(2)
                                list9: array([], dtype=int32)
                                standard_name: 'specific_humidity'
                                string1: '1'
                                string2: 'a'
                                string3: 'kg m-2'
                                string4: ''
                                string5: ' '
                                string6: ''
                                string7: ''
                                string8: ''
                                string9: ''
                                uint16: np.uint16(49)
                                uint32: np.uint32(49)
                                uint64: np.uint64(49)
                                uint8: np.uint8(49)"""
        )


def test_p5netcdf_zarr3(data_dir):
    """Test Zarr3 functionality."""
    dataset = data_dir / "test.zarr3"
    with p5netcdf.Dataset(dataset) as p:
        assert p.backend == "zarr"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 0 dimensions, 1 variable, 1 group>
    Attributes:
        Conventions: 'CF-1.13'
        global_attr_1: 3.14
        global_attr_2: 'foo'
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'
    Groups:
        forecast: <p5netcdf.Group: /forecast, 2 dimensions, 2 variables, 1 group>
            Dimensions:
                lon: <p5netcdf.Dimension: /forecast/lon, size=8>
                bounds2: <p5netcdf.Dimension: /forecast/bounds2, size=2>
            Variables:
                lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
                    Attributes:
                        bounds: '/forecast/lon_bnds'
                        standard_name: 'longitude'
                        units: 'degrees_east'
                lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /forecast/bounds2)>
            Groups:
                model: <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
                    Attributes:
                        group_attr_1: 12
                        group_attr_2: 'bar'
                    Dimensions:
                        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
                    Variables:
                        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                            Attributes:
                                bounds: '/forecast/model/lat_bnds'
                                standard_name: 'latitude'
                                units: 'degrees_north'
                        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /forecast/bounds2)>
                        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                            Attributes:
                                cell_methods: 'area: mean'
                                coordinates: 'time'
                                float: 49.0
                                float32: 49.0
                                float64: 49.0
                                int: 49
                                int16: 49
                                int32: 49
                                int64: 49
                                int8: 49
                                list1: array([2, 3])
                                list10: []
                                list11: ['a', 'bb', 'ccc']
                                list12: ['a', '1', '2.5']
                                list13: 'a'
                                list14: ['a', 'bb']
                                list2: array([2, 3])
                                list3: array([2, 3])
                                list4: array([2, 3])
                                list5: array([2., 3.])
                                list6: array([2., 3.])
                                list7: array([2, 3])
                                list8: 2
                                list9: []
                                standard_name: 'specific_humidity'
                                string1: '1'
                                string2: 'a'
                                string3: 'kg m-2'
                                string4: ''
                                string5: ' '
                                string6: ''
                                string7: ''
                                string8: ''
                                string9: ''
                                uint16: 49
                                uint32: 49
                                uint64: 49
                                uint8: 49"""
        )


def test_p5netcdf_zarr2(data_dir):
    """Test Zarr2 functionality."""
    dataset = data_dir / "test1.zarr2"
    with p5netcdf.Dataset(dataset) as p:
        assert p.backend == "zarr"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 3 dimensions, 6 variables, 0 groups>
    Attributes:
        Conventions: 'CF-1.12'
    Dimensions:
        lat: <p5netcdf.Dimension: /lat, size=5>
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
        lon: <p5netcdf.Dimension: /lon, size=8>
    Variables:
        lat: <p5netcdf.Variable: /lat, shape=(5,), dimensions=(/lat,)>
            Attributes:
                bounds: 'lat_bnds'
                standard_name: 'latitude'
                units: 'degrees_north'
        lat_bnds: <p5netcdf.Variable: /lat_bnds, shape=(5, 2), dimensions=(/lat, /bounds2)>
        lon: <p5netcdf.Variable: /lon, shape=(8,), dimensions=(/lon,)>
            Attributes:
                bounds: 'lon_bnds'
                standard_name: 'longitude'
                units: 'degrees_east'
        lon_bnds: <p5netcdf.Variable: /lon_bnds, shape=(8, 2), dimensions=(/lon, /bounds2)>
        q: <p5netcdf.Variable: /q, shape=(5, 8), dimensions=(/lat, /lon)>
            Attributes:
                cell_methods: 'area: mean'
                coordinates: 'time'
                project: 'research'
                standard_name: 'specific_humidity'
                units: '1'
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'"""
        )


def test_p5netcdf_kerchunk(data_dir):
    """Test Kerchunk functionality."""
    dataset = str(data_dir / "test1.kerchunk")
    mapper = fsspec.filesystem("reference", fo=dataset).get_mapper()
    with p5netcdf.Dataset(mapper) as p:
        assert p.backend == "zarr"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 3 dimensions, 6 variables, 0 groups>
    Attributes:
        Conventions: 'CF-1.12'
    Dimensions:
        lat: <p5netcdf.Dimension: /lat, size=5>
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
        lon: <p5netcdf.Dimension: /lon, size=8>
    Variables:
        lat: <p5netcdf.Variable: /lat, shape=(5,), dimensions=(/lat,)>
            Attributes:
                bounds: 'lat_bnds'
                standard_name: 'latitude'
                units: 'degrees_north'
        lat_bnds: <p5netcdf.Variable: /lat_bnds, shape=(5, 2), dimensions=(/lat, /bounds2)>
        lon: <p5netcdf.Variable: /lon, shape=(8,), dimensions=(/lon,)>
            Attributes:
                bounds: 'lon_bnds'
                standard_name: 'longitude'
                units: 'degrees_east'
        lon_bnds: <p5netcdf.Variable: /lon_bnds, shape=(8, 2), dimensions=(/lon, /bounds2)>
        q: <p5netcdf.Variable: /q, shape=(5, 8), dimensions=(/lat, /lon)>
            Attributes:
                cell_methods: 'area: mean'
                coordinates: 'time'
                project: 'research'
                standard_name: 'specific_humidity'
                units: '1'
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'"""
        )


def test_p5netcdf_netcdf_file(data_dir):
    """Test Kerchunk functionality."""
    dataset = data_dir / "test1.nc3"
    with p5netcdf.Dataset(dataset, backend="netcdf_file") as p:
        assert p.backend == "netcdf_file"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 3 dimensions, 6 variables, 0 groups>
    Attributes:
        Conventions: 'CF-1.13'
    Dimensions:
        lat: <p5netcdf.Dimension: /lat, size=5>
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
        lon: <p5netcdf.Dimension: /lon, size=8>
    Variables:
        lat_bnds: <p5netcdf.Variable: /lat_bnds, shape=(5, 2), dimensions=(/lat, /bounds2)>
        lat: <p5netcdf.Variable: /lat, shape=(5,), dimensions=(/lat,)>
            Attributes:
                bounds: 'lat_bnds'
                standard_name: 'latitude'
                units: 'degrees_north'
        lon_bnds: <p5netcdf.Variable: /lon_bnds, shape=(8, 2), dimensions=(/lon, /bounds2)>
        lon: <p5netcdf.Variable: /lon, shape=(8,), dimensions=(/lon,)>
            Attributes:
                bounds: 'lon_bnds'
                standard_name: 'longitude'
                units: 'degrees_east'
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'
        q: <p5netcdf.Variable: /q, shape=(5, 8), dimensions=(/lat, /lon)>
            Attributes:
                cell_methods: 'area: mean'
                coordinates: 'time'
                project: 'research'
                standard_name: 'specific_humidity'
                units: '1'"""
        )


def test_p5netcdf_ppfive(data_dir):
    """Test ppfive functionality."""
    dataset = data_dir / "test2.pp"
    with p5netcdf.Dataset(dataset, backend="ppfive") as p:
        assert p.backend == "ppfive"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 5 dimensions, 9 variables, 0 groups>
    Attributes:
        Conventions: 'CF-1.14'
    Dimensions:
        height: <p5netcdf.Dimension: /height, size=1>
        time: <p5netcdf.Dimension: /time, size=100>
        site: <p5netcdf.Dimension: /site, size=3>
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
        dimension1: <p5netcdf.Dimension: /dimension1, size=1>
    Variables:
        UM_m01s03i236_vn405: <p5netcdf.Variable: /UM_m01s03i236_vn405, shape=(1, 1, 100, 3), dimensions=(/dimension1, /height, /time, /site)>
            Attributes:
                _FillValue: np.float32(-1.0737418e+09)
                cell_methods: 'realization: mean time: mean'
                coordinates: 'height time site longitude latitude region'
                lbcode: '11323'
                lbproc: '131200'
                lbtim: '22'
                lbvc: '1'
                long_name: 'TEMPERATURE AT 1.5M'
                missing_value: np.float32(-1.0737418e+09)
                runid: 'xfqqp'
                source: 'UM'
                standard_name: 'air_temperature'
                stash_code: '3236'
                submodel: '1'
                um_identity: 'UM_m01s03i236_vn405'
                um_stash_source: 'm01s03i236'
                um_version: '4.5'
                units: 'K'
        height: <p5netcdf.Variable: /height, shape=(1,), dimensions=(/height,)>
            Attributes:
                axis: 'Z'
                positive: 'up'
                standard_name: 'height'
                units: 'm'
        time: <p5netcdf.Variable: /time, shape=(100,), dimensions=(/time,)>
            Attributes:
                axis: 'T'
                calendar: '360_day'
                standard_name: 'time'
                units: 'days since 0-1-1'
        site: <p5netcdf.Variable: /site, shape=(3,), dimensions=(/site,)>
            Attributes:
                long_name: 'site'
        longitude: <p5netcdf.Variable: /longitude, shape=(3,), dimensions=(/site,)>
            Attributes:
                bounds: 'longitude_bounds'
                long_name: 'region limit'
                standard_name: 'longitude'
                units: 'degrees_east'
        longitude_bounds: <p5netcdf.Variable: /longitude_bounds, shape=(3, 2), dimensions=(/site, /bounds2)>
        latitude: <p5netcdf.Variable: /latitude, shape=(3,), dimensions=(/site,)>
            Attributes:
                bounds: 'latitude_bounds'
                long_name: 'region limit'
                standard_name: 'latitude'
                units: 'degrees_north'
        latitude_bounds: <p5netcdf.Variable: /latitude_bounds, shape=(3, 2), dimensions=(/site, /bounds2)>
        region: <p5netcdf.Variable: /region, shape=(3,), dimensions=(/site,)>"""
        )


def test_p5netcdf_xarray(data_dir):
    """Test xarray functionality."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="xarray") as p:
        assert p.backend == "xarray"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 0 dimensions, 1 variable, 1 group>
    Attributes:
        Conventions: 'CF-1.13'
        global_attr_1: np.float64(3.14)
        global_attr_2: 'foo'
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'
    Groups:
        forecast: <p5netcdf.Group: /forecast, 2 dimensions, 2 variables, 1 group>
            Dimensions:
                lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
                bounds2: <p5netcdf.Dimension: /forecast/bounds2, size=2>
            Variables:
                lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /forecast/bounds2)>
                lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
                    Attributes:
                        bounds: '/forecast/lon_bnds'
                        standard_name: 'longitude'
                        units: 'degrees_east'
            Groups:
                model: <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
                    Attributes:
                        group_attr_1: np.int64(12)
                        group_attr_2: 'bar'
                    Dimensions:
                        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
                    Variables:
                        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /forecast/bounds2)>
                        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                            Attributes:
                                cell_methods: 'area: mean'
                                coordinates: 'time'
                                float: np.float64(49.0)
                                float32: np.float32(49.0)
                                float64: np.float64(49.0)
                                int: np.int64(49)
                                int16: np.int16(49)
                                int32: np.int32(49)
                                int64: np.int64(49)
                                int8: np.int8(49)
                                list1: array([2, 3], dtype=int8)
                                list10: array([], dtype=float64)
                                list11: ['a', 'bb', 'ccc']
                                list12: ['a', '1', '2.5']
                                list13: 'a'
                                list14: ['a', 'bb']
                                list2: array([2, 3], dtype=int16)
                                list3: array([2, 3])
                                list4: array([2, 3], dtype=int32)
                                list5: array([2., 3.], dtype=float32)
                                list6: array([2., 3.])
                                list7: array([2, 3])
                                list8: np.int32(2)
                                list9: array([], dtype=int32)
                                standard_name: 'specific_humidity'
                                string1: '1'
                                string2: 'a'
                                string3: 'kg m-2'
                                string4: ''
                                string5: ' '
                                string6: ''
                                string7: ''
                                string8: ''
                                string9: ''
                                uint16: np.uint16(49)
                                uint32: np.uint32(49)
                                uint64: np.uint64(49)
                                uint8: np.uint8(49)
                        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                            Attributes:
                                bounds: '/forecast/model/lat_bnds'
                                standard_name: 'latitude'
                                units: 'degrees_north'"""
        )


def test_p5netcdf_Dataset_xarray_like(data_dir):
    """Check Dataset with an xarray.DataTree input."""
    dataset = data_dir / "test.nc"
    xr_dataset = xr.open_datatree(
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


def test_p5netcdf_h5py(data_dir):
    """Test h5py functionality."""
    dataset = data_dir / "test.nc"
    with p5netcdf.Dataset(dataset, backend="h5py") as p:
        assert p.backend == "h5py"
        assert (
            p.dump(display=False)
            == f"""{p.dataset_name}: <p5netcdf.Dataset: /, 1 dimension, 1 variable, 1 group>
    Attributes:
        Conventions: 'CF-1.13'
        global_attr_1: np.float64(3.14)
        global_attr_2: 'foo'
    Dimensions:
        bounds2: <p5netcdf.Dimension: /bounds2, size=2>
    Variables:
        time: <p5netcdf.Variable: /time, shape=(), dimensions=()>
            Attributes:
                standard_name: 'time'
                units: 'days since 2018-12-01'
    Groups:
        forecast: <p5netcdf.Group: /forecast, 1 dimension, 2 variables, 1 group>
            Dimensions:
                lon: <p5netcdf.Dimension: /forecast/lon, size=8, unlimited>
            Variables:
                lon_bnds: <p5netcdf.Variable: /forecast/lon_bnds, shape=(8, 2), dimensions=(/forecast/lon, /bounds2)>
                lon: <p5netcdf.Variable: /forecast/lon, shape=(8,), dimensions=(/forecast/lon,)>
                    Attributes:
                        bounds: '/forecast/lon_bnds'
                        standard_name: 'longitude'
                        units: 'degrees_east'
            Groups:
                model: <p5netcdf.Group: /forecast/model, 1 dimension, 3 variables, 0 groups>
                    Attributes:
                        group_attr_1: np.int64(12)
                        group_attr_2: 'bar'
                    Dimensions:
                        lat: <p5netcdf.Dimension: /forecast/model/lat, size=5>
                    Variables:
                        lat_bnds: <p5netcdf.Variable: /forecast/model/lat_bnds, shape=(5, 2), dimensions=(/forecast/model/lat, /bounds2)>
                        lat: <p5netcdf.Variable: /forecast/model/lat, shape=(5,), dimensions=(/forecast/model/lat,)>
                            Attributes:
                                bounds: '/forecast/model/lat_bnds'
                                standard_name: 'latitude'
                                units: 'degrees_north'
                        q: <p5netcdf.Variable: /forecast/model/q, shape=(5, 8), dimensions=(/forecast/model/lat, /forecast/lon)>
                            Attributes:
                                cell_methods: 'area: mean'
                                coordinates: 'time'
                                float: np.float64(49.0)
                                float32: np.float32(49.0)
                                float64: np.float64(49.0)
                                int: np.int64(49)
                                int16: np.int16(49)
                                int32: np.int32(49)
                                int64: np.int64(49)
                                int8: np.int8(49)
                                list1: array([2, 3], dtype=int8)
                                list10: array([], dtype=float64)
                                list11: ['a', 'bb', 'ccc']
                                list12: ['a', '1', '2.5']
                                list13: 'a'
                                list14: ['a', 'bb']
                                list2: array([2, 3], dtype=int16)
                                list3: array([2, 3])
                                list4: array([2, 3], dtype=int32)
                                list5: array([2., 3.], dtype=float32)
                                list6: array([2., 3.])
                                list7: array([2, 3])
                                list8: np.int32(2)
                                list9: array([], dtype=int32)
                                standard_name: 'specific_humidity'
                                string1: '1'
                                string2: 'a'
                                string3: 'kg m-2'
                                string4: ''
                                string5: ' '
                                string6: ''
                                string7: ''
                                string8: ''
                                string9: ''
                                uint16: np.uint16(49)
                                uint32: np.uint32(49)
                                uint64: np.uint64(49)
                                uint8: np.uint8(49)"""
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
