# PyQt based visualization toolkit, PICviewer #

![picture](PICviewer_logo.png)

##The toolkit provides various easy-to-use functions for data analysis of PIC simulations.

## Main features
* 2D/3D openPMD or WarpX data visualization
(automatically detects the data type)
* 2D slicing in 3D images,
* multi-plot panels (up to 6 rows x 5 columns) which are conrolled independently or synchronously,
* interactive mouse functions (panel selection, image zoom-in, local data selection, etc),
* making a movie file (.mp4),
* saving your job configuration and loading it later, 
(you do not need to repeat the same work),
* interface to use VisIt, yt, or mayavi for 3D volume rendering (not available now, currently updating)

## Required software
* python 2.7 or higher:
http://docs.continuum.io/anaconda/install.

* PyQt5
```
conda install pyqt
```
* h5py
* matplotlib
* numpy
* yt
```
conda install -c atmyers yt
```
* numba

## To install with pip
```
pip install picviewer
```
You have to install yt and PyQt5 separately as above.

For the latest updates,
```
pip install git+https://bitbucket.org/ecp_warpx/picviewer/
```

## To install manually

* Clone this repository `git clone https://bitbucket.org/ecp_warpx/picviewer/`
* Switch to the cloned directory with `cd picviewer` and type `python setup.py install`

## To run

* You can start PICViewer from any directory. Type `picviewer` in the command line. Select a folder where your data files are located. 
* You can directly open your data. Move on to a folder where your data files ae located (`cd [your data folder]`) and type `picviewer` in the command line.

## To make a movie, ffmpeg should be installed.
* for Mac users, `brew install ffmpeg`
* for Nersc users, `module load ffmpeg`
* for other linux users, download with wget and untar.
https://gist.github.com/jmsaavedra/62bbcd20d40bcddf27ac

## Contact
* Developer: Jaehong Park (LBNL); jaehongpark@lbl.gov

![picture](sample.png)
Figure shows several widget tools in the left side and multi-plot panels in the right side.
