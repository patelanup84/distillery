import streamlit as st
import os

def file_selector(folder_path='inputs/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select AI Master Grower Data File to Load', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)