from pangeo_forge_recipes.recipes import XarrayZarrRecipe
from pangeo_forge_recipes.patterns import ConcatDim, FilePattern
import pandas as pd

#TODO: replace with ENV vars
username = password = 'pangeo@developmentseed.org'

def make_filename(time):
    input_url_pattern = (
        "https://arthurhouhttps.pps.eosdis.nasa.gov/gpmdata/{yyyy}/{mm}/{dd}/imerg/3B-HHR.MS.MRG.3IMERG.{yyyymmdd}-S{sh}{sm}00-E{eh}{em}59.{MMMM}.V06B.HDF5"
    ).format(
        yyyy=time.strftime("%Y"),
        mm = time.strftime("%m"),
        dd = time.strftime("%d"),
        yyyymmdd=time.strftime("%Y%m%d"),
        sh = time.strftime("%H"),
        sm = time.strftime("%M"),
        eh = time.strftime("%H"),
        em = (time+pd.Timedelta("29 min")).strftime("%M"),
        MMMM = f'{(time.hour*60 + time.minute):04}'
    )
    return input_url_pattern

time_concat_dim = ConcatDim("time", dates, nitems_per_file=1)
pattern = FilePattern(make_filename, time_concat_dim)

recipe = XarrayZarrRecipe(
    pattern, 
    xarray_open_kwargs={'group': 'Grid', 'drop_variables': ['time_bnds', 'lon_bnds', 'lat_bnds']},
    fsspec_open_kwargs={'auth': aiohttp.BasicAuth(username, password)},
    inputs_per_chunk=1
)