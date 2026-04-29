"""Rasterise vector data to a 5km and 1km grid."""

import geopandas as gpd

from nzglid import DATAPATH, NZGLID_PATH, RESOLUTION
from nzglid.helpers import rasterise, postprocess_save

CATEGORIES_CODE = {
    'e': 'estuary',
    'i': 'icefield',
    'l': 'lake',
    'q': 'quarry-mine-other_earthworks',
    'r': 'river',
    't': 'urban_area-airport-oxidation_pond',
}

EROSION_CODE = {
    '0': 'negligible',
    '1': 'slight',
    '2': 'moderate',
    '3': 'severe',
    '4': 'very_severe',
    '5': 'extreme',
    **CATEGORIES_CODE
}

FLOOD_CODE = {
    '1': 'nil',
    '2': 'slight',
    '3': 'moderate',
    '4': 'moderately-severe',
    '5': 'severe',
    '6': 'very-severe',
}

LCDB_CODE = {
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

LUM_CODE = {
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

STR_CODE = {
    'T': 'thermic',
    'WM': 'warm-mesic',
    'MM': 'mild-mesic',
    'CM': 'cool-mesic',
    'DM': 'cold-mesic',
    'C': 'cryic',
}

for res, grid in RESOLUTION.items():
    
    res_path = NZGLID_PATH / f"nzglid_{res}"
    res_path.mkdir(exist_ok=True)

    # cation exchange capacity
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-cation-exchange-capacity'
    layer = gpd.read_file(fp / 'fsl-cation-exchange-capacity.shp')
    data = rasterise(layer, "CEC_MOD", grid)
    attrs = {
        'long_name': 'Cation Exchange Capacity',
        'units': 'cmol kg-1',
        'source': 'https://lris.scinfo.org.nz/layer/48099-fsl-cation-exchange-capacity/',
        'description': 'CEC is estimated as weighted averages for the soil profile from 0-0.6 m depth '
        'and expressed in units of centimoles of charge per kg.'
    }
    postprocess_save(data, "cation_exchange_capacity", "CEC_MOD", attrs, res_path, res)

    # drainage class
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-soil-drainage-class'
    layer = gpd.read_file(fp / 'fsl-soil-drainage-class.shp')
    categories = layer['DRAIN_CLAS'].unique().tolist()
    data = rasterise(layer, "DRAIN_CLAS", grid, categorical_enums={'DRAIN_CLAS': categories})
    mapping = {i: v for i, v in enumerate(data['DRAIN_CLAS_categories'].values[:-1])}
    attrs = {
        'long_name': 'Drainage Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48104-fsl-soil-drainage-class/',
        'description': 'Drainage classes are assessed using criteria of soil depth and '
        'duration of water tables inferred from soil colours and mottles.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([f'DrainClass_{v}' for v in mapping.values()])
    }
    postprocess_save(data, "drainage", "DRAIN_CLAS", attrs, res_path, res)

    # depth to slowly permeable horizon
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-depth-to-slowly-permeable-horizon'
    layer = gpd.read_file(fp / 'fsl-depth-to-slowly-permeable-horizon.shp')
    data = rasterise(layer, "DSLO_MOD", grid)
    attrs = {
        'long_name': 'Depth to Slowly Permeable Horizon',
        'units': 'm',
        'source': 'https://lris.scinfo.org.nz/layer/48108-fsl-depth-to-slowly-permeable-horizon/',
        'description': 'Depth to a slowly permeable horizon describes the minimum and maximum depths '
        '(in metres) to a horizon in which the permeability is less than 4mm/hr as measured by '
        'techniques outlined in Griffiths (1985).',
    }
    postprocess_save(data, "depth_slowly_permeable_horizon", "DSLO_MOD", attrs, res_path, res)

    # erosion
    fp = DATAPATH / 'lris-nzlri-nz-land-resource-inventory/nzlri-erosion-type-and-severity'
    layer = gpd.read_file(fp / 'nzlri-erosion-type-and-severity.shp')
    layer = layer.dropna(subset=['ERO1S'])
    categories = layer['ERO1S'].unique().tolist()
    data = rasterise(layer, "ERO1S", grid, categorical_enums={'ERO1S': categories})
    mapping = {i: v for i, v in enumerate(data['ERO1S_categories'].values[:-1])}
    mapping = {k: EROSION_CODE[v] for k, v in mapping.items() if v in EROSION_CODE}
    attrs = {
        'long_name': 'Erosion Severity Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48054-nzlri-erosion-type-and-severity/',
        'description': 'Erosion severity is a classification of the degree of erosion corresponding '
        'to the area of land affected by erosion processes.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([f'ErosionSeverity_{v}' for v in mapping.values()])
    }
    postprocess_save(data, "erosion_severity", "ERO1S", attrs, res_path, res)

    # flood return interval
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-flood-return-interval'
    layer = gpd.read_file(fp / 'fsl-flood-return-interval.shp')
    layer = layer.dropna(subset=['FLOOD_CLAS'])
    categories = layer['FLOOD_CLAS'].unique().tolist()
    data = rasterise(layer, "FLOOD_CLAS", grid, categorical_enums={'FLOOD_CLAS': categories})
    mapping = {i: v for i, v in enumerate(data['FLOOD_CLAS_categories'].values[:-1])}
    mapping = {k: FLOOD_CODE[v] for k, v in mapping.items() if v in FLOOD_CODE}
    attrs = {
        'long_name': 'Flood Return Interval Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48106-fsl-flood-return-interval/',
        'description': 'nil = nil, slight: < 1 in 60 years; moderate: 1 in 20 to 1 in 60 years, '
        'moderately-severe: 1 in 10 to 1 in 20 years, severe: 1 in 5 to 1 in 10 years, '
        'very-severe: > 1 in 5 years.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([f'FloodClass_{v}' for v in mapping.values()])
    }
    postprocess_save(data, "flood_return_interval", "FLOOD_CLAS", attrs, res_path, res)

    # land cover
    fp = DATAPATH / 'lris-lcdb-v60-land-cover-database-version-60-mainland-new-zealand'
    layer = gpd.read_file(fp / 'lcdb-v60-land-cover-database-version-60-mainland-new-zealand.shp')
    categories = layer['Class_2023'].unique().tolist()
    data = rasterise(layer, "Class_2023", grid, categorical_enums={'Class_2023': categories})
    mapping = {i: f"{v}" for i, v in enumerate(data['Class_2023_categories'].values[:-1])}
    mapping = {k: LCDB_CODE[v] for k, v in mapping.items() if v in LCDB_CODE}
    attrs = {
        'long_name': 'Land Cover',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/123148-lcdb-v60-land-cover-database-version-60-mainland-new-zealand/',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([v for v in mapping.values()]),
        'description': 'The New Zealand Land Cover Database (LCDB) is a multi-temporal, '
        'thematic classification of New Zealand\'s land cover.'
    }
    postprocess_save(data, "land_cover", "Class_2023", attrs, res_path, res)

    # land use capability
    fp = DATAPATH / 'lris-nzlri-nz-land-resource-inventory/nzlri-land-use-capability-2021'
    layer = gpd.read_file(fp / 'nzlri-land-use-capability-2021.shp')
    layer = layer.dropna(subset=['lcorrclass'])
    categories = layer['lcorrclass'].unique().tolist()
    data = rasterise(layer, "lcorrclass", grid, categorical_enums={'lcorrclass': categories})
    mapping = {i: v for i, v in enumerate(data['lcorrclass_categories'].values[:-1])}
    mapping = {k: CATEGORIES_CODE[v] if v in CATEGORIES_CODE else f'LUCClassCode_{v}' for k, v in mapping.items()}
    attrs = {
        'long_name': 'Land Use Capability Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48076-nzlri-land-use-capability-2021/',
        'description': 'Land Use Capability (LUC) is a hierarchical classification identifying: '
        'the land\'s general versatility for productive use; the factor most limiting to production; '
        'and a general association of characteristics relevant to productive use (e.g., landform, soil, erosion potential, etc.).',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([v for v in mapping.values()])
    }
    postprocess_save(data, "land_use_capability", "lcorrclass", attrs, res_path, res)

    # LUCAS land use
    fp = DATAPATH / 'mfe-lucas-nz-land-use-map-2020-v005/lucas-nz-land-use-map-2020-v005.shp'
    layer = gpd.read_file(fp)
    categories = layer['LUCID_2020'].unique().tolist()
    data = rasterise(layer, "LUCID_2020", grid, categorical_enums={'LUCID_2020': categories})
    mapping = {i: v[:2] for i, v in enumerate(data['LUCID_2020_categories'].values[:-1])}
    mapping = {k: LUM_CODE[v] if v in LUM_CODE else f'LUMClassCode_{v}' for k, v in mapping.items()}
    attrs = {
        'long_name': 'LUCAS Land Use Map',
        'units': '',
        'source': 'https://data.mfe.govt.nz/layer/117733-lucas-nz-land-use-map-2020-v005/',
        'description': 'The LUCAS NZ Land Use Map 2020 v005 is composed of New Zealand-wide land use classes (12) '
        'nominally at 31 December 1989, 31 December 2007, 31 December 2012, 31 December 2016, and 31 December 2020. '
        'These date boundaries are dictated by the Paris Agreement and former Kyoto Protocol. '
        'The data can therefore be used to create a map at any of the nominal mapping dates depending on what field is symbolised.'
    }
    postprocess_save(data, "lucas_land_use", "LUCID_2020", attrs, res_path, res)

    # particle size classification
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-particle-size-classification'
    layer = gpd.read_file(fp / 'fsl-particle-size-classification.shp')
    categories = layer['PS'].unique().tolist()
    data = rasterise(layer, "PS", grid, categorical_enums={'PS': categories})
    mapping = {i: v for i, v in enumerate(data['PS_categories'].values[:-1])}
    mapping.update({27: 'e', 28: 'i', 29: 'l', 30: 'q', 31: 'r', 32: 't'})
    mapping = {k: CATEGORIES_CODE[v] if v in CATEGORIES_CODE else f'PSClassCode_{v}' for k, v in mapping.items()}
    attrs = {
        'long_name': 'Particle Size Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48112-fsl-particle-size-classification/',
        'description': 'Particle size class describes in broad terms the proportions of sand, silt and '
        'clay in the fine earth fraction of the soil except in the case of skeletal soils '
        '(> 35% coarse fraction) where it applies to the whole soil.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([v for v in mapping.values()])
    }
    postprocess_save(data, "particle_size", "PS", attrs, res_path, res)

    # permeability profile
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-permeability-profile'
    layer = gpd.read_file(fp / 'fsl-permeability-profile.shp')
    categories = layer['PERMEABILI'].unique().tolist()
    data = rasterise(layer, "PERMEABILI", grid, categorical_enums={'PERMEABILI': categories})
    mapping = {i: v for i, v in enumerate(data['PERMEABILI_categories'].values[:-1])}
    attrs = {
        'long_name': 'Permeability Profile',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48105-fsl-permeability-profile/',
        'description': 'Permeability is the rate that water moves through saturated soil. '
        'The permeability of a soil profile is related to potential rooting depth, depth '
        'to a slowly permeable horizon and internal soil drainage.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([f'PermClass_{v}' for v in mapping.values()])
    }
    postprocess_save(data, "permeability_profile", "PERMEABILI", attrs, res_path, res)

    # ph
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-ph'
    layer = gpd.read_file(fp / 'fsl-ph.shp')
    data = rasterise(layer, "PH_MOD", grid)
    attrs = {
        'long_name': 'Minimum pH',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48102-fsl-ph/',
        'description': 'Minimum pH is the minimum pH of the soil profile from 0-0.6 m depth.',
    }
    postprocess_save(data, "ph", "PH_MOD", attrs, res_path, res)

    # phosphate retention
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-phosphate-retention'
    layer = gpd.read_file(fp / 'fsl-phosphate-retention.shp')
    data = rasterise(layer, "PRET_MOD", grid)
    attrs = {
        'long_name': 'Phosphate Retention',
        'units': '%',
        'source': 'https://lris.scinfo.org.nz/layer/48111-fsl-phosphate-retention/',
        'description': 'P retention (phosphate retention) is estimated as weighted averages '
        'for the upper part of the soil profile from 0-0.2 m depth, and expressed as a percentage.',
    }
    postprocess_save(data, "phosphate_retention", "PRET_MOD", attrs, res_path, res)

    # potential rooting depth
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-potential-rooting-depth'
    layer = gpd.read_file(fp / 'fsl-potential-rooting-depth.shp')
    data = rasterise(layer, "PRD_MOD", grid)
    attrs = {
        'long_name': 'Potential Rooting Depth',
        'units': 'm',
        'source': 'https://lris.scinfo.org.nz/layer/48110-fsl-potential-rooting-depth/',
        'description': 'Potential rooting depth describes the depth (in metres) to a layer '
        'that may impede root extension.',
    }
    postprocess_save(data, "potential_rooting_depth", "PRD_MOD", attrs, res_path, res)

    # profile available water
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-profile-available-water'
    layer = gpd.read_file(fp / 'fsl-profile-available-water.shp')
    data = rasterise(layer, "PAW_MOD", grid)
    attrs = {
        'long_name': 'Profile Total Available Water',
        'units': 'mm',
        'source': 'https://lris.scinfo.org.nz/layer/48100-fsl-profile-available-water/',
        'description': 'Profile total available water for the soil profile to a depth of 0.9 m, or to '
        'the potential rooting depth (whichever is the lesser). Values are weighted averages over the '
        'specified profile section (0-0.9 m) and are expressed in units of mm of water.',
    }
    postprocess_save(data, "profile_total_available_water", "PAW_MOD", attrs, res_path, res)

    # profile readily available water
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-profile-readily-available-water'
    layer = gpd.read_file(fp / 'fsl-profile-readily-available-water.shp')
    data = rasterise(layer, "PRAW_MOD", grid)
    attrs = {
        'long_name': 'Profile Readily Available Water',
        'units': 'mm',
        'source': 'https://lris.scinfo.org.nz/layer/48101-fsl-profile-readily-available-water/',
        'description': 'Profile readily available water for the soil profile to a depth of 0.9 m, or to '
        'the potential rooting depth (whichever is the lesser). Values are weighted averages over the '
        'specified profile section (0-0.9 m) and are expressed in units of mm of water.',
    }
    postprocess_save(data, "profile_readily_available_water", "PRAW_MOD", attrs, res_path, res)

    # rock outcrops and surface boulders
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-rock-outcrops-and-surface-boulders'
    layer = gpd.read_file(fp / 'fsl-rock-outcrops-and-surface-boulders.shp')
    data = rasterise(layer, "ROCK_MOD", grid)
    attrs = {
        'long_name': 'Rock Outcrops and Surface Boulders',
        'units': '%',
        'source': 'https://lris.scinfo.org.nz/layer/48113-fsl-rock-outcrops-and-surface-boulders/',
        'description': 'Expression of the percentage of the area of the map units covered by rock '
        'outcrops or surface boulders',
    }
    postprocess_save(data, "rock_outcrops_surface_boulders", "ROCK_MOD", attrs, res_path, res)

    # salinity
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-salinity'
    layer = gpd.read_file(fp / 'fsl-salinity.shp')
    data = rasterise(layer, "SAL_MOD", grid)
    attrs = {
        'long_name': 'Maximum Salinity',
        'units': 'g 100g-1',
        'source': 'https://lris.scinfo.org.nz/layer/48103-fsl-salinity/',
        'description': 'Salinity is measured as percent soluble salts (g/100g soil).',
    }
    postprocess_save(data, "salinity", "SAL_MOD", attrs, res_path, res)

    # soil carbon
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-soil-carbon'
    layer = gpd.read_file(fp / 'fsl-soil-carbon.shp')
    data = rasterise(layer, "CARBON_MOD", grid)
    attrs = {
        'long_name': 'Total Carbon',
        'units': '%',
        'source': 'https://lris.scinfo.org.nz/layer/48098-fsl-soil-carbon/',
        'description': 'Total carbon (organic matter content) is estimated as weighted averages '
        'for the upper part of the soil profile from 0-0.2 m depth.',
    }
    postprocess_save(data, "total_carbon", "CARBON_MOD", attrs, res_path, res)

    # soil temperature regime
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-soil-temperature-regime'
    layer = gpd.read_file(fp / 'fsl-soil-temperature-regime.shp')
    layer = layer.dropna(subset=['TEMP_CLASS'])
    categories = layer['TEMP_CLASS'].unique().tolist()
    data = rasterise(layer, "TEMP_CLASS", grid, categorical_enums={'TEMP_CLASS': categories})
    mapping = {i: v for i, v in enumerate(data['TEMP_CLASS_categories'].values[:-1])}
    mapping = {k: STR_CODE[v] if v in STR_CODE else f'STRClassCode_{v}' for k, v in mapping.items()}
    attrs = {
        'long_name': 'Soil Temperature Regime Class',
        'units': '',
        'source': 'https://lris.scinfo.org.nz/layer/48107-fsl-soil-temperature-regime/',
        'description': 'The soil temperature regime classes relate to the soil temperature at 0.3 m depth.',
        'flag_values': ', '.join([f'{k}' for k in mapping.keys()]),
        'flag_meanings': ' '.join([v for v in mapping.values()]),
    }
    postprocess_save(data, "soil_temperature_regime", "TEMP_CLASS", attrs, res_path, res)

    # topsoil gravel content
    fp = DATAPATH / 'lris-fsl-fundamental-soil-layers/fsl-topsoil-gravel-content'
    layer = gpd.read_file(fp / 'fsl-topsoil-gravel-content.shp')
    data = rasterise(layer, "GRAV_MOD", grid)
    attrs = {
        'long_name': 'Topsoil Gravel Content',
        'units': '%',
        'source': 'https://lris.scinfo.org.nz/layer/48109-fsl-topsoil-gravel-content/',
        'description': 'Topsoil gravel content is estimated as weighted averages for the upper part of the soil profile from 0-0.2 m depth.',
    }
    postprocess_save(data, "topsoil_gravel_content", "GRAV_MOD", attrs, res_path, res)
