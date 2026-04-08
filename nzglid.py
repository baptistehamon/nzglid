from pathlib import Path
import geopandas as gpd
import xarray as xr
from geocube.api.core import make_geocube

import matplotlib.pyplot as plt

DATA_PATH = Path(r"R:\DATA\GIS-NZ")
OUTPUT_PATH = Path(r"R:\DATA\NZGLID")

# RESAMPLING SHP
# define file paths
fp = {
    'LUC': DATA_PATH / 'lris-nzlri-nz-land-resource-inventory' / 'nzlri-land-use-capability',
    'ERO': DATA_PATH / 'lris-nzlri-nz-land-resource-inventory' / 'nzlri-erosion-type-and-severity',
    'PH': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-ph',
    'SAL': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-salinity',
    'CEC': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-cation-exchange-capacity',
    'CARBON': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-soil-carbon',
    'PRET': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-phosphate-retention',
    'GRAV': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-topsoil-gravel-content',
    'ROCK': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-rock-outcrops-and-surface-boulders',
    'PS': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-particle-size-classification',
    'PRD': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-potential-rooting-depth',
    'DSLO': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-depth-to-slowly-permeable-horizon',
    'DRAIN': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-soil-drainage-class',
    'PERM': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-permeability-profile',
    'FLOOD': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-flood-return-interval',
    'TEMP': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-soil-temperature-regime',
    'PAW': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-profile-available-water',
    'PRAW': DATA_PATH / 'lris-fsl-fundamental-soil-layers' / 'fsl-profile-readily-available-water',
    'SLOPE': DATA_PATH / 'lris-nzenvds-nz-environmental-data-stack' / 'nzenvds-slope-degrees-v10',
    'ASPECT': DATA_PATH / 'lris-nzenvds-nz-environmental-data-stack' / 'nzenvds-aspect-degrees-v10',
    'LCDB': DATA_PATH / 'lris-lcdb-v50-land-cover-database-version-50-mainland-new-zealand',
    'LUM': DATA_PATH / 'mfe-lucas-nz-land-use-map-2020-v003',
    'DOC': DATA_PATH / 'lds-protected-areas'
}

# define output parameters
out_crs = 'EPSG:4326'
grid_res = (-0.05, 0.05) # ~ 5km resolution
res = '5km' # approximate resolution
# grid_res = (-0.01, 0.01) # ~ 1km resolution
# res = '1km' # approximate resolution

# define default codes for categorical variables
default_code = {
    'e': 'estuary',
    'i': 'icefield',
    'l': 'lake',
    'q': 'quarry-mine-other_earthworks',
    'r': 'river',
    't': 'urban_area-airport-oxidation_pond',
}

da = []
# luc
layer = gpd.read_file(fp['LUC'] / 'nzlri-land-use-capability.shp')
layer = layer.dropna(subset=['LUC1C'])
cat_list = layer['LUC1C'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["LUC1C"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'LUC1C': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['LUC1C_categories'].values[:-1])}
cat_mapping = {k: default_code[v] if v in default_code else f'LUCClassCode_{v}' for k, v in cat_mapping.items()}
da_ = da_['LUC1C'].where(da_['LUC1C'] != -1).rename('land_use_capability')
da_.attrs = {
    # 'title': 'NZLRI Land Use Capability 2021',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Land Use Capability Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48076-nzlri-land-use-capability-2021/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'Land Use Capability (LUC) is a hierarchical classification identifying: '
    'the land\'s general versatility for productive use; the factor most limiting to production; '
    'and a general association of characteristics relevant to productive use (e.g., landform, soil, erosion potential, etc.).',
    'comment': 'from field: from field: LUC1C'
}
da.append(da_)

# erosion
ero_code = {
    '0': 'negligible',
    '1': 'slight',
    '2': 'moderate',
    '3': 'severe',
    '4': 'very_severe',
    '5': 'extreme',
    **default_code
}
layer = gpd.read_file(fp['ERO'] / 'nzlri-erosion-type-and-severity.shp')
layer = layer.dropna(subset=['ERO1S'])
cat_list = layer['ERO1S'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["ERO1S"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'ERO1S': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['ERO1S_categories'].values[:-1])}
cat_mapping = {k: ero_code[v] for k, v in cat_mapping.items() if v in ero_code}
da_ = da_['ERO1S'].where(da_['ERO1S'] != -1).rename('erosion_severity')
da_.attrs = {
    # 'title': 'NZLRI Erosion Type and Severity',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Erosion Severity Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48054-nzlri-erosion-type-and-severity/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'Erosion severity is a classification of the degree of erosion corresponding '
    'to the area of land affected by erosion processes.',
    'comment': 'from field: ERO1S'
}
da.append(da_)

