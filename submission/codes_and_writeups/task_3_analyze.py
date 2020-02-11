import pandas as pd
import numpy as np
import folium

interim_data_path = 'data/interim/'

data_df = pd.read_csv(interim_data_path + 'DataSampleLabeled.csv')
poi_df = pd.read_csv(interim_data_path + 'POIlistCleaned.csv')
poi_df.set_index('POIID', inplace=True)

#remove errenous entries (lon/lat do not match Canada locations)
data_df = data_df[data_df['ClosestDistance'] < 3000]

#Calcuate the average and standard deviation of distrance for each POI
poi_stats = data_df.groupby('ClosestPOI').agg({'ClosestDistance':['mean', 'std']})

print(poi_stats)
print('\n')

#create dataframe for plotting
#the max ClosesetDistance is used as the radium to ensure all locations are
#covered

poi_plot = data_df.groupby('ClosestPOI').agg({'ClosestDistance':['max','count']})
poi_plot.columns = poi_plot.columns.get_level_values(1)

#merge with POIlistCleaned
poi_plot = poi_plot.merge(poi_df, left_index = True, right_on = 'POIID')
print('\n')

# Plot with Folium
m = folium.Map(location=[55, -100], width=1000, height=500,zoom_start=3)

for i, data in poi_plot.iterrows():
    folium.Circle(location=[data['Latitude'],data['Longitude']],
    radius=data['max']*1000, popup = str(i), color='#3186cc', fill=True,
    fill_color='#3186cc').add_to(m)

viz_out_path = 'submission/visualization/'
m.save(viz_out_path + 'POICoverPlot.html')

# Calculate densign
poi_density = poi_plot[['max','count']].copy()

poi_density.columns = ['radius','count']

poi_density['density'] = np.divide(poi_density['count'],
np.power(poi_density['radius'],2)*np.pi)

print(poi_density)
