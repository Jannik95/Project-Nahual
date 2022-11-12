#takes a folder path with rawdata and produces csv and videos
import sys
import loader
import WsaEnlilDatamodelClass
import time
from datetime import timedelta


try:
    dir_path = sys.argv[1]
    print(dir_path)

except:
    print("please provide a directory path with \".tar.gz\" files as argument to this script to create CSVs and Videos from them")
    sys.exit()


def provide_csv_and_video(dir_path: str) -> None:
    start_time = time.time()
    nc_dict = loader.get_rawdata(dir_path)
    print(f"detected files: {nc_dict}")
    for name in nc_dict:
        print(f"current file: {name}")
        model = WsaEnlilDatamodelClass.WsaEnlilDatamodel()
        model.load_from_rawdata(nc_dict[name])
        
        model.save_as_csv(dir_path + "\\" + name + ".csv")
        model.create_video(dir_path + "\\" + name + ".mp4")
        
        runtime = (time.time() - start_time)
        runtime_str = str(timedelta(seconds=runtime))
        print(f"passed time: {runtime_str}")


provide_csv_and_video(dir_path)