# ph
layer = gpd.read_file(fp['PH'] / 'fsl-ph.shp')
da_ = make_geocube(
    layer,
    measurements=["PH_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['PH_MOD'].rename('ph')
da_.attrs = {
    # 'title': 'FSL pH',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Minimum pH',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48102-fsl-ph/',
    'description': '',
    'comment': 'from field: PH_MOD'
}
da.append(da_)

# salinity
layer = gpd.read_file(fp['SAL'] / 'fsl-salinity.shp')
da_ = make_geocube(
    layer,
    measurements=["SAL_MOD"],
    resolution= grid_res,
    output_crs= out_crs,
)
da_ = da_['SAL_MOD'].rename('salinity')
da_.attrs = {
    # 'title': 'FSL Salinity',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Maximum Salinity',
    'units': 'g 100g-1',
    'source': 'https://lris.scinfo.org.nz/layer/48103-fsl-salinity/',
    'description': 'Salinity is measured as percent soluble salts (g/100g soil).',
    'comment': 'from field: SAL_MOD'
}
da.append(da_)

# cation exchange capacity
layer = gpd.read_file(fp['CEC'] / 'fsl-cation-exchange-capacity.shp')
da_ = make_geocube(
    layer,
    measurements=["CEC_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['CEC_MOD'].rename('cation_exchange_capacity')
da_.attrs = {
    # 'title': 'FSL Cation Exchange Capacity',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Cation Exchange Capacity',
    'units': 'cmol kg-1',
    'source': 'https://lris.scinfo.org.nz/layer/48099-fsl-cation-exchange-capacity/',
    'description': 'CEC is estimated as weighted averages for the soil profile from 0-0.6 m depth '
    'and expressed in units of centimoles of charge per kg.',
    'comment': 'from field: CEC_MOD'
}
da.append(da_)

# soil carbon
layer = gpd.read_file(fp['CARBON'] / 'fsl-soil-carbon.shp')
da_ = make_geocube(
    layer,
    measurements=["CARBON_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['CARBON_MOD'].rename('total_carbon')
da_.attrs = {
    # 'title': 'FSL Soil Carbon',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Total Carbon',
    'units': '%',
    'source': 'https://lris.scinfo.org.nz/layer/48098-fsl-soil-carbon/',
    'description': 'Total carbon (organic matter content) is estimated as '
    'weighted averages for the upper part of the soil profile from 0-0.2 m depth.',
    'comment': 'from field: CARBON_MOD'
}
da.append(da_)

# phosphate retention
layer = gpd.read_file(fp['PRET'] / 'fsl-phosphate-retention.shp')
da_ = make_geocube(
    layer,
    measurements=["PRET_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['PRET_MOD'].rename('phosphate_retention')
da_.attrs = {
    # 'title': 'FSL Phosphate Retention',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Phosphate Retention',
    'units': '%',
    'source': 'https://lris.scinfo.org.nz/layer/48111-fsl-phosphate-retention/',
    'description': 'P retention (phosphate retention) is estimated as weighted averages '
    'for the upper part of the soil profile from 0-0.2 m depth, and expressed as a percentage.',
    'comment': 'from field: PRET_MOD',
}
da.append(da_)

# gravel content
layer = gpd.read_file(fp['GRAV'] / 'fsl-topsoil-gravel-content.shp')
da_ = make_geocube(
    layer,
    measurements=["GRAV_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['GRAV_MOD'].rename('topsoil_gravel_content')
da_.attrs = {
    # 'title': 'FSL Topsoil Gravel Content',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Topsoil Gravel Content',
    'units': '%',
    'source': 'https://lris.scinfo.org.nz/layer/48109-fsl-topsoil-gravel-content/',
    'description': '',
    'comment': 'from field: GRAV_MOD'
}
da.append(da_)

# rock outcrops and surface boulders
layer = gpd.read_file(fp['ROCK'] / 'fsl-rock-outcrops-and-surface-boulders.shp')
da_ = make_geocube(
    layer,
    measurements=["ROCK_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['ROCK_MOD'].rename('rock')
da_.attrs = {
    # 'title': 'FSL Rock Outcrops and Surface Boulders',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Rock Outcrops and Surface Boulders',
    'units': '%',
    'source': 'https://lris.scinfo.org.nz/layer/48113-fsl-rock-outcrops-and-surface-boulders/',
    'description': 'Expression of the percentage of the area of the map units covered by rock '
    'outcrops or surface boulders',
    'comment': 'from field: ROCK_MOD'
}
da.append(da_)

# particle size
layer = gpd.read_file(fp['PS'] / 'fsl-particle-size-classification.shp')
cat_list = layer['PS'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["PS"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'PS': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['PS_categories'].values[:-1])}
cat_mapping.update({27: 'e', 28: 'i', 29: 'l', 30: 'q', 31: 'r', 32: 't'})
cat_mapping = {k: default_code[v] if v in default_code else f'PSClassCode_{v.replace('/', '-')}' for k, v in cat_mapping.items()}
da_ = da_['PS'].where(da_['PS'] != -1).rename('particle_size')
da_.attrs = {
    # 'title': 'FSL Particle Size Classification',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Particle Size Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48112-fsl-particle-size-classification/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'Particle size class describes in broad terms the proportions of sand, silt and '
    'clay in the fine earth fraction of the soil except in the case of skeletal soils '
    '(> 35% coarse fraction) where it applies to the whole soil.',
    'comment': 'from field: PS'
}
da.append(da_)

# potential rooting depth
layer = gpd.read_file(fp['PRD'] / 'fsl-potential-rooting-depth.shp')
da_ : xr.Dataset = make_geocube(
    layer,
    measurements=["PRD_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['PRD_MOD'].rename('potential_rooting_depth')
da_.attrs = {
    # 'title': 'FSL Potential Rooting Depth',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Potential Rooting Depth',
    'units': 'm',
    'source': 'https://lris.scinfo.org.nz/layer/48110-fsl-potential-rooting-depth/',
    'description': 'Potential rooting depth describes the depth (in metres) to a layer '
    'that may impede root extension.',
    'comment': 'from field: PRD_MOD'
}
da.append(da_)

# depth to slowly permeable horizon
layer = gpd.read_file(fp['DSLO'] / 'fsl-depth-to-slowly-permeable-horizon.shp')
da_ = make_geocube(
    layer,
    measurements=["DSLO_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['DSLO_MOD'].rename('depth_slowly_permeable_horizon')
da_.attrs = {
    # 'title': 'FSL Depth to Slowly Permeable Horizon',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Depth to Slowly Permeable Horizon',
    'units': 'm',
    'source': 'https://lris.scinfo.org.nz/layer/48108-fsl-depth-to-slowly-permeable-horizon/',
    'description': 'Depth to a slowly permeable horizon describes the minimum and maximum depths '
    '(in metres) to a horizon in which the permeability is less than 4mm/hr as measured by '
    'techniques outlined in Griffiths (1985).',
    'comment': 'from field: DSLO_MOD'
}
da.append(da_)

# drainage class
layer = gpd.read_file(fp['DRAIN'] / 'fsl-soil-drainage-class.shp')
cat_list = layer['DRAIN_CLAS'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["DRAIN_CLAS"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'DRAIN_CLAS': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['DRAIN_CLAS_categories'].values[:-1])}
da_ = da_['DRAIN_CLAS'].where(da_['DRAIN_CLAS'] != -1).rename('drainage')
da_.attrs = {
    # 'title': 'FSL Soil Drainage Class',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Drainage Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48104-fsl-soil-drainage-class/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([f'DrainClass_{v}' for v in cat_mapping.values()]),
    'description': 'Drainage classes are assessed using criteria of soil depth and '
    'duration of water tables inferred from soil colours and mottles.',
    'comment': 'from field: DRAIN_CLAS'
}
da.append(da_)

# permeability profile
layer = gpd.read_file(fp['PERM'] / 'fsl-permeability-profile.shp')
cat_list = layer['PERMEABILI'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["PERMEABILI"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'PERMEABILI': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['PERMEABILI_categories'].values[:-1])}
da_ = da_['PERMEABILI'].where(da_['PERMEABILI'] != -1).rename('permeability_profile')
da_.attrs = {
    # 'title': 'FSL Permeability Profile',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Permeability Profile',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48105-fsl-permeability-profile/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([f'PermClass_{v}' for v in cat_mapping.values()]),
    'description': 'Permeability is the rate that water moves through saturated soil. '
    'The permeability of a soil profile is related to potential rooting depth, depth '
    'to a slowly permeable horizon and internal soil drainage.',
    'comment': 'from field: PERMEABILI'
}
da.append(da_)

# flood return interval
flood_code = {
    '1': 'nil',
    '2': 'slight',
    '3': 'moderate',
    '4': 'moderately-severe',
    '5': 'severe',
    '6': 'very-severe'
}
layer = gpd.read_file(fp['FLOOD'] / 'fsl-flood-return-interval.shp')
layer = layer.dropna(subset=['FLOOD_CLAS'])
cat_list = layer['FLOOD_CLAS'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["FLOOD_CLAS"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'FLOOD_CLAS': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['FLOOD_CLAS_categories'].values[:-1])}
cat_mapping = {k: flood_code[v] for k, v in cat_mapping.items()}
da_ = da_['FLOOD_CLAS'].where(da_['FLOOD_CLAS'] != -1).rename('flood_return_interval')
da_.attrs = {
    # 'title': 'FSL Flood Return Interval',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Flood Return Interval Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48106-fsl-flood-return-interval/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([f'FloodClass_{v}' for v in cat_mapping.values()]),
    'description': 'nil = nil, slight: < 1 in 60 years; moderate: 1 in 20 to 1 in 60 years, '
    'moderately-severe: 1 in 10 to 1 in 20 years, severe: 1 in 5 to 1 in 10 years, '
    'very-severe: > 1 in 5 years.',
    'comment': 'from field: FLOOD_CLAS',
}
da.append(da_)

# soil temperature regime
str_code = {
    'T': 'thermic',
    'WM': 'warm-mesic',
    'MM': 'mild-mesic',
    'CM': 'cool-mesic',
    'DM': 'cold-mesic',
    'C': 'cryic',
}
layer = gpd.read_file(fp['TEMP'] / 'fsl-soil-temperature-regime.shp')
layer = layer.dropna(subset=['TEMP_CLASS'])
cat_list = layer['TEMP_CLASS'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["TEMP_CLASS"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'TEMP_CLASS': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['TEMP_CLASS_categories'].values[:-1])}
cat_mapping = {k: str_code[v] for k, v in cat_mapping.items()}
da_ = da_['TEMP_CLASS'].where(da_['TEMP_CLASS'] != -1).rename('soil_temperature_regime')
da_.attrs = {
    # 'title': 'FSL Soil Temperature Regime',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Temperature Regime Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/48107-fsl-soil-temperature-regime/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'The soil temperature regime classes relate to the soil temperature at 0.3 m depth.',
    'comment': 'from field: TEMP_CLASS'
}
da.append(da_)

# profile available water
layer = gpd.read_file(fp['PAW'] / 'fsl-profile-available-water.shp')
da_ = make_geocube(
    layer,
    measurements=["PAW_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['PAW_MOD'].rename('profile_total_available_water')
da_.attrs = {
    # 'title': 'FSL Profile Available Water',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Profile Total Available Water',
    'units': 'mm',
    'source': 'https://lris.scinfo.org.nz/layer/48100-fsl-profile-available-water/',
    'description': 'Profile total available water for the soil profile to a depth of 0.9 m, or to '
    'the potential rooting depth (whichever is the lesser). Values are weighted averages over the '
    'specified profile section (0-0.9 m) and are expressed in units of mm of water.',
    'comment': 'from field: PAW_MOD'
}
da.append(da_)

# profile readily available water
layer = gpd.read_file(fp['PRAW'] / 'fsl-profile-readily-available-water.shp')
da_ = make_geocube(
    layer,
    measurements=["PRAW_MOD"],
    resolution= grid_res,
    output_crs= out_crs
)
da_ = da_['PRAW_MOD'].rename('profile_readily_available_water')
da_.attrs = {
    # 'title': 'FSL Profile Readily Available Water',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Profile Readily Available Water',
    'units': 'mm',
    'source': 'https://lris.scinfo.org.nz/layer/48101-fsl-profile-readily-available-water/',
    'description': 'Profile readily available water for the soil profile to a depth of 0.9 m, or to '
    'the potential rooting depth (whichever is the lesser). Values are weighted averages over the '
    'specified profile section (0-0.9 m) and are expressed in units of mm of water',
    'comment': 'from field: PRAW_MOD'
}
da.append(da_)

# slope
da_ = xr.open_dataarray(fp['SLOPE'] / f'nzenvds-slope-degrees-v10-NZ{res}.tif' , engine='rasterio')
da_ = da_.sel(band=1).drop_vars('band').rename('slope')
da_.attrs = {
    # 'title': 'NZEnvDS Slope',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Slope',
    'units': 'degrees',
    'source': 'https://lris.scinfo.org.nz/layer/107239-nzenvds-slope-degrees-v10/',
    'description': '',
    'comment': 'from field: Band 1'
}
da.append(da_)

# aspect
da_ = xr.open_dataarray(fp['ASPECT'] / f'nzenvds-aspect-degrees-v10-NZ{res}.tif', engine='rasterio')
da_ = da_.sel(band=1).drop_vars('band').rename('aspect')
da_.attrs = {
    # 'title': 'NZEnvDS Aspect',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Aspect',
    'units': 'degrees',
    'source': 'https://lris.scinfo.org.nz/layer/105706-nzenvds-aspect-degrees-v10/',
    'description': '',
    'comment': 'from field: Band 1'
}
da.append(da_)

# lcdb
lcdb_code = {
    '0': 'not-land',
    '1': 'built_up_area-settlement',
    '2': 'urban_parkland-open_space',
    '5': 'transport_infrastructure',
    '6': 'surface_mine_dump',
    '10': 'sand-gravel',
    '12': 'landslide',
    '14': 'permanent_snow-ice',
    '15': 'alpine_grass-herbfield',
    '16': 'gravel-rock',
    '20': 'lake-pond',
    '21': 'river',
    '22': 'estuarine_open_water',
    '30': 'short_rotation_cropland',
    '33': 'orchards-vineyards-other_perennial_crops',
    '40': 'high_producing_exotic_grassland',
    '41': 'low-producing_grassland',
    '43': 'tall_tussock_grassland',
    '44': 'depleted_grassland',
    '45': 'herbaceous_freshwater_vegetation',
    '46': 'herbaceous_saline_vegetation',
    '47': 'flaxland',
    '50': 'fernland',
    '51': 'gorse-broom',
    '52': 'manuka-kanuka',
    '54': 'broadleaved_indigenous_hardwoods',
    '55': 'sub_alpine_shrubland',
    '56': 'mixed_exotic_shrubland',
    '58': 'matagouri-grey_scrub',
    '64': 'forest_harvested',
    '68': 'deciduous_hardwoods',
    '69': 'indigenous_forest',
    '70': 'mangrove',
    '71': 'exotic_forest',
    '80': 'peat_shrubland-Chatham_Is',
    '81': 'dune_shrubland-Chatham_Is',
}
layer = gpd.read_file(fp['LCDB'] / 'lcdb-v50-land-cover-database-version-50-mainland-new-zealand.shp')
cat_list = layer['Class_2018'].astype(str).unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["Class_2018"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'Class_2018': cat_list}
)
cat_mapping = {i: v for i, v in enumerate(da_['Class_2018_categories'].values[:-1])}
cat_mapping = {k: lcdb_code[v] for k, v in cat_mapping.items() if v in lcdb_code}
da_ = da_['Class_2018'].where(da_['Class_2018'] != -1).rename('land_cover')
da_.attrs = {
    # 'title': 'LCDB v5.0 - Land Cover Database version 5.0, Mainland, New Zealand',
    # 'institution': 'Landcare Research NZ Ltd',
    'long_name': 'Land Cover Class',
    'units': '',
    'source': 'https://lris.scinfo.org.nz/layer/104400-lcdb-v50-land-cover-database-version-50-mainland-new-zealand/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'The New Zealand Land Cover Database (LCDB) is a multi-temporal, '
    'thematic classification of New Zealand\'s land cover.',
    'comment': 'from field: Class_2018'
}
da.append(da_)

# lucas lum
lum_code = {
    '71': 'natural_forest',
    '72': 'pre_1990_planted_forest',
    '73': 'post_1989_planted_forest',
    '74': 'grassland-woody_biomass',
    '75': 'grassland-high_producing',
    '76': 'grassland-low_producing',
    '77': 'cropland-perennial',
    '78': 'cropland-annual',
    '79': 'wetland-open_water',
    '80': 'wetland-vegetated_non_forest',
    '81': 'settlements',
    '82': 'other',
}
layer = gpd.read_file(fp['LUM'])
cat_list = layer['LUCID_2020'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["LUCID_2020"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'LUCID_2020': cat_list}
)
cat_mapping = {i: v[:2] for i, v in enumerate(da_['LUCID_2020_categories'].values[:-1])}
cat_mapping = {k: lum_code[v] for k, v in cat_mapping.items()}
da_ = da_['LUCID_2020'].where(da_['LUCID_2020'] != -1).rename('lucas_land_use')
da_.attrs = {
    # 'title': 'LUCAS NZ Land Use Map 2020 v003',
    # 'institution': 'Ministry for the Environment',
    'long_name': 'Land Use Class',
    'units': '',
    'source': 'https://data.mfe.govt.nz/layer/117733-lucas-nz-land-use-map-2020-v003/',
    'flag_values': ', '.join([f'{k}' for k in range(len(cat_mapping))]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'The LUCAS NZ Land Use Map 2020 v003 is composed of New Zealand-wide land use classes (12) '
    'at 31 December 2020. These date boundaries are dictated by the Paris Agreement and former Kyoto Protocol. '
    'The data can therefore be used to create a map at any of the nominal mapping dates depending on what field is symbolised.',
    'comment': 'from field: LUCID_2020'
}
da.append(da_)

# protected areas
layer = gpd.read_file(fp['DOC'] / 'protected-areas-mainland.shp')
layer = layer.dropna(subset=['Type'])
cat_list = layer['type'].unique().tolist()
da_ = make_geocube(
    layer,
    measurements=["type"],
    resolution= grid_res,
    output_crs= out_crs,
    categorical_enums= {'type': cat_list}
)
cat_mapping = {i: v.lower() for i, v in enumerate(da_['type_categories'].values[:-1])}
da_ = da_['type'].where(da_['type'] != -1).rename('doc_protected_area')
da_.attrs = {
    # 'title': 'DOC Public Conservation Areas',
    # 'institution': 'Department of Conservation',
    'long_name': 'DOC Protected Area Type',
    'units': '',
    'source': 'https://data.linz.govt.nz/layer/53564-protected-areas/',
    'flag_values': ', '.join([f'{k}' for k in cat_mapping.keys()]),
    'flag_meanings': ' '.join([v for v in cat_mapping.values()]),
    'description': 'This Protected Area Layer contains land and marine areas, most of which '
    'are administered by the Department of Conservation Te Papa Atawhai (DOC) and are protected '
    'by the Conservation, Reserves, National Parks, Marine Mammal and Marine Reserves Acts.'
}
da.append(da_)

# fixing coords issues
for i in da:
    i['x'] = i['x'].round(3)
    i['y'] = i['y'].round(3)

ds = xr.merge(da).drop_vars(['spatial_ref'])
ds = ds.rename({'x': 'lon', 'y': 'lat'})
ds.attrs = {
    'title': 'New Zealand Gridded Land Information Dataset (NZGLID)',
    'institution': 'Department of Civil and Natural Resources Engineering, University of Canterbury, Christchurch 8140, NZ',
    'contact': 'Baptiste Hamon: baptiste.hamon@pg.canterbury.ac.nz',
    'reference': 'https://doi.org/10.5281/zenodo.16249351',
    'Convention': 'CF-1.7',
}


# Save files and dataset
for var in ds.data_vars:
    ds_ = ds[var].to_dataset(name=var)
    if var == 'doc_protected_area':
        ds_.to_netcdf(fp['DOC'] / f'protected-areas-mainland_NZ{res}.nc')
    else:
        ds_.attrs = ds.attrs
        ds_.to_netcdf(OUTPUT_PATH / f'nzglid_{res}/NZGLID_{var.replace('_', '-')}_NZ{res}.nc')
ds.drop_vars('doc_protected_area').to_netcdf(OUTPUT_PATH / f'New-Zealand-Gridded-Land-Information-Dataset_NZ{res}.nc')

# -------------------------------------------------- #
# RESAMPLE SLOPE & ASPECT RASTERS
# import rasterio

# EXFILE_PATH = r"c:\Users\bha170\Database\CLIMATE-Data\NEX-GDDP-CMIP6\NEX-GDDP-CMIP6_NZ\NEX-GDDP-CMIP6_Example_file-0deg05.tif"
# out_fn = r"c:\Users\bha170\Database\CLIMATE-Data\NEX-GDDP-CMIP6\NEX-GDDP-CMIP6_NZ\NEX-GDDP-CMIP6_Example_file-0deg01.tif"
# rst = rasterio.open(EXFILE_PATH)
# meta = rst.meta.copy()
# meta.update(compress='lzw')
# rst.close()

# # TERRAIN
# import rasterio
# from rasterio.plot import show
# from rasterio.enums import Resampling


# DATA_PATH = Path(r'C:\Users\bha170\Database\GIS-Data')
# SLOPE_PATH = DATA_PATH / 'lris-nzenvds-slope-degrees-v10-GTiff'
# ASPECT_PATH = DATA_PATH / 'lris-nzenvds-aspect-degrees-v10-GTiff'
# EXFILE_PATH = r"C:\Users\bha170\Database\CLIM-Data\GDDP-CMIP6\NEX-GDDP-CMIP6_Example_file.tif"

# slope_fp = [f for f in SLOPE_PATH.glob('*.tif')][2]
# aspect_fp = [f for f in ASPECT_PATH.glob('*.tif')][0]
# slope = rasterio.open(slope_fp)
# aspect = rasterio.open(aspect_fp)
# exfile = rasterio.open(EXFILE_PATH)

# factor = 1/200
# with rasterio.open(slope_fp) as dst:

#     # resample data to target shape
#     data = dst.read(
#         out_shape=(
#             dst.count,
#             int(dst.height * factor),
#             int(dst.width * factor)
#         ),
#         resampling=Resampling.bilinear
#     )

#     # scale image transform
#     transform = dst.transform * dst.transform.scale(
#         (dst.width / data.shape[-1]),
#         (dst.height / data.shape[-2])
#     )

# out_meta = dst.meta.copy()
# out_meta.update({'driver':'GTiff',
#                  'height': data.shape[1],
#                  'width': data.shape[2],
#                  'transform': transform})

# with rasterio.open('PastureYield_Irrigated200NCap-5km.tif', 'w', **out_meta) as dst:
#     dst.write(data)



# from rasterio.warp import reproject, Resampling, calculate_default_transform
# import rasterio
# def reproj_match(infile, match, outfile):
#     """Reproject a file to match the shape and projection of existing raster. 
    
#     Parameters
#     ----------
#     infile : (string) path to input file to reproject
#     match : (string) path to raster with desired shape and projection 
#     outfile : (string) path to output file tif
#     """
#     # open input
#     with rasterio.open(infile) as src:
#         src_transform = src.transform
        
#         # open input to match
#         with rasterio.open(match) as match:
#             dst_crs = match.crs
            
#             # calculate the output transform matrix
#             dst_transform, dst_width, dst_height = calculate_default_transform(
#                 src.crs,     # input CRS
#                 dst_crs,     # output CRS
#                 match.width,   # input width
#                 match.height,  # input height 
#                 *match.bounds,  # unpacks input outer boundaries (left, bottom, right, top)
#             )

#         # set properties for output
#         dst_kwargs = src.meta.copy()
#         dst_kwargs.update({"crs": dst_crs,
#                            "transform": dst_transform,
#                            "width": dst_width,
#                            "height": dst_height,
#                            "nodata": src.nodata})
#         print("Coregistered to shape:", dst_height,dst_width,'\n Affine',dst_transform)
#         # open output
#         with rasterio.open(outfile, "w", **dst_kwargs) as dst:
#             # iterate through bands and write using reproject function
#             for i in range(1, src.count + 1):
#                 reproject(
#                     source=rasterio.band(src, i),
#                     destination=rasterio.band(dst, i),
#                     src_transform=src.transform,
#                     src_crs=src.crs,
#                     dst_transform=dst_transform,
#                     dst_crs=dst_crs,
#                     resampling=Resampling.nearest)