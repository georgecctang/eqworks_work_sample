
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

##################################################################################
#Note that I have also considered using vectorization calculation, which
#consists of the following steps:
#1. Calculate the distance for each POI and store them in columns (POI-dist columns)
#2. Create 'ClosestDistrance' column with the min value of the POI-dist columns
#3. Create 'ClosestPOI' column with the column name of the POI-dist column with 
#the min value
#4. Drop the POI0dist columns
#
# This approach is a lot faster than using the APPLY method; however, 
# if there are many POI, this approach will create many temp columns which
# the memory may not support.
# So I chose the APPLY method because the memory requirement should be lower.
###################################################################################


#save cleaned POIlist
poi_df.to_csv(interim_data_path + 'POIlistCleaned.csv',index=False)

#save labeled data sample
data_df.to_csv(interim_data_path + 'DataSampleLabeled.csv',index=False)
