import os
import sys
import cv2
import numpy as np
import pandas as pd
from cellpose import models, denoise, io, utils
from cellpose.io import imread
import argparse
import skimage as ski
from pathlib import Path

# This is a helper function used for skimage processing
def intensity_sdeviation(mask, intensity):
    return np.std(intensity[mask])


# Use for debugging purposes if needed
# logger = io.logger_setup()

# The following chunk of code is to handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help='name of directory where inputs are located', type=str)
parser.add_argument("-t", "--saveMasksTIF", action="store_true", help="toggle saving of masks in .tif file format")
parser.add_argument("-p", "--saveMasksPNG", action="store_true", help="toggle saving of masks in .png file format")
parser.add_argument("-id", "--storeCellIntensityData", action="store_true", help="store intensity data for individual cells")
args = parser.parse_args()


# Note: Channels are set to 0 because images are in greyscale
channels = [0,0]
# Change this to potentially improve model performance. This is the expected cell diameter
diam = 30.0
# diam = 20.0
# diam = 40.0


idir = args.input
saveMasksTIF = args.saveMasksTIF
saveMasksPNG = args.saveMasksPNG
storeCellIntensityData = args.storeCellIntensityData
input_dir = os.path.join('images',idir)

# Model to use
# Current model pre-trained model from Cellpose3 and include denoise
model = denoise.CellposeDenoiseModel(gpu=True, model_type='cyto3', restore_type='denoise_cyto3', chan2_restore=False)
# or
# model = models.Cellpose(gpu=True, model_type='cyto3')
# model = models.Cellpose(gpu=True, model_type='cyto2')
# model = models.Cellpose(gpu=True, model_type='cyto')
# model = denoise.CellposeDenoiseModel(gpu=True, model_type='cyto2', restore_type='denoise_cyto2', chan2_restore=False)



# Initialize vars
vals = []
names = []
n = 0
input_imgs = []

print(f'retrieving images within: {input_dir}')

# Load the images in by iterating through the entire input directory
print('parsing input directory...')
for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if "GFP" in filename and '.tif' in filename:
            fullpath = os.path.join(root, filename)
            input_imgs.append(imread(fullpath))
            final_name = filename.replace('.tif', '_processed')
            names.append(Path(final_name))
            n += 1

if n == 0:
    raise ValueError('0 valid images found! Did you specify the right input directory?')

print(f'{n} images found to run segmentation (ignore if in test run mode)')
        




# Run denoise (image restoration) and automatic cell segementation model simultaneously
# This is done for all images in the input list
print('running segmentation...')
masks, flows, styles, diams = model.eval(input_imgs,diameter=diam,channels = channels)
print('segmentation complete.')


# Save masks for debugging and visualization purposes if desired
# Note that masks will be saved as an int16 image and will likely require either imageJ or matplotlib to be viewed
if saveMasksTIF == True:
    io.save_masks(input_imgs, masks, flows, names, savedir='outputs_tif', png=False, tif=True)
if saveMasksPNG == True:
    io.save_masks(input_imgs, masks, flows, names, savedir='outputs_png', png=True, tif=False)



# Write relevant roi values to csv
final_means = []
final_stds = []
amount_cells = []
final_intensities = []
final_intensitystds = []
for i in range(len(masks)):
    props_table = pd.DataFrame(ski.measure.regionprops_table(masks[i], intensity_image=input_imgs[i], properties=['label','intensity_mean'], extra_properties=[intensity_sdeviation]))

    if storeCellIntensityData == True:
        imageCSVPath = os.path.join('roiCSV_outputs',f'{names[i]}.csv')
        props_table.to_csv(imageCSVPath,index=False)


    unique, counts = np.unique(masks[i], return_counts=True)
    final_intensities.append(props_table.loc[:,'intensity_mean'].mean())
    final_intensitystds.append(props_table.loc[:,'intensity_mean'].std())
    i, = np.where(unique == 0)
    areas = np.delete(counts, i)
    final_means.append(areas.mean())
    final_stds.append(areas.std())
    amount_cells.append(len(unique))

dict = {'name': names, 'nucleus_area_mean': final_means, "nucleus_area_std": final_stds, "amount_of_cells": amount_cells, "mean_intensity": final_intensities, "standard_dev_of_mean_intensities": final_intensitystds}
df = pd.DataFrame(dict)
df.to_csv('value_outputs.csv', index=False)



# Save masks as rois for opening in imagej
for i in range(0, len(masks)):
    mask = masks[i]
    name = names[i]
    io.save_rois(mask, os.path.join('outputs_roi',f'output_{names[i]}'))

