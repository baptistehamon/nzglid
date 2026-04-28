"""Python Code of the New Zealand Gridded Land Information Dataset (NZGLID)."""

from pathlib import Path

__author__ = "Baptiste Hamon"
__email__ = "baptiste.hamon@pg.canterbury.ac.nz"
__version__ = "2.0-dev0"
release = __version__.split("-", maxsplit=1)[0]

__all__ = ["release"]

DATAPATH = Path(r"R:\DATA\GIS-NZ")
NZGLID_PATH = Path(r"R:\DATA\NZGLID")
METADATA = {
    'title': f'New Zealand Gridded Land Information Dataset (NZGLID) v{release}',
    'institution': 'Department of Civil and Environmental Engineering, University of Canterbury, Christchurch 8140, NZ',
    'contact': 'Baptiste Hamon: baptiste.hamon@pg.canterbury.ac.nz',
    'reference': 'https://doi.org/10.5281/zenodo.16249351',
    'Convention': 'CF-1.7',
}