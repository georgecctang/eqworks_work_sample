
import pandas as pd
import numpy as np

#import haversine function to calculate distances
from sys import path
from os import getcwd
path.append(getcwd() + "/submission/function")
from haversine_function import haversine


raw_data_path = 'data/raw/'
interim_data_path = 'data/interim/'

#import CLeaned Data Sample Table
data_df = pd.read_csv(interim_data_path + 'DataSampleCleaned.csv')

# import POI data table
poi_df = pd.read_csv(raw_data_path + 'POIlist.csv')

# Clean column names
poi_df.columns  = list(map(lambda x: str.strip(x), poi_df.columns))

# Drop duplicates (keep first) 
poi_df.drop_duplicates(['Latitude','Longitude'],inplace=True)
poi_df.reset_index(inplace =True, drop=True)

#create list of POI lat & lon
POI_lat_lon = [(lat, lon) for lat,lon in zip(poi_df.Latitude, poi_df.Longitude)]
POI_index_dict = poi_df.POIID.to_dict()

#Use apply method to find the closest distance
data_df['ClosestDistance'] = data_df[['Latitude','Longitude']].apply(lambda x:
 (np.array([haversine(x['Latitude'], x['Longitude'], lat, lon) for lat, lon in
 POI_lat_lon]).min()), axis=1)

#Use apply method to find the POIID with closest distance
data_df['ClosestPOI'] = data_df[['Latitude','Longitude']].apply(lambda x:
(np.array([haversine(x['Latitude'], x['Longitude'], lat, lon)
for lat, lon in POI_lat_lon]).argmin()), axis=1).map(POI_index_dict)

#save cleaned POIlist
poi_df.to_csv(interim_data_path + 'POIlistCleaned.csv',index=False)

#save labeled data sample
data_df.to_csv(interim_data_path + 'DataSampleLabeled.csv',index=False)
