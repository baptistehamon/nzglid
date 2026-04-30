"""Merge individual variable files into a single dataset for each resolution."""

import xarray as xr

from nzglid import (
    NZGLID_PATH,
    RESOLUTION,
    VECTOR_VARS,
    RASTER_VARS,
    METADATA,
    release
)

for res in RESOLUTION:
    
    res_path = NZGLID_PATH / f"nzglid_{res}"

    files = list(res_path.glob("*.nc"))
    raster_files = [fp for fp in files if fp.stem.split("_")[1].replace("-", "_") in RASTER_VARS]
    vector_files = [fp for fp in files if fp.stem.split("_")[1].replace("-", "_") in VECTOR_VARS]

    # open rasters
    ds = xr.merge([xr.open_dataarray(fp) for fp in raster_files], join="outer")
    ds['lon'] = ds['lon'].round(3) # round to 3 decimals to avoid precision issues when merging with vector data
    ds['lat'] = ds['lat'].round(3)
    ds = xr.merge([ds, *[xr.open_dataarray(fp) for fp in vector_files]], join="outer")
    ds.attrs = METADATA
    ds.to_netcdf(NZGLID_PATH / f"NZGLID_{res}_v{release}.nc")
