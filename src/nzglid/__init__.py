"""Python Code of the New Zealand Gridded Land Information Dataset (NZGLID)."""

from pathlib import Path

__author__ = "Baptiste Hamon"
__email__ = "baptiste.hamon@pg.canterbury.ac.nz"
__version__ = "2.0-dev0"
release = __version__.split("-", maxsplit=1)[0]

__all__ = ["release"]

DATAPATH = Path(r"R:\DATA\GIS-NZ")
NZGLID_PATH = Path(fr"R:\DATA\NZGLID\v{release}")
NZGLID_PATH.mkdir(exist_ok=True)
METADATA = {
    'title': f'New Zealand Gridded Land Information Dataset (NZGLID) v{release}',
    'institution': 'Department of Civil and Environmental Engineering, University of Canterbury, Christchurch 8140, NZ',
    'contact': 'Baptiste Hamon: baptiste.hamon@pg.canterbury.ac.nz',
    'reference': 'https://doi.org/10.5281/zenodo.16249350',
    'Convention': 'CF-1.7',
}

RESOLUTION = {
    "5km": (0.05, 0.05),
    "1km": (0.01, 0.01),
}

VECTOR_VARS = [
    'cation_exchange_capacity',
    'drainage',
    'depth_slowly_permeable_horizon',
    'erosion_severity',
    'flood_return_interval',
    'land_cover',
    'land_use_capability',
    'lucas_land_use',
    'particle_size',
    'permeability_profile',
    'ph',
    'phosphate_retention',
    'potential_rooting_depth',
    'profile_readily_available_water',
    'profile_total_available_water',
    'rock_outcrops_surface_boulders',
    'salinity',
    'soil_temperature_regime',
    'topsoil_gravel_content',
    'total_carbon_content',
]

RASTER_VARS = [
    "aspect",
    "elevation",
    "slope",
]