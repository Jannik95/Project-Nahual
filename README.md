# Project Nahual Visualizer

The Project Nahual visualizer is a Python script, which is a first step of the bigger [Project Nahual](https://nahual.eu/). It is designed to bring data from the WSA-enlil model provided by the NOAA into a 3D visualization. I created it to get a better grasp on which data the model exactly provides. Additionally in the future I plan to modify the data and a 3D visualization helps immensely with understanding behaviour and problems.

## Usage

In its current status the main file takes a directory with respecting [rawdata files](https://www.ngdc.noaa.gov/enlil/) as argument and creates tidy csv-data and videos from every file detected in the same folder. Subfunctions can be accessed with importing and integrating the WsaEnlilDatamodelClass in your own code. Running the "test.py" script will execute all written tests.

Command line usage example:
```
C:\Users\Jannik>python "..\src\main.py" "..\testdata"
or
C:\Users\Jannik>"<absolute filepath venv-python.exe>" "<absolute filepath main.py>" "<absolute filepath with rawdata/.tar.gz-files>"
```

The script is work in progress, the video functionality unfortunately takes 30 minutes per file, because the chosen plotly library takes a lot of time to bring the data into pictures. Additionally you might find unexpected behaviour when using the script.

## Requirements
A requirements.txt is provided to setup a virtual environment with venv. To run the script defaultly with the "testdata" folder, just run the "test.py" script once, to create testdata, which is also used for the tests.


## Notes
Since this is my first project on GitHub I don't know how to handle contributions. You might try it and see what happens. In the time of Project Nahual I will probably add or change features.

This project uses the standard MIT licence. Do what you cant let and have fun.