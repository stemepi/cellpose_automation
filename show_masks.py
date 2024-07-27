import os
import sys
import cv2
import pandas as pd
from cellpose import models, denoise, io 
from cellpose.io import imread
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help='name of directory where inputs are located', type=str)
parser.add_argument("input_name", help='name of image to be viewed', type=str)
args = parser.parse_args()

idir = args.input_dir
iname = args.input_name

# This script exists to provide an easy way to read the png and tif outputs produced by automate_seg which cannot be read in a standard image_reader
# imagepath = os.path.join('outputs_png', 'E5_-1_1_1_GFP_001_processed_cp_masks.png')
imagepath = os.path.join(idir, iname)
image = mpimg.imread(imagepath)
plt.imshow(image)
plt.show()
