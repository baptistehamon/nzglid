# Release Notes

## v2.0 (2026-04-30)

### Code updates
- The code has been split into multiple scripts for better organization and readability.
  - `rasterise.py` was created and contains the code for rasterising the input vectors data.
  - `resample.py` was created and contains the code for resampling the input rasters data.
  - `nzglid.py` is now used to create the final dataset by merging the rasterised and resampled data.
  - `utils.py` was created and contains utility functions used across the other scripts.
  - `inspect.py` was created and contains code for inspecting differences between versions of the dataset.
- The `sources.txt` file was added and include the date and url of the sources used to create the dataset.

### Data updates
- The _elevation_ variable has been added to the dataset.
- The version of the following input variables have been updated:
  - The _land-cover_ has been updated to version 6.
  - The _LUCAS land use_ has been updated to version 5.
- The following corrections and fixes have been made to the dataset:
  - The missing data for the _land cover_ variable has been fixed. 
  - The negative values in the slope variable have been corrected and replaced by 0.
  - The variable _rock_ has been renamed to _rock outcrops surface boulders_ for better clarity.
- As results of the above updates, minor differences can be observed in the _slope_, _land use capability_, _land cover_ and
_LUCAS land use_ variables between version 1.1 and version 2.0 of the dataset.

## v1.1 (2025-08-12)

- This version modifies the structures of the archives removing subfolders making downloading data through zenodo API easier.
- The data itself and the code used to create the dataset remain unchanged.

## v1.0 (2025-07-23)

- Initial release of the New Zealand Gridded Land Information Dataset (NZGLID).
- The dataset includes the following 22 variables at 5 km and 1 km spatial resolutions (WGS84): land use capability, erosion severity, ph, salinity, cation exchange capacity, soil carbon, phosphate retention, topsoil gravel content, rock outcrops and surface boulders, particle size, potential rooting depth, depth to slowly permeable horizon, soil drainage, permeability profile, flood return interval, soil temperature regime, profile available water, profile readily available water, slope, aspect, land cover, land use.
