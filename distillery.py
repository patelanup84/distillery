# import libraries
import streamlit as st

import pandas as pd
import re
import numpy as np
import os

# for location data
import requests
import time

# for weather data
from datetime import datetime
from meteostat import Point, Monthly

# for progress bar
from time import sleep
from tqdm import tqdm


#Title and Subheader
st.title("Data Distillery")
st.subheader("Prototype 1.0 - Match 2021 Email & Weather Data.")

st.write("This application will enrich the existing AI Grower Data with email behaviour data for use in customer journey/persona building, marketing campaigns, ML modelling etc.")

# ---------------------------------#
# User Functions
# function to format/standardize dataframes for processing:
def format_dataframe(df):
  
  # Format col. headers (snake case)
  # df = df.rename(columns={element: re.sub(r'([A-Z]+)', r'_\1', element) for element in df.columns.tolist()})# add space before cap. letter
  df = df.rename(columns={element: re.sub(r'(?<![A-Z])(?<!^)([A-Z])',r' \1', element) for element in df.columns.tolist()})
  df.columns = df.columns.str.lstrip('_') #strip leading underscore
  df.columns = df.columns.str.lower() # convert to lowercase
  df.columns = map(lambda x : x.replace("-", "_").replace(" ", "_"), df.columns) # replace hyphens/spaces with underscore
  df.columns = map(lambda x : x.replace("__", "_"), df.columns) # replace double underscore with single underscore
  df.columns = df.columns.str.strip() # strip leading and trailing whitespaces
  specchar = '[≅,#,@,&,(,),?,\']' # List of spec. chars
  df.columns = df.columns.str.replace(specchar, '') # Remove spec. char.
  # Format row data
  df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # strip leading and trailing whitespaces
  df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x) # convert string values to uppercase
  df.fillna(0) #
  return df


# Dictionary to define program years
dict_proyr = {'2016':['2015-09-01','2016-08-31'],
              '2017':['2016-09-01','2017-08-31'],
              '2018':['2017-09-01','2018-08-31'],
              '2019':['2018-09-01','2019-08-31'],
              '2020':['2019-09-01','2020-08-31'],
              '2021':['2020-09-01','2021-08-31'],
              '2022':['2021-09-01','2022-08-31']}


## Function to get avg. temp. and precip. for specific location
def get_meteostat_results(coordinates):

  # Split grower_coord string to get lat,lon
  grower_lat = float(coordinates.split(',')[0])
  grower_lon = float(coordinates.split(',')[1])
  
  # Get location by aggregate of nearby weather stations
  location = Point(lat=grower_lat, lon=grower_lon, alt=600) 

  # Define date range
  date_start = datetime(2021, 5, 1)
  date_end = datetime(2021, 8, 31)

  # Get weather data
  grower_weather_monthly = Monthly(location, start=date_start, end=date_end)
  grower_weather_monthly = grower_weather_monthly.fetch()

  avg_prec = round(grower_weather_monthly['prcp'].mean(),1)
  avg_temp = round(grower_weather_monthly['tavg'].mean(),1)

  return avg_prec,avg_temp


### MAIN PANEL ###

#Step 1. Load Grower Master file
st.header('Step 1. Load Grower Master File')
st.write('Note: For the purposes of this prototype, a random selection of 100 growers will be selected from the Master File.')

uploaded_file = st.file_uploader('Load the latest grower master file.csv')
if uploaded_file is not None:
    
    # load selected file
    df_grower = pd.read_csv(uploaded_file)

    # select small sample size
    df_geo = df_geo.sample(n=100)

    # Format/standardize dataframe
    df_grower = format_dataframe(df_grower)

    ## FORMAT/CLEAN DATA
    # replace 0 with blanks for select cols.
    list_cols = ['grower_site_id','grower_site_name','grower_first_name','grower_last_name','grower_email','grower_phone','grower_cellular','grower_contact_phone','grower_contact_cell']
    df_grower[list_cols] = df_grower[list_cols].replace({'0':np.nan, 0:np.nan,'':np.nan})

    # remove all numeric values from select cols.
    list_cols = ['2021_sales','grower_phone','grower_cellular','grower_contact_phone','grower_contact_cell']
    df_grower[list_cols] = df_grower[list_cols].replace('[^\d.]', '', regex = True).replace('',np.nan)

    # convert select cols to numeric(float)
    list_cols = ['2021_sales']
    df_grower[list_cols] = df_grower[list_cols].astype(float)

    # display No. of growers
    num_growers = df_grower['grower_site_id'].nunique()
    st.write("Total No. of Growers in Database=",num_growers)
    
    # display % with emails
    num_emails = df_grower['grower_email'].nunique()
    per_emails = round(((num_emails/num_growers)*100),0)
    st.write("Percent of growers with emails=",per_emails)

    # display dataframe
    st.write(df_grower)



