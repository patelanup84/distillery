import streamlit as st

import pandas as pd
import os
import numpy as np
import re

#for connecting to gbq
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

# function to run query in GBQ
# Use st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


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

    # Create GBQ API client (pull from .toml)
    credentials = service_account.Credentials.from_service_account_info(st.secrets["ws_gcp_service_account"])
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Query GBQ and create dataframe
    rows = run_query("SELECT * FROM `ws-performance.sfmc.emails_totals`")


    df_sfmc = client.query(query).to_dataframe()

    #  Display dataframe
    st.write(df_grower)

    #blend with Acton data








#Step 3. Load Latest Email data from GBQ
# st.header('Step 3. Blend Grower Data with Email Data')
# submit = st.button('Blend Data')
# if submit:
#     filepath = 'inputs/ai master file/2022 AI Grower Master Data File Jan 28 - modifed.csv'
#     df_grower = pd.read_csv(filepath)





### TESTING ###

