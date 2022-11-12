import numpy
import xarray
import tarfile


def create_wsa_enlil_testdata() -> xarray.Dataset:
    test_attrs = {'WARNING': 'THIS IS A RANDOMLY GENERATED TESTFILE',
                  'REFDATE_MJD': 59652.0,
                  'REFDATE_CAL': '2022-03-14T00:00:00',
                  'OBSDATE_MJD': 59652.0,
                  'OBSDATE_CAL': '2022-03-14T00:00:00',
                  'program': 'enlil',
                  'enlil_version': '2.9',
                  'wsa_version': 'WSA_V2.2',
                  'enlil_param_code': 'reg2med1.dvb-a8b1-d4',
                  'wsa_vel_file': 'wsa.gong.fits',
                  'observatory': 'gongb',
                  'model_run_id': '46290',
                  'execution_start_time': '2022-03-14 00:05',
                  'PDY': '20220314',
                  'cyc': '00',
                  'datafile_format_version': '1.0',
                  'summary': 'Standard Enlil model output file as utilized by NOAA/SWPC',
                  'cal_min': -32768.0,
                  'cal_range': 65535.0,
                  'calibration_explanation': "All parameters whose names begin with 'uncalibrated' are calibrated with the following formula: param_calibrated=((param_uncalibrated-cal_min)*(param_max-param_min)/cal_range)+param_min, where param_max and param_min are attributes associated with each uncalibrated parameter."}

    rng = numpy.random.default_rng()

    test_data_vars = {
        "x_coord": (["x"], numpy.linspace(1.52e+10, 2.54e+11, num=128, dtype="float32"), {'long_name': 'longitudinal magnetic field at points on the magnetic field line which passes through STEREO_B', 'units': 'T'}),
        "y_coord": (["y"], numpy.linspace(0.54, 2.60, num=15, dtype="float32"), {'long_name': 'co-latitude cell positions', 'units': 'radians'}),
        "z_coord": (["z"], numpy.linspace(0.02, 6.09, num=45, dtype="float32"), {'long_name': 'longitude cell positions', 'units': 'radians'}),
        "time": (["t"], numpy.linspace(-172794312500000, 432157906250000, num=8, dtype='timedelta64[ns]'), {'long_name': 'time relative to REFDATE'}),
        "dd12_3d": (["t", "y", "x"], rng.integers(low=-32768, high=32767, size=(8,15,128), dtype=numpy.int16), {'dd12_max': 2.5593448e-18, 'dd12_min': 6.4323193e-22, 'long_name': 'uncalibrated plasma density in rad-colat-time, longitude zero', 'units': 'kg/m3 - after calibration'}),
        "vv12_3d": (["t", "y", "x"], rng.integers(low=-32768, high=32767, size=(8,15,128), dtype=numpy.int16), {'vv12_max': 591867.44, 'vv12_min': 212494.62, 'long_name': 'uncalibrated velocity in rad-colat-time, longitude zero', 'units': 'm/s - after calibration'}),
        "pp12_3d": (["t", "y", "x"], rng.integers(low=-32768, high=32767, size=(8,15,128), dtype=numpy.int16), {'pp12_max': 98.58362, 'pp12_min': -99.63219, 'long_name': 'uncalibrated magnetic polarity in rad-colat-time, longitude zero'}),
        "dd13_3d": (["t", "z", "x"], rng.integers(low=-32768, high=32767, size=(8,45,128), dtype=numpy.int16), {'dd13_max': 2.416222e-18, 'dd13_min': 9.587344e-22, 'long_name': 'uncalibrated plasma density in rad-long-time, Earth latitude', 'units': 'kg/m3 - after calibration'}),
        "vv13_3d": (["t", "z", "x"], rng.integers(low=-32768, high=32767, size=(8,45,128), dtype=numpy.int16), {'vv13_max': 550474.9, 'vv13_min': 218759.16, 'long_name': 'uncalibrated velocity in rad-long-time, Earth latitude', 'units': 'm/s - after calibration'}),
        "pp13_3d": (["t", "z", "x"], rng.integers(low=-32768, high=32767, size=(8,45,128), dtype=numpy.int16), {'pp13_max': 99.641304, 'pp13_min': -96.63624, 'long_name': 'uncalibrated magnetic polarity in rad-long-time, Earth latitude'}),
        "dd23_3d": (["t", "z", "y"], rng.integers(low=-32768, high=32767, size=(8,45,15), dtype=numpy.int16), {'dd23_max': 4.029721e-20, 'dd23_min': 2.6127277e-21, 'long_name': 'uncalibrated plasma density in colat-long-time, 1AU surface', 'units': 'kg/m3 - after calibration'}),
        "vv23_3d": (["t", "z", "y"], rng.integers(low=-32768, high=32767, size=(8,45,15), dtype=numpy.int16), {'vv23_max': 590585.0, 'vv23_min': 232180.78, 'long_name': 'uncalibrated velocity in colat-long-time, 1AU surface', 'units': 'm/s - after calibration'}),
        "pp23_3d": (["t", "z", "y"], rng.integers(low=-32768, high=32767, size=(8,45,15), dtype=numpy.int16), {'pp23_max': 2.9621806, 'pp23_min': -2.3206325, 'long_name': 'uncalibrated magnetic polarity in colat-long-time, 1AU surface'}),
        }

    dataset = xarray.Dataset(data_vars = test_data_vars,
                             attrs = test_attrs,
                             )
    
    return dataset


def create_nc_testfile(filename: str) -> None:
    data = create_wsa_enlil_testdata()
    data.to_netcdf(filename)


def create_targz(archive_name: str, content_path: str, archive_path: str) -> None:
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(content_path, arcname=archive_path)


def create_test_targz(dir_path: str, nc_file: str):
    import os
    create_targz(dir_path + "swpc_waenlil_cme_20220202_2000.tar.gz", nc_file, "wsa_enlil.latest.suball.nc")
    
    structure = "archive-item-000000\\models\\space_weather\\enlil\\2022\\02\\swpc_waenlil_cme_20220202_2000.tar.gz"
    create_targz(dir_path + "test.tar.gz", dir_path + "swpc_waenlil_cme_20220202_2000.tar.gz", structure)
    
    os.remove(dir_path + "swpc_waenlil_cme_20220202_2000.tar.gz") # unclean solution, but I don't want to have this and it needs to be there for tarfile.add

    #file.tar.gz > archive-item-456460\\models\\space_weather\\enlil\\2022\\02\\swpc_waenlil_cme_20220202_2000.tar.gz (x2)

    #> pictures, video, txt-file CMEs, inputs.tar.gz, wsa_enlil.latest.suball.nc
