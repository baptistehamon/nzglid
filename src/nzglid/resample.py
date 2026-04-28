"""Resample rasters to 5km and 1km resolution."""

import numpy as np
from osgeo import gdal
from pathlib import Path
import rasterio as rio
from rasterio.transform import Affine
from rasterio.warp import reproject, Resampling, calculate_default_transform
import xarray as xr

from nzglid import DATAPATH, NZGLID_PATH, METADATA, release, RESOLUTION

def make_exraster(path: str, res: tuple[float | int, float | int]):
    """
    Make an example raster with specified resolution and WGS84 projection.

    Parameters
    ----------
    path : str
        Path to output raster file.
    res : tuple[float | int, float | int]
        Resolution of output raster in degrees (x, y).
    """

    x = np.arange(166 + res[0] / 2, 179.5, res[0]).round(3)
    y = np.arange(-47.5 + res[1] / 2, -33.5, res[1]).round(3)

    data = np.ones((len(y), len(x)))
    transform = Affine.translation(x[0] - res[0] / 2, y[0] - res[1] / 2) * Affine.scale(res[0], res[1])

    with rio.open(
        path,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        crs="EPSG:4326",
        transform=transform,
    ) as dst:
        dst.write(data, 1)


def reproj_match(infile, matchfile, outfile, method='bilinear'):
    """
    Reproject a file to match the shape and projection of existing raster. 

    From: https://pygis.io/docs/e_raster_resample.html#example-of-co-registering-rasters-with-rasterio
    
    Parameters
    ----------
    infile: str
        Path to source raster to reproject.
    matchfile: str
        Path to raster with desired shape and projection.
    outfile: str
        Path to output raster file.
    method: str
        Resampling method to use. See 'rasterio.warp.Resampling' for options. Default is 'bilinear'.
    """
    resampling = getattr(Resampling, method)

    # open input
    with rio.open(infile) as src:
        # src_transform = src.transform
        
        # open input to match
        with rio.open(matchfile) as match:
            dst_crs = match.crs
            
            # calculate the output transform matrix
            dst_transform, dst_width, dst_height = calculate_default_transform(
                src.crs,     # input CRS
                dst_crs,     # output CRS
                match.width,   # input width
                match.height,  # input height 
                *match.bounds,  # unpacks input outer boundaries (left, bottom, right, top)
            )

        # set properties for output
        dst_kwargs = src.meta.copy()
        dst_kwargs.update({"crs": dst_crs,
                           "transform": dst_transform,
                           "width": dst_width,
                           "height": dst_height,
                           "nodata": src.nodata})
        print("Coregistered to shape:", dst_height,dst_width,'\n Affine',dst_transform)
        # open output
        with rio.open(outfile, "w", **dst_kwargs) as dst:
            # iterate through bands and write using reproject function
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=resampling)

def open_raster(path):
    """Open raster file as xarray DataArray."""
    da = xr.open_dataarray(path, engine="rasterio")
    da = da.rename({"x": "lon", "y": "lat"}).isel(lat=slice(None, None, -1), band=0)
    return da.drop_vars(["band", "spatial_ref"])

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
