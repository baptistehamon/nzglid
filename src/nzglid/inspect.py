"""Inspect differences between versions."""

import matplotlib.pyplot as plt
import xarray as xr

from nzglid import NZGLID_PATH, RESOLUTION, release

VARSNAMES = {
    # "new": "old"; if same name, set to 1; if new variable, set to None
    "aspect": 1,
    "cation_exchange_capacity": 1,
    "depth_slowly_permeable_horizon": 1,
    "drainage": 1,
    "elevation": None, # new variable
    "erosion_severity": 1,
    "flood_return_interval": 1,
    "land_cover": 1,
    "land_use_capability": 1,
    "lucas_land_use": 1,
    "particle_size": 1,
    "permeability_profile": 1,
    "ph": 1,
    "phosphate_retention": 1,
    "potential_rooting_depth": 1,
    "profile_readily_available_water": 1,
    "profile_total_available_water": 1,
    "rock_outcrops_surface_boulders": "rock",
    "salinity": 1,
    "slope": 1,
    "soil_temperature_regime": 1,
    "topsoil_gravel_content": 1,
    "total_carbon_content": 1,
}

old_release = "1.1"

differences = {}
for res in RESOLUTION:

    differences[res] = {}

    new  = xr.open_dataset(NZGLID_PATH / f"NZGLID_{res}_v{release}.nc")
    old = xr.open_dataset(NZGLID_PATH.parent / f"v{old_release}" / f"New-Zealand-Gridded-Land-Information-Dataset_NZ{res}.nc")

    for v in list(new.data_vars):
        old_v = VARSNAMES[v]
        if old_v is None:
            print(f"{v} is new in v{release}")
            continue
        elif old_v == 1:
            old_v = v

        diff = new[v] - old[old_v]

        if diff.max() != 0:
            differences[res][v] = diff
        
        diff.plot()
        plt.title(f"{v} - {res}")
        plt.show()
