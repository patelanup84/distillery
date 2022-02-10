import streamlit as st

import pandas as pd
import os
import numpy as np
import re


#Title and Subheader
st.title("Data Distillery")
st.write("Prototype 1.0 - Get Email Activity")

st.write("This application will add email activity (sends, opens, clicks) to the AI Grower Master file")

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

  return df


# ---------------------------------#
# Main panel

uploaded_file = st.file_uploader("Load latest AI Master File")
if uploaded_file is not None:
  df_grower = pd.read_csv(uploaded_file)
  df_grower = df_grower.astype(str)
  df_grower = format_dataframe(df_grower)
  st.write(df_grower)

