import numpy as np
import pandas as pd

# Read Sample Data
raw_data_path = 'data/raw/'
data_df = pd.read_csv(raw_data_path + 'DataSample.csv')

#CLean Data
data_df.columns = list(map(lambda x: str.strip(x), data_df.columns))

#remove all records with duplicates (all records discarded)
data_df.drop_duplicates(['TimeSt', 'Country', 'Province', 'City', 'Latitude',
'Longitude'], keep=False, inplace=True)

#Write cleaned DataSample file to csv and save in data/interim
interim_data_path = 'data/interim/'
data_df.to_csv(interim_data_path + 'DataSampleCleaned.csv',index=False)
