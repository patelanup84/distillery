import streamlit as st

import pandas as pd
import os
import numpy as np
import re

#for connecting to gbq
import pandas_gbq as gbq
from google.cloud import bigquery
from google.oauth2 import service_account

#Title and Subheader
st.title("Data Distillery")
st.subheader("Prototype 1.0 - Get Email Activity")

st.write("This application will enrich the existing AI Grower Data with email behaviour data.")

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

uploaded_file = st.file_uploader('Load the latest grower master file .csv')
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

#Step 2. Load Latest Email data from GBQ
st.header('Step 2. Load Email Data')
st.write('By pressing the button below, the latest available email data from Sales Force Marketing Cloud and Acton will be imported into this application for blending and analysis.')

submit = st.button('Load Email Data')
if submit:

    # connect to GBQ
    key_path = "/content/drive/Shareddrives/TADA/Data/ws-performance-dd7b40645fd6.json"
    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)


    # Build query
    query = """
        SELECT *
        FROM `ws-performance.sfmc.emails_totals` 
    """

    # Create dataframe
    df_sfmc = client.query(query).to_dataframe() 

    #load table
    filepath = 'inputs/email/2022 AI Grower Master Data File Jan 28 - modifed.csv'
    df_grower = pd.read_csv(filepath)
    df_grower = df_grower.astype(str)
    df_grower = format_dataframe(df_grower)
    st.write(df_grower)

    #blend with Acton data








#Step 3. Load Latest Email data from GBQ
# st.header('Step 3. Blend Grower Data with Email Data')
# submit = st.button('Blend Data')
# if submit:
#     filepath = 'inputs/ai master file/2022 AI Grower Master Data File Jan 28 - modifed.csv'
#     df_grower = pd.read_csv(filepath)





### TESTING ###

