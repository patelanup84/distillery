import streamlit as st

import pandas as pd
import os
import numpy as np
import re


#Title and Subheader
st.title("Data Distillery - Prototype 1.0 - Get Email Activity")
st.write("This application will add email activity (sends, opens, clicks) to the AI Grower Master file")

# ---------------------------------#
# User Functions

# function to select files  
def file_selector(folder_path='inputs/ai master file/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select AI Master Grower Data File to Load', filenames)
    return os.path.join(folder_path, selected_filename)



# ---------------------------------#
# Main panel


filename = file_selector()
st.write('You selected `%s`' % filename)

# reading master file csv display first 5 rows
df_grower = pd.read_csv('inputs/ai master file/2022 AI Grower Master Data File Jan 28 - modifed.csv')
st.write(df_grower.head())