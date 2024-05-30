# rainfall_analysis
Analysis of rainfall over Singapore using NEA satellite imagery 

## Overview
This library is designed to fetch, process, and analyze rainfall data from weather images. It can convert the images to magnitudes, save the data in GeoJSON and HDF5 formats, and provide tools to review the stored data. The data is indexed by datetime, latitude, and longitude, allowing for temporal and spatial analysis of rainfall.

##HDF5 File Structure
The HDF5 file created by this library has the following structure:

- magnitudes: A 3D dataset with dimensions (time_steps, latitudes, longitudes) representing rainfall magnitudes.
- latitudes: A 1D dataset with latitude values.
- longitudes: A 1D dataset with longitude values.
- datetimes: A 1D dataset with datetime strings corresponding to each time step.
Analyzing HDF5 Data
