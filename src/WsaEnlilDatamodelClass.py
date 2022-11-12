import numpy
import pandas

import plotly.express

class WsaEnlilDatamodel:
    def __init__(self) -> None:
        self._rawdatapath = None
        self._filepath = None
        self._save_path = None
        self.datamodel = None
        self.compressed = None

    
    def load_from_rawdata(self, rawdatapath: str) -> None:
        """
        
        """
        import dataformatting
        self._rawdatapath = rawdatapath
        self.datamodel = dataformatting.create_datamodel(rawdatapath)

    
    def load_from_csv(self, filepath: str) -> None: # quickload
        self._filepath = filepath
        self.datamodel = pandas.read_csv(filepath)

    
    def save_as_csv(self, save_path: str) -> None: # takes for 2 datafiles 10 minutes and 6gb space.. # creates "unnamed: 0" column
        self._save_path = save_path
        self.datamodel.to_csv(save_path, index=False)
        
    
    def compress(self, timesteps: int): # dedicated for a good vizualization and a small save file
        self.compressed = self.datamodel
        self.compressed = self.compressed[['absolute_time', 'x_coord', 'y_coord', 'z_coord', 'density_[kg/m3]', 'velocity_[m/s]', 'polarity']]
        self._reduce_timesteps(timesteps)
        self.compressed["absolute_time"] = self.compressed["absolute_time"].dt.strftime("%Y-%m-%d %H:%m") # could just remove "t" in import

    
    def _reduce_timesteps(self, steps: int):
        times = numpy.unique(self.compressed["absolute_time"].to_numpy())
        earliest = times[0]
        latest = times[-1]
        ideal_steps = pandas.date_range(earliest, latest, steps)
        ideal_steps = numpy.array(ideal_steps)
        
        real_steps = numpy.searchsorted(times, ideal_steps)
        steps = times[real_steps]

        self.compressed = self.compressed.loc[self.datamodel["absolute_time"].isin(steps)]
    
    
    def create_video(self, save_path: str, frames_per_second=None,  scatter=None, layout=None, traces=None) -> None:
        import visualizer
        self._save_path = save_path

        visualizer.create_video(self.datamodel, save_path, frames_per_second,  scatter, layout, traces)
        


def test():
    import loader

    testfile = "Testdata\\vv13_3d_test_data.csv"
    rawdata_path = "Testdata\\ncei_order_2022-06-04T06_12_57.535Z_singlefile.tar.gz" #bkg file
    filepath_two_files = "Testdata\\ncei_order_2022-07-18T14_23_27.468Z_twoCMEfiles_spacexstorm.tar.gz"
    csv_save_path = "Testdata\\csv_save.csv"
    save2 = "C:\\Users\\Jannik\\Downloads\\test_save.csv"
    test_files = loader.unpack_rawdata_to_cmebkg(filepath_two_files)

    datamodel = WsaEnlilDatamodel()
    datamodel.load_from_rawdata(test_files["cme_files"][1])
    #datamodel.preview()
    #datamodel.save_as_csv(csv_save_path)
    #datamodel.load_from_csv(csv_save_path)

    runtime = (time.time() - start_time)
    print(f"WsaEnlilDatamodel - test successful - time: {runtime} seconds")
    return datamodel
    
def test2():
    save = "Testdata\\compressed_export.csv"
    datamodel = WsaEnlilDatamodel()
    datamodel.load_from_csv(save)
    
    runtime = (time.time() - start_time)
    print(f"WsaEnlilDatamodel - test successful - time: {runtime} seconds")
    
    return datamodel
    
    
if __name__ == "__main__":
    import time
    start_time = time.time()
    
    #test = test()
    model1 = test2()
