#!/usr/bin/env python
# coding: utf-8

# In[ ]:


############## Import eBird Data ###########

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from scipy import stats

pd.set_option('display.max_columns', None)
df = pd.read_csv('eBirdData.csv', on_bad_lines='skip', delimiter = '\t')


# In[ ]:


############## Specify timeframe ###########

from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

timeframe = df[df['year'].isin([year, year, year])]


# In[ ]:


############ DROP DUPLICATES Per Day TO CREATE BIRDING USER DAYS ###############

df = df.drop_duplicates(
  subset = ['recordedBy', 'eventDate'],
  keep = 'last').reset_index(drop = True)


# In[ ]:


######### COMBINE LAT LON VARIABLES TO SHAPELY POINT OBJECT FOR USE IN ARCGIS ############

from shapely.geometry import Point

df['geometry'] = df.apply(lambda x: Point((float(x.decimalLongitude), float(x.decimalLatitude))), axis=1)

########### ADD GEOMETRY, CLEAN DATA AND DEFINE CRS FOR GIS USE ##############

df_gdf = gpd.GeoDataFrame(df, geometry='geometry')

df_gdf.crs= "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
df_gdf.drop(['decimalLatitude', 'decimalLongitude'], axis=1, inplace=True)

########## CREATE SHAPEFILE ############

df_gdf.to_file('MyGeometries2.shp')

