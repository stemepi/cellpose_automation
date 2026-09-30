# Automated Cellpose Segmentation Pipeline for Quantitative Image Analysis

## Introduction 
This repository contains a script for automating a cell segmentation and analysis procedure used by the lab of Dr. Haiting Ma at the UIUC MCB department. It relies on the Cellpose API for generalized cell segmentation, the citation for which can be found as [1] in the references section. It also utilizes functionalities from the scikit-image library, can be cited as [2]. 

The main functionality is in "automate_seg.py". A minor additional script, "show_masks.py" is included simply to open mask images with matplotlib, as they cannot be viewed with a traditional image viewer. 

This repository was developed using specific versions of Python, Cellpose, Cellpose.io, OpenCV, and Scikit-Image, among othes. A requirements.txt file is provided to set up the necessary virtual environment.

## Usage
Ensure that the following directories are present:

outputs_png\
outputs_roi\
outputs_tif\
roiCSV_outputs\
images 

### automate_seg.py

#### Inputs

"automate_seg.py" has only one required command line argument, and it represents the input. The argument should be the name of the directory which contains the images to be analyzed. Please place the directory within the directory labeled "images". The script will parse through and load all .tif formatted images with the phrase "GFP" in the file name. It will also use the original file name to label outputs. Input directory can be of any format and contain irrelevant content, but note that any images that are not in .tif format or missing the phrase "GFP" will not be processed. Also ensure that any .tif images you do not want processed do not contain "GFP" in their file name.

#### Outputs

"automate_seg.py" will always have two types of outputs. 

The first output is a single .csv file which will be written to the main directory as "output.csv". This CSV will contain aggregated metrics for all the images in the input directory, each line respective to one image. This line will contain the average area of the ROIs in pixels, the standard deviation of the areas, the amount of ROIs, and the average of each ROI's average intensity, and the standard deviation of the ROI's average intensity. 

The second output is a series of .zip files containing ROI data, which can be opened in ImageJ for manual processing. These are written into the "outputs_roi" directory and there is a zip file for every input image.

#### Optional command line arguments are included for user convinience. 

Including "-id" triggers the option to save individual ROI intensity values. This saves the mean intensity and standard deviation of intensity for each region of interest (ROI) within an image, in the form of a csv. This will generate a CSV for every image in the input directory, and it will write them to the "roiCSV_outputs" directory.

Including "-t" triggers the option to save the intemediate output masks as a .tif file(s). They will be written to the "outputs_tif" directory and will require the "show_masks.py" helper function to view. They can also be viewed with ImageJ.

Including "-p" triggers the option to save the intemediate output masks as a .png file(s). They will be written to the "outputs_png" directory and will require the "show_masks.py" helper function to view. They can also be viewed with ImageJ.

Note that the "-tr" argument, respective to the "test run" option, is no longer included. This is because the feature was determined redundant after the script was finished and removed for clarity.

#### Note that none of the output directories clear automatically. If there is an existing file within an ouptut directory with the same name as a new output, it will be written over.

### show_masks.py

"show_masks.py" is a small helper function used to view any outputs written to "outputs_png" and "outputs_tif" if ImageJ is not available. It has two command line arguments. The first should be either "outputs_png" or "outputs_tif" depending on where the image is located. The second should be the name of the image to be viewed. There are no outputs.

## References
[1] Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106.\
[2] Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu, and the scikit-image contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014) https://doi.org/10.7717/peerj.453

## Authors:
The script in this repository was originally authored by Franklyn Wu.
