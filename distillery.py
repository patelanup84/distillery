import streamlit as st

import pandas as pd
import os
import numpy as np
import re



def file_selector(folder_path='inputs/ai master file/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select AI Master Grower Data File to Load', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)



df_grower = pd.DataFrame(load_iris()['data'], columns=load_iris()['feature_names'])


# ---------------------------------#
# Main panel

st.title('Data Distillery')
st.write("Prototype 1.0 - Get Email Activity")
st.write("This application will add email activity (sends, opens, clicks) to the AI Grower Master file")