# New Zealand Gridded Land Information Dataset (NZGLID)

[![release](https://img.shields.io/github/v/tag/baptistehamon/nzglid?label=release)](https://doi.org/10.5281/zenodo.16249350)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16249350.svg)](https://doi.org/10.5281/zenodo.16249350)


This repository contains the code used to create the New Zealand Gridded Land Information Dataset (NZGLID). The files `rasterise.py`, `resample.py` and `nzglid.py` were used for rasterising the input vectors data, resampling the input rasters data and creating the final dataset by merging the rasterised and resampled data, respectively. The `utils.py` file contains utility functions used across the other scripts. The `inspect.py` file contains code for inspecting differences between versions of the dataset. The `sources.txt` file includes the date and url of the sources used to create the dataset. A detailed description of the dataset is provided below. The dataset is available on [Zenodo](https://doi.org/10.5281/zenodo.16809254).

## Description

The ***New Zealand Gridded Land Information Dataset*** integrates data from various sources to offer detailed spatial information about the land, soil, terrain, and environment of New Zealand's mainland. The dataset is available at spatial resolutions of 5 km and 1 km (WGS84). The input data were processed to achieve the final resolutions by rasterizing geospatial vector layers and reprojecting and performing bilinear resampling of raster layers.

The full dataset can be accessed by downloading the following files:

- `NZGLID_5km_v2.0.nc`
- `NZGLID_1km_v2.0.nc`

Individual variable files are also available in .zip folders.

### Variables

The NZGLID comprises a total of 23 variables: aspect, cation exchange capacity, depth to slowly permeable horizon, drainage, elevation, erosion severity, flood return interval, land cover, land use capability, LUCAS land use, particle size, permeability profile, ph, phosphate retention, potential rooting depth, profile readily available water, profile total available water, rock outcrops and surface boulders, salinity, slope, soil temperature regime, topsoil gravel content, total carbon content.

### Using the data

The data is provided in the NetCDF format following the [CF Convention](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html). NetCDF files can be opened and manipulated in GIS softwares (e.g., QGIS) or using programing languages (e.g., Python, R).

Categorical data are provided as numerical values. Users should refer to the `flag_values` and `flag_meanings` attributes for the correspondence between values and categories.

## Citation

If you use this dataset, please cite it as:
Hamon, B. (2026). New Zealand Gridded Land Information Dataset (NZGLID) (v2.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19901807
