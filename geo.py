#connect to db here
import pandas as pd
import geopandas as gpd
import geopy
from sqlalchemy import create_engine
import geoalchemy2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geopandas as gpd
import psycopg2
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import plotly_express as px

import tqdm
from tqdm import tqdm

conn = psycopg2.connect(
    host="localhost",
    database="Nizz0k",
    user="Nizz0k",
    password="")
    
sql = "select * from public.\"Peng\""

engine = create_engine('postgresql://Nizz0k@localhost:5432/public.\"Peng\"')
df = gpd.read_postgis(sql, conn, geom_col="geom")
#print(df.head())
#df.plot()
#plt.show()


df['lon'] = df.geometry.apply(lambda p: p.x)
df['lat'] = df.geometry.apply(lambda p: p.y)
df['geocode'] = df['lat'].map(str) + ', ' + df['lon'].map(str)
#try with zoom 10
locator = Nominatim(user_agent="pengMappingAgent", timeout=10)
rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)
tqdm.pandas()
df['address'] = df['geocode'].progress_apply(rgeocode)
print(df.address.raw)
#df.drop(['lat', 'lon', 'geocode'], axis=1)
df.to_csv('/Users/Nizz0k/Sites/python-spatial/address-pengs.csv', encoding='utf-8-sig')
#df.to_postgis('Peng', engine, if_exists='append')
