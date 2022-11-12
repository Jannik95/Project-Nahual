import os, fnmatch
import tarfile
from tempfile import TemporaryDirectory


def get_rawdata(dir_path: str) -> dict:
    temp_dir = unpack_dir(dir_path)
    nc_files = find_files("wsa_enlil.latest.suball.nc", temp_dir)
        

    rawdata = {}
    
    for file in nc_files:
        name = os.path.basename(os.path.dirname(file))
        rawdata[name] = file
        
    return rawdata


def unpack_dir(dir_path: str) -> str:
    temp_dir = TemporaryDirectory().name
    
    archive_paths = find_files("*.tar.gz", dir_path)
    
    for file in archive_paths:
        open_tar = tarfile.open(file)
        open_tar.extractall(temp_dir)
    
    sub_file_paths = find_files("*.tar.gz", temp_dir)
    
    for file in sub_file_paths:
        open_tar = tarfile.open(file)
        open_tar.extractall(file.removesuffix(".tar.gz"))
    
    return temp_dir


def find_files(pattern: str, path: str) -> list:
    file_names = []
    
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                file_names.append(os.path.join(root, name))
    
    return file_names

