import numpy
import pandas
import plotly.express
import plotly.io
from moviepy.editor import ImageSequenceClip
from tempfile import TemporaryDirectory
import time


scatter_default = {"x": "x_coord",
                   "y": "y_coord",
                   "z": "z_coord",
                   "color": "velocity_[m/s]",
                   "range_color": [230000, 680000],
                   "size": "density_[kg/m3]",
                   "template": "plotly_dark",
                   "color_continuous_scale": "jet",
                   }


layout_default = {"title": {"text": "solar wind velocity"},
                  "scene_camera": {"up":{"x": 0, "y": 0, "z": 1},
                                   "center": {"x": 0, "y": 0, "z": 0},
                                   "eye": {"x": 0.8, "y": -0.4, "z": 0.25}
                                   }
                  }


traces_default = {"marker": {"opacity": 1,
                             "line": {"width": 0}
                             },
                  "selector": {"mode": "markers"}
                  }

fps_default = 8


def create_frame(one_timestep: pandas.DataFrame, scatter: dict, layout: dict, traces: dict) -> plotly.graph_objs._figure.Figure:
    #TODO: fig.update_layout(title={"text": "solar wind velocity - bkg-2022-03-14 - 2022-02-01 22:02"})
    frame = plotly.express.scatter_3d(one_timestep, **scatter)
    
    frame.update_layout(**layout)
    
    frame.update_traces(**traces)
    
    return frame


def create_video(data: pandas.DataFrame, filepath: str, frames_per_second=None,  scatter=None, layout=None, traces=None) -> None:
    if frames_per_second == None:
        frames_per_second = fps_default
    if scatter == None:
        scatter = scatter_default
    if layout == None:
        layout = layout_default
    if traces == None:
        traces = traces_default
    
    
    directory = TemporaryDirectory()
    temporary_path = directory.name
    timesteps = numpy.unique(data["absolute_time"].to_numpy())
    #timesteps = set(data["absolute_time"])
    
    i = 100 # TODO: fix iterable to be in order and maybe include file naming
    for timestep in timesteps:
        step = data.loc[data["absolute_time"] == timestep]
        layout["title"]["text"] = f"Solar wind - {timestep}"
        
        frame = create_frame(step, scatter, layout, traces)
        
        frame.write_image((temporary_path + f"\\fig{i}.png"), scale=5)
        i += 1
    
    
    clip = ImageSequenceClip(temporary_path, frames_per_second)
    clip.write_videofile(filepath)
    
    return temporary_path
    

def create_preview(data: pandas.DataFrame, scatter=None, layout=None, traces=None) -> plotly.graph_objs._figure.Figure:
    if scatter == None:
        scatter = scatter_default
    if layout == None:
        layout = layout_default
    if traces == None:
        traces = traces_default
    
    
    times = numpy.unique(data["absolute_time"].to_numpy())
    step = data.loc[data["absolute_time"] == times[0]]
    
    frame = create_frame(step, scatter, layout, traces)
    frame.show()
    
    return frame

