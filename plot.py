import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import json
import math

from shapely.geometry import Point
from geopandas.tools import sjoin
from bokeh.io import curdoc, output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource
from bokeh.models import HoverTool
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis256 as palette

shapefile = './data/ne_110m_admin_0_countries.shp'

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

gdf.columns = ['country_name', 'country_code', 'geometry']

pathtoCSV=r'./covid.csv'

df1 = pd.read_csv(pathtoCSV, encoding='utf8',names = ['country', 'confirmed_day', 'confirmed_month', 'deaths'], index_col=False)

datafile_2='./country_geocodes.csv'
df2 = pd.read_csv(datafile_2, names = ['country', 'latitude', 'longitude'], skiprows = 1)

points = pd.merge(df1, df2, left_on='country',right_on='country', how='left')
points_df = points.drop(['country'],axis=1)

geometry_centroids = [Point(xy) for xy in zip(points_df['longitude'], points_df['latitude'])]

crs = {'init': 'epsg:4326'}

points_gdf = gpd.GeoDataFrame(points_df, crs=crs, geometry=geometry_centroids)

joined = gpd.sjoin(gdf, points_gdf, how="left", op='intersects')

joined.fillna("None", inplace=True)

joined_json = json.loads(joined.to_json())

palette = list(reversed(palette))
max_cases = math.log(df1['confirmed_day'].max())
one_division = (max_cases + 1)/len(palette)
for i in range(len(joined_json['features'])):
    current_day =  joined_json['features'][i]['properties']['confirmed_day']
    if current_day == "None":
        joined_json['features'][i]['properties']['Color'] = "grey"
        continue
    if current_day == 0:
        joined_json['features'][i]['properties']['Color'] = palette[0]
        continue
    joined_json['features'][i]['properties']['Color'] = palette[int(math.log(current_day)/one_division)]

json_data = json.dumps(joined_json)

geosource = GeoJSONDataSource(geojson = json_data)

p = figure(title = 'Big Data Project - Covid Map, 2021',plot_height = 1000 , plot_width = 1600,
           background_fill_color="#2b8cbe", background_fill_alpha=0)
p.title.text_font = "helvetica"
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

patch=p.patches('xs', 'ys', source = geosource, fill_color='Color',
          line_color = '#d95f0e', line_width = 0.35, fill_alpha = 1, hover_fill_color="#fec44f")

p.add_tools(HoverTool(tooltips=[('Country','@country_name'),('Cases per day','@confirmed_day'),
                        ('Cases per month','@confirmed_month'), ('Deaths','@deaths')], renderers=[patch]))

show(p)
