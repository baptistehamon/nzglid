"""Resample rasters to 5km and 1km resolution."""

import numpy as np
import rasterio as rio
from rasterio.transform import Affine

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
