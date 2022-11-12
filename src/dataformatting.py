# expects list of "wsa_enlil.latest.suball.nc"-filepaths and returns a dataframe with tidy and cartesian data
import xarray
import pandas
import numpy


def create_datamodel(filepath: str) -> pandas.DataFrame:
    wsa_enlil_dataset = xarray.open_dataset(filepath)
    data = format_data(wsa_enlil_dataset)
    
    return data

def format_data(wsa_enlil_dataset: xarray.Dataset) -> pandas.DataFrame:
    data = join_dataarrays_with_same_coordinates(wsa_enlil_dataset)
    data = provide_spheric_coordinates_for_indeces(wsa_enlil_dataset, data)
    data = provide_absolute_time_for_indices(wsa_enlil_dataset, data)
    data = provide_cartesian_coordinates_from_spheric(data)
    
    data = data.reset_index()
    data = data.drop(["index"], axis=1)
    
    return data


def join_dataarrays_with_same_coordinates(wsa_enlil_dataset: xarray.Dataset) -> pandas.DataFrame:
    dd12_3d_df = calibrate_data(wsa_enlil_dataset.dd12_3d)
    vv12_3d_df = calibrate_data(wsa_enlil_dataset.vv12_3d)
    pp12_3d_df = calibrate_data(wsa_enlil_dataset.pp12_3d)
    
    rad_colat_data = pandas.concat([dd12_3d_df, vv12_3d_df, pp12_3d_df], axis=1)
    rad_colat_data = rad_colat_data.reset_index()
    rad_colat_data = rad_colat_data.rename(columns={"dd12_3d": "density_[kg/m3]", "vv12_3d": "velocity_[m/s]", "pp12_3d": "polarity"})
    rad_colat_data.insert(1, "z", 9999)
    
    
    dd13_3d_df = calibrate_data(wsa_enlil_dataset.dd13_3d)
    vv13_3d_df = calibrate_data(wsa_enlil_dataset.vv13_3d)
    pp13_3d_df = calibrate_data(wsa_enlil_dataset.pp13_3d)
    
    rad_long_data = pandas.concat([dd13_3d_df, vv13_3d_df, pp13_3d_df], axis=1)
    rad_long_data = rad_long_data.rename(columns={"dd13_3d": "density_[kg/m3]", "vv13_3d": "velocity_[m/s]", "pp13_3d": "polarity"})
    rad_long_data = rad_long_data.reset_index()
    rad_long_data["y"] = 9999
    
    
    dd23_3d_df = calibrate_data(wsa_enlil_dataset.dd23_3d)
    vv23_3d_df = calibrate_data(wsa_enlil_dataset.vv23_3d)
    pp23_3d_df = calibrate_data(wsa_enlil_dataset.pp23_3d)
    
    colat_long_data = pandas.concat([dd23_3d_df, vv23_3d_df, pp23_3d_df], axis=1)
    colat_long_data = colat_long_data.rename(columns={"dd23_3d": "density_[kg/m3]", "vv23_3d": "velocity_[m/s]", "pp23_3d": "polarity"})
    colat_long_data = colat_long_data.reset_index()
    colat_long_data["x"] = 9999
    
    concatenated_data_df = pandas.concat([rad_colat_data, rad_long_data, colat_long_data])
    
    return concatenated_data_df
    
    
def calibrate_data(rawdata: xarray.DataArray) -> pandas.DataFrame:
    data = rawdata.to_dataframe()
    param_max = rawdata.attrs[list(rawdata.attrs)[0]]
    param_min = rawdata.attrs[list(rawdata.attrs)[1]]
    cal_max = numpy.float64(numpy.amax(data.to_numpy()))
    cal_min = numpy.float64(numpy.amin(data.to_numpy()))
        
    data[rawdata.name] = ((data[rawdata.name] - cal_min) * ((param_max - param_min) / (cal_max - cal_min))) + param_min
    return data
    

def provide_spheric_coordinates_for_indeces(wsa_enlil_dataset: xarray.Dataset, concatenated_data_df: pandas.DataFrame) -> pandas.DataFrame:
    spheric_data_df = concatenated_data_df
    
    r_df = wsa_enlil_dataset.x_coord.to_dataframe()
    r_df = r_df.rename(columns={"x_coord": "distance_r"})
    spheric_data_df = spheric_data_df.join(r_df, on="x")
    
    astronomical_unit = 149597870700
    spheric_data_df.loc[spheric_data_df['x'] == 9999, "distance_r"] = astronomical_unit
    
    
    colat_df =  wsa_enlil_dataset.y_coord.to_dataframe()
    colat_df = colat_df.rename(columns={"y_coord": "colatitude_theta"})
    spheric_data_df = spheric_data_df.join(colat_df, on="y")
    
    latitude_zero = numpy.pi / 2
    spheric_data_df.loc[spheric_data_df['y'] == 9999, "colatitude_theta"] = latitude_zero # this defines the zero plane to always be in line with the earth inclination instead of the solar equator; it seems to be the most fitting value, since tests with actual change to earth latitude looked unfitting in the vizualisation
    
    
    longitude_df = wsa_enlil_dataset.z_coord.to_dataframe()
    longitude_df = longitude_df.rename(columns={"z_coord": "longitude_phi"})
    longitude_df = longitude_df["longitude_phi"] - numpy.pi # not entirely understood, maybe to set longitudefrom 0<phi<2pi to -pi<phi<pi?
    spheric_data_df = spheric_data_df.join(longitude_df, on="z")
    
    default_longitude = 0.0
    spheric_data_df.loc[spheric_data_df['z'] == 9999, "longitude_phi"] = default_longitude
    
    return spheric_data_df


def provide_cartesian_coordinates_from_spheric(spheric_data_df: pandas.DataFrame) -> pandas.DataFrame:
    cartesian_data_df = spheric_data_df
    
    x_coord = spheric_data_df["distance_r"] * numpy.cos(spheric_data_df["longitude_phi"]) * numpy.sin(spheric_data_df["colatitude_theta"])
    y_coord = spheric_data_df["distance_r"] * numpy.sin(spheric_data_df["longitude_phi"]) * numpy.sin(spheric_data_df["colatitude_theta"])
    z_coord = spheric_data_df["distance_r"] * numpy.cos(spheric_data_df["colatitude_theta"])
    
    cartesian_data_df["x_coord"] = x_coord
    cartesian_data_df["y_coord"] = y_coord
    cartesian_data_df["z_coord"] = z_coord

    return cartesian_data_df


def provide_absolute_time_for_indices(wsa_enlil_dataset: xarray.Dataset, data: pandas.DataFrame) -> pandas.DataFrame:
    import datetime
    times = wsa_enlil_dataset.time.to_dataframe()
    
    REFDATE_CAL = wsa_enlil_dataset.attrs["REFDATE_CAL"]
    refdate = datetime.datetime.strptime(REFDATE_CAL, "%Y-%m-%dT%H:%M:%S")
    
    absolute_datetime = refdate + times["time"]
    times["absolute_time"] = absolute_datetime
    
    data = data.join(times["absolute_time"], on="t")

    return data

