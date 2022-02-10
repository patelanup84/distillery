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



# ---------------------------------#
# Main panel

uploaded_file = st.file_uploader("Load latest AI Master File")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  df = df.astype(str)
  st.write(df)