# Video2NeRFs

A compilation of scripts to simplify the process of converting a set of videos to a simpler dataformat for NeRFs

Some of the scripts used or modified in this project originate from the following sources:
- [NeRF](https://github.com/bmild/nerf/tree/master) (`load_llff.py`) for preparing the data for NeRFs
- [LLFF](https://github.com/fyusion/llff) (`imgs2poses.py`) for generating the `poses_bounds.npy`
- [Instant NGP](https://github.com/NVlabs/instant-ngp) (`colmap2nerf.py`) for running COLMAP

## Usage

Make sure to have a python environment loaded such as through [Conda](https://docs.anaconda.com/miniconda/).

e.g.
```
conda create -n video2nerf pip
conda activate video2nerf
```

Then install the required libraries
```
pip install -r /path/to/requirements.txt
```
Now navigate to this project's root folder and create a folder such as `videos` and place all the videos you would like to use in that folder like such:
```
Video2NeRFs
|   +-- YOUR_FOLDER_HERE/
|   |   +--vid1.mp4
|   |   +--vid2.mp4
|   |   +--...
|   +-- external/
|   +-- llff/
|   +-- scripts/
|   +-- convert.py
|   +-- imgs2poses.py
|   +-- load_llff.py
...
```
Run `convert.py` to extract all the images. `-p` specifies the path to the folder with the videos and `--fps` specifies the framerate at which we want to collect images.  
```
python convert.py -p ./path_to_videos --fps 2
```
This should have created a folder names `images` which contains all the images from the videos.  

Now run `colmap2nerf.py`. Do not run this inside the scripts folder.  

This may take a while to run depending on the machine and size of the images.

You may need to install COLMAP if you are using macOS or [Linux](https://colmap.github.io/install.html). If you are using macOS, using homebrew may be the simplest way to install it (e.g. `brew install colmap`). 

```
python ./scripts/colmap2nerf.py --colmap_matcher exhaustive --run_colmap
```
To generate the required `poses_bounds.npy` file, now we need to run `imgs2poses.py`.
```
python imgs2poses.py ./
```
Finally, we can generate the final dataset for your NeRF Project.  

`-p` PATH: specifies the base directory for the script  
`-o` FILE_NAME: specifies the output file name  
`--factor` N: downsamples the images by a factor of N  
`--spherify`: makes it so that the render poses are a sphere around an object, rather than a spiral  
```
python load_llff.py -p ./ -o my_dataset --factor 8 --spherify
```