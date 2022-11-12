import pandas
import os
from src import loader
from src import dataformatting
from src import visualizer
from src import testfiles


test_dir = "testdata\\"
test_nc = test_dir + "wsa_enlil.latest.suball.nc"
test_csv = test_dir + "test.csv"
test_video = test_dir + "test.mp4"


def create_testdata(dir_path: str, nc_path: str, csv_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    
    testfiles.create_nc_testfile(nc_path)
    testfiles.create_test_targz(dir_path, nc_path)
    
    datamodel = dataformatting.create_datamodel(nc_path)
    datamodel.to_csv(csv_path, index=False)

    
def test_find_files(dir_path: str):
    assert len(loader.find_files("*wsa_enlil.latest.suball.nc", dir_path)) > 0
    
    
def test_loader_integration(dir_path: str):
    all_raw_paths = loader.get_rawdata(dir_path)

    assert len(all_raw_paths) > 0
    assert type(all_raw_paths) == dict


def test_dataformatting_integration(nc_path: str):
    datamodel = dataformatting.create_datamodel(nc_path)
    
    assert type(datamodel) == pandas.core.frame.DataFrame
    assert len(datamodel) > 0


def test_visualizer_integration(csv_path: str, video_path: str):
    testfile = pandas.read_csv(csv_path)
    
    visualizer.create_video(testfile, video_path) # takes 2 minutes
    assert os.path.getsize(video_path) > 100
    
    

def test_all(dir_path: str, nc_path: str, csv_path: str, video_path: str):
    import time
    start_time = time.time()
    
    create_testdata(dir_path, nc_path, csv_path)
    
    test_find_files(dir_path)
    test_loader_integration(dir_path)
    test_dataformatting_integration(nc_path)
    test_visualizer_integration(csv_path, video_path)
    
    runtime = (time.time() - start_time)
    print(f"all tests successful - time: {runtime} seconds")


if __name__ == "__main__":
    test_all(test_dir, test_nc, test_csv, test_video)
