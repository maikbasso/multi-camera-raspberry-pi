# multi-camera-raspberry-pi
Enables the use of Multi Camera Adapter Module on Raspberry Pi. This software creates the visualization by separating the multiplexed images provided by the Arducam Multi Camera Adapter Module.

## Using on Raspberry PI
At the terminal, install all dependencies:
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo rpi-update
$ sudo apt-get install g++ libopencv-dev python-dev python-numpy python-opencv opencv-docs ffmpeg
```
Clone repository:
```
$ git clone https://github.com/maikbasso/multi-camera-raspberry-pi.git
```
Running:
```
$ python multi-camera-raspberry-pi/multi-camera.py
```
During the execution of the software, enter the number of cameras installed on the adapter. The minimum number of cameras for the software is 1 and the maximum number is 4.

## Changing the display mode
In the code, search for the line `displayImage (img, 1)`. Using as parameter: 1 for the visualization of all the cameras in a window, and 2 for visualization in separate windows.
