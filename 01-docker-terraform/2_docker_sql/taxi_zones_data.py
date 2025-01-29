import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

os.system("wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")

df_zones = pd.read_csv("taxi_zone_lookup.csv")
df_zones.to_sql(name='zones', con=engine, if_exists='replace')