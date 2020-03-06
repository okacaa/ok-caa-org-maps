import sys

sys.executable

import pandas as pd
import geopandas as gpd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import GeoJSONDataSource, ColumnDataSource, LinearColorMapper, BasicTickFormatter
from bokeh.io import output_file, show, save
from bokeh.palettes import Category20_18
import json

url = "https://www2.census.gov/geo/tiger/TIGER2018/COUNTY/tl_2018_us_county.zip"
cnty = gpd.read_file(url)

cnty.info()

cnty.loc[:, 'agencies'] = cnty.loc[:, 'NAME'].replace(['Bryan',
                                                       'Carter',
                                                       'Coal',
                                                       'Love',
                                                       'Pontotoc'], 'Big 5') \
                    .replace(['Canadian',
                              'Oklahoma'], 'CAAOKC') \
                    .replace(['Beckham',
                              'Cotton',
                              'Jefferson',
                              'Kiowa',
                              'Roger Mills',
                              'Tillman',
                              'Washita'], 'CADC') \
                    .replace(['Tulsa'], 'CAP Tulsa') \
                    .replace(['Mayes',
                              'Nowata',
                              'Rogers',
                              'Wagoner',
                              'Washington'], 'CARD') \
                    .replace(['Garfield',
                              'Grant'], 'CDSA') \
                    .replace(['Cleveland',
                              'Lincoln',
                              'Logan',
                              'Payne',
                              'Pottawatomie',
                              'Seminole'], 'COCAA') \
                    .replace(['Garvin',
                              'McClain',
                              'Stephens'], 'Delta') \
                    .replace(['Hughes',
                              'McIntosh',
                              'Okfuskee',
                              'Okmulgee'], 'DFCAF') \
                    .replace(['Comanche'], 'GPIF') \
                    .replace(['Atoka',
                              'Johnston',
                              'Marshall',
                              'Murray'], 'INCA') \
                    .replace(['Haskell',
                              'Latimer',
                              'Le Flore',
                              'Muskogee',
                              'Pittsburg',
                              'Sequoyah'], 'KI BOIS') \
                    .replace(['Choctaw',
                              'McCurtain',
                              'Pushmataha'], 'Little Dixie') \
                    .replace(['Adair',
                              'Cherokee',
                              'Craig',
                              'Delaware',
                              'Ottawa'], 'NEOCAA') \
                    .replace(['Alfalfa',
                              'Beaver',
                              'Blaine',
                              'Cimarron',
                              'Custer',
                              'Dewey',
                              'Ellis',
                              'Harper',
                              'Kingfisher',
                              'Major',
                              'Texas',
                              'Woods',
                              'Woodward'], 'Opportunities') \
                    .replace(['Greer',
                              'Harmon',
                              'Jackson'], 'SOCAG') \
                    .replace(['Creek',
                              'Kay',
                              'Noble',
                              'Osage',
                              'Pawnee'], 'UCAP') \
                    .replace(['Caddo',
                              'Grady'], 'WVCAC')

cnty['caa'] = cnty.agencies.replace(['NEOCAA',
 'KI BOIS',
 'CAAOKC',
 'INCA',
 'Opportunities',
 'COCAA',
 'DFCAF',
 'CARD',
 'WVCAC',
 'Big 5',
 'SOCAG',
 'CADC',
 'Little Dixie',
 'UCAP',
 'GPIF',
 'Delta',
 'CAP Tulsa',
 'CDSA'], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])

cnty['phone'] = cnty.agencies.replace(['NEOCAA',
 'KI BOIS',
 'CAAOKC',
 'INCA',
 'Opportunities',
 'COCAA',
 'DFCAF',
 'CARD',
 'WVCAC',
 'Big 5',
 'SOCAG',
 'CADC',
 'Little Dixie',
 'UCAP',
 'GPIF',
 'Delta',
 'CAP Tulsa',
 'CDSA'], ['918-253-4683',
           '918-967-3325',
           '405-232-0199',
           '580-371-2352',
           '580-623-7283',
           '405-275-6060',
           '918-756-2826',
           '918-343-2960',
           '405-224-5831',
           '580-924-5331',
           '580-482-5040',
           '580-335-5588',
           '580-326-3351',
           '918-762-3041',
           '580-353-2364',
           '405-756-1100',
           '918-382-3200',
           '580-242-6131'])

ok = cnty.loc[cnty['STATEFP'] == "40"]

ok.info()

df = ok[['geometry','agencies','NAME','caa','phone']]

#Read data to json.
df_json = json.loads(df.to_json())

#Convert to string-like object.
json_data = json.dumps(df_json)

#Input GeoJSON source that contains features for plotting.
geo_source = GeoJSONDataSource(geojson = json_data)

TOOLS = "pan","wheel_zoom","reset","hover"

TOOLTIPS = [("County","@NAME"),
            ("Agency","@agencies"),
            ("Phone","@phone")]

color_mapper = LinearColorMapper(palette=Category20_18)

#Error: "Models must be owned by only a single document" aka Cannot share geo_sources?
#Must re-run geo_source or reset document on subsequent runs.
geo_source = GeoJSONDataSource(geojson = json_data)

p = figure(title="Community Action Agency Service Areas",
           tools=TOOLS,
           tooltips=TOOLTIPS,
           height=600,
           width=1200,
           x_axis_location=None,
           y_axis_location=None,
           lod_threshold=10)

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('xs',
          'ys',
          source=geo_source,
          fill_color={'field':'caa',
                      'transform':color_mapper},
          fill_alpha=0.7,
          line_color="white",
          line_width=0.5)

#show(p)

save(p)

output_file("C:/Users/zcole/my_projects/okcaa_org_maps/outputs/ok-caa-service-areas.html")