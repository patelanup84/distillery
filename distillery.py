import streamlit as st

import pandas as pd
import os
import numpy as np
import re


#Title and Subheader
st.title("Data Distillery")
st.subheader("Prototype 1.0 - Email & Weather Data for 2022.")

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


### MAIN PANEL ###

#Step 1. Load Grower Master file
st.header('Step 1. Load Grower Master File')

uploaded_file = st.file_uploader('Load the latest grower master file.csv')
if uploaded_file is not None:
    
    # load selected file
    df_grower = pd.read_csv(uploaded_file)

    # format/clean data
    df_grower = df_grower.astype(str)
    df_grower = format_dataframe(df_grower)
    list_cols = ['grower_site_id','grower_site_name','grower_first_name','grower_email','grower_cellular']
    df_grower[list_cols] = df_grower[list_cols].replace({'0':np.nan, 0:np.nan}) #repl. 0 with blanks

    # display No. of growers
    num_growers = df_grower['grower_site_id'].nunique()
    st.write("Total No. of Growers in Database=",num_growers)
    
    # display % with emails
    num_emails = df_grower['grower_email'].nunique()
    per_emails = round(((num_emails/num_growers)*100),0)
    st.write("Percent of growers with emails=",per_emails)

    # display dataframe
    st.write(df_grower)

#Step 2. Load Email Data
st.header('Step 2. Load Email Data')
st.write('Pres the button below to upload the 2021 email activity directly from SFMC')

submit = st.button('Load Email Data')
if submit:

    # Load formatted & unstacked email data
    filepath = 'inputs/email/emails_formatted.csv'
    df_emails = pd.read_csv(filepath)

    #  Display dataframe
    st.write(df_emails)

    #blend with Acton data

st.subheader('Email Analysis')
st.write('Below will be charts/statistical data for email perf. over the p. year')


#Step 3. Load Weather Data
st.header('Step 3. Load Weather Data')
st.write('Pres the button below to upload the 2021 weather data for grower regions from Environment Canada (via Meteostat')

st.subheader('Weather Analysis')
st.write('Below will be charts (i.e. map)/statistical data for weather. over the p. year')

#Step 4. Blend Data
st.header('Step 4. Blend Data')
st.write('Pres the button below to blend the latest email and weather data to the uploaded grower master file')

st.subheader('Grower Data Analysis')
st.write('Below will be charts (i.e. map)/statistical data for weather. over the p. year. **What qustions do we want to answer?**')

#Step 5. Export Data
st.header('Step 5. Export Data')
st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')