#Step 2. Import Email Data
st.header('Step 2. Import Email Data')
st.write('Press the button below to upload the historical email activity from SFMC & Act-on')

submit = st.button('Import Email Data')
if submit:
  # Load formatted & unstacked email data
  filepath = 'inputs/email/emails_formatted.csv'
  df_emails = pd.read_csv(filepath)

  # Classify each row by Program Year
  for k, (startdate,enddate) in dict_proyr.items():
      df_emails.loc[df_emails['action_date'].between(startdate,enddate), 'program_year'] = k
  # Drop cols
  df_emails = df_emails.drop(['action_date'],axis=1,inplace=False)
  # Pivot by Grower
  df_grower_email = pd.pivot_table(df_emails, index=['grower_email','program_year'], columns = 'action',aggfunc=len).reset_index()
  # Format cols.
  df_grower_email.columns = df_grower_email.columns.str.lower() # convert to lowercase
  # Reorder columns
  list_col = ['grower_email','program_year','sent','opened','clicked']
  df_grower_email = df_grower_email.reindex(columns=list_col)
  # Rename columns
  df_grower_email = df_grower_email.rename({'sent':'emails_sent','opened':'emails_opened','clicked':'emails_clicked',},axis=1)
  # Reset index
  df_grower_email = df_grower_email.reset_index(drop=True)
  
  # Group by Prog. years
  df_grower_email_by_year = df_grower_email.groupby(['program_year'])['emails_sent','emails_opened','emails_clicked'].sum().reset_index()
  # add open rates and ctr                               
  df_grower_email_by_year['open_rate'] = round((df_grower_email_by_year['emails_opened']/df_grower_email_by_year['emails_sent'])*100,2)
  df_grower_email_by_year['ctr'] = round((df_grower_email_by_year['emails_clicked']/df_grower_email_by_year['emails_sent'])*100,2)
  
  # Display dataframe
  st.write(df_grower_email_by_year)


#Step 3. Import Weather Data
st.header('Step 3. Import Weather Data')
st.write('Press the button below to upload the 2021 weather data for grower regions from Environment Canada (via Meteostat')

submit = st.button('Import Weather Data')
if submit:
  # Load formatted & unstacked email data
  filepath = 'inputs/geo/grower_geo_data.csv'
  df_geo = pd.read_csv(filepath)

  # Create list of coordinates
  list_coord = df_geo['site_coord'].tolist()
  num_coord = len(list_coord)
  st.write("No. of locations to gather weather data for=",num_coord)

  # Create a placeholder list to hold results
  results = []

  # loop through list and get weather data
  # my_bar = st.progress(0)
  # for percent_complete in range(num_coord):
  #   time.sleep(0.1)
  #   my_bar.progress(percent_complete + 1)
  for coord in list_coord:
    weather_result = get_meteostat_results(coord)
    results.append(weather_result)
  
  # Write results to dataframe
  df_weather = pd.DataFrame(results,columns = ['2021_site_avg_prec', '2021_site_avg_temp'])

  # Display dataframe
  st.write(df_weather)


#Step 4. Blend Data
st.header('Step 4. Match Data')
st.write('Pres the button below to match the imported email and weather data to the uploaded grower master file')

# st.subheader('Grower Data Analysis')
# st.write('Below will be charts (i.e. map)/statistical data for weather. over the p. year. **What qustions do we want to answer?**')

#Step 5. Export Data
st.header('Step 5. Export Data')
st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')

submit = st.button('Export Enhanced Grower Dataset')
# if submit:
  # Load formatted & unstacked email data
  # filepath = 'outputs/geo/grower_geo_data.csv'
  