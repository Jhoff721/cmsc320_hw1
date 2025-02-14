# Make sure these code blocks run properly and that you have properly installed the appropriate modules required.
import pandas as pd
import requests

# Don't remove this
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# API URL and headers in case request gets denied.
api_url = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanoes"

headers = {
    'accept': '*/*'
}

response = requests.get(api_url, headers=headers)

# Get content information as JSON
data = response.json()["items"]

# Convert data to DataFrame
df = pd.DataFrame(data)
    
# Save to file
df.to_csv("volcanoes.csv", index=False)

# Describing information
#print("Number of datapoints and features: ", df.shape)
#print("Names of all features: ", list(df))

# Create new dataframe that discards all except:
#id,	year, month, day,	tsunamiEventId, earthquakeEventId, 
# volcanoLocationId, volcanoLocationNewNum, name, country, elevation,
#  morphology, deathsTotal, vei, deaths
new_df = df[['id', 'year', 'month', 'day', 'tsunamiEventId', 'earthquakeEventId', 
             'volcanoLocationId', 'volcanoLocationNewNum', 'name', 'country', 'elevation', 
             'morphology', 'deathsTotal', 'vei', 'deaths']]

# remove rows where year, month or day are NaN
new_df = new_df.dropna(subset=['year', 'month', 'day'])

#print(new_df)

# change index column so it has 1-based indexing
new_df.index = new_df.index + 1

#print(new_df)

# make new column 'totalDeaths' that takes max of deathsTotal and deaths
new_df['totalDeaths'] = new_df[['deaths', 'deathsTotal']].max(axis=1)

#print(new_df[['deaths', 'deathsTotal', 'totalDeaths']])

# turn year, month, day into one column 'date'

#print(new_df[['year', 'month', 'day']])

# Convert month and day to ints (instead of floats)
new_df['month'] = new_df['month'].astype(int)
new_df['day'] = new_df['day'].astype(int)

# Convert the columns to datetime
new_df['date'] = pd.to_datetime(new_df[['year','month','day']], format='%Y-%m-%d', errors='coerce')

# Drop year, month, day
new_df = new_df.drop(columns=new_df[['year', 'month', 'day']])

# Move date to second position
date = new_df.pop('date')
new_df.insert(1, 'date', date)

# ==========================================================================
# Part 2

# Group data by country showing date, country, name, vei
# Sort vei from highest to lowest
from IPython.display import display
countryGroup = new_df.sort_values(['vei'], ascending=False).groupby('country')[['date', 'country', 'name', 'vei']]

#for group in countryGroup:
#    display(group)

# print out max vei for each unique country
maxVei = new_df.groupby('country')['vei'].max()

# For loop has the index (which is country due to the groupby) and value
#for country, max in maxVei.items():
#    print(f"Country: {country}, Highest VEI: {max}")

# 
