import pandas as pd

interm_data_path = 'data/interim/'
raw_data_path = 'data/raw/'
# data_cleaned = pd.read_csv(interm_data_path + 'DataSampleCleaned.csv', )
# print(data_cleaned.shape)

poi_df = pd.read_csv(raw_data_path + 'POIlist.csv')

poi_df.columns  = list(map(lambda x: str.strip(x), poi_df.columns))
poi_df.drop_duplicates(['Latitude','Longitude'], inplace=True)
poi_df.reset_index(inplace =True,drop=True)

print(poi_df)
