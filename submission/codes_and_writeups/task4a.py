# The goal is to achieve maximum visualization difference for POI's
# with popularity close to averge, and to minimize the effect of outliers.

# Here I assume that the visualization is done with color scale.

# Here is the approach I would propose:

#1. Identify a upper bound and lower bound of popularity score that would
# be considered normal.
#2. Divide the dataset into three datasets: low_outlier, normal and high_outlier.
#3. Standardize the popularity score to range (-10,10) as specified in the question.
#4. Assign a score of 10 to the high_outliers, and 0 to the low_outliers.
#5. Plot high_outliers and low_outliers with the same color at 10 and -10, respectively.
#6. if it is important to identify the outliers, we can use other visualization
# features, e.g. size and shape etc.

# As an example, let's assume there are 100 POIs. The range of popularity score is
#(0 to 100), with mean = 50, and standard deviation = 18.

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
poi = ['POI' + str(i) for i in range(0,100)]
popularity = np.random.normal(50,15,100)

np.random.seed(1)
data_df = pd.DataFrame(popularity, index=poi, columns = ['popularity'])

# What should be considered outliers is a business question. Here, we assume
# anything lower than 30 and higher than 70 are outliers.

lower = 30
upper = 70

#create high and low outliers dataframe

data_hi_outliers = data_df[data_df.popularity > upper].copy()
data_hi_outliers['scaled_score'] = 10
data_hi_outliers['group'] = 'hi'

data_low_outliers = data_df[data_df.popularity < lower].copy()
data_low_outliers['scaled_score'] = -10
data_low_outliers['group'] = 'low'

# scale to range (-10,10)

data_df = data_df[data_df.popularity.between(lower,upper)]


scaled_max = 10
scaled_min = -10

scaler = MinMaxScaler((scaled_min,scaled_max))
data_df['scaled_score'] = scaler.fit_transform(data_df[['popularity']])
data_df['group'] = 'normal'

data_df = pd.concat([data_df, data_low_outliers,data_hi_outliers])

print(data_hi_outliers.head())

# With this modified data frame, the difference in visualization can be maximized
# around the average values.

# The outliers can be identified with the group columns and with different features
# e.g. marker style, marker size. 
