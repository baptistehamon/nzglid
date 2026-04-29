"""Resample rasters to 5km and 1km resolution."""

from pathlib import Path
import xarray as xr

from nzglid import DATAPATH, NZGLID_PATH, METADATA, release, RESOLUTION
from nzglid.helpers import make_exraster, reproj_match, open_raster

for res, grid in RESOLUTION.items():

    if not Path(f"WGS84_{res}.tif").exists():
        make_exraster(f"WGS84_{res}.tif", grid)
    
    res_path = NZGLID_PATH / f"nzglid_{res}"
    res_path.mkdir(exist_ok=True)

    # Aspect
    fp = DATAPATH / "lris-nzenvds-nz-environmental-data-stack/nzenvds-aspect-degrees-v10"
    reproj_match(fp / "nzenvds-aspect-degrees-v10.tif", f"WGS84_{res}.tif", fp / f"aspect_{res}.tif")
    da = open_raster(fp / f"aspect_{res}.tif").rename("aspect")
    da.attrs = {
        **METADATA,
        'long_name': 'Aspect',
        'units': 'degrees',
        'source': 'https://lris.scinfo.org.nz/layer/105706-nzenvds-aspect-degrees-v10/',
        'comment': 'from field: Band 1'
    }
    da.to_netcdf(res_path / f"NZGLID_aspect_{res}_v{release}.nc")
    
    # Elevation
    fp = DATAPATH / "lris-nzdem-25-metre-GTiff"
    reproj_match(fp / "nzdem.tif", f"WGS84_{res}.tif", fp / f"elevation_{res}.tif")
    da = open_raster(fp / f"elevation_{res}.tif").rename("elevation")
    da.attrs = {
        **METADATA,
        'long_name': 'Elevation',
        'units': 'm',
        'source': 'https://lris.scinfo.org.nz/layer/48131-nzdem-north-island-25-metre/ '
                  'https://lris.scinfo.org.nz/layer/48127-nzdem-south-island-25-metre/',
        'comment': 'from field: Band 1'
    }
    da.to_netcdf(res_path / f"NZGLID_elevation_{res}_v{release}.nc")

    # Slope
    fp = DATAPATH / "lris-nzenvds-nz-environmental-data-stack/nzenvds-slope-degrees-v10"
    reproj_match(fp / "nzenvds-slope-degrees-v10.tif", f"WGS84_{res}.tif", fp / f"slope_{res}.tif")
    da = open_raster(fp / f"slope_{res}.tif").rename("slope")
    da = xr.where(da < 0, 0, da)  # correct negative values to 0 (issue likely from resampling)
    da.attrs = {
        **METADATA,
        'long_name': 'Slope',
        'units': 'degrees',
        'source': 'https://lris.scinfo.org.nz/layer/107239-nzenvds-slope-degrees-v10/',
        'comment': 'from field: Band 1'
    }
    da.to_netcdf(res_path / f"NZGLID_slope_{res}_v{release}.nc")
