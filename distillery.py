import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import load_diabetes, load_boston

import requests
import io

# ---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='Data Distillery',
                   layout='wide')
# ---------------------------------#
# Data loading
# def load_sample():
#     data = pd.read_csv('/inputs/sample.csv')
#     return data

# Data loading from Github account
url = "https://raw.githubusercontent.com/patelanup84/distillery/main/inputs/sample.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url).content
# Reading the downloaded content and turning it into a pandas dataframe
def load_sample():
    data = pd.read_csv(io.StringIO(download.decode('utf-8')))
    return data


# ---------------------------------#
# Model building
def build_model(df):
    X = df.iloc[:, :-1]  # Using all column except for the last column as X
    Y = df.iloc[:, -1]  # Selecting the last column as Y

    # # Data splitting
    # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(100 - split_size) / 100)
    #
    # st.markdown('**1.2. Data splits**')
    # st.write('Training set')
    # st.info(X_train.shape)
    # st.write('Test set')
    # st.info(X_test.shape)
    #
    # st.markdown('**1.3. Variable details**:')
    # st.write('X variable')
    # st.info(list(X.columns))
    # st.write('Y variable')
    # st.info(Y.name)
    #
    # rf = RandomForestRegressor(n_estimators=parameter_n_estimators,
    #                            random_state=parameter_random_state,
    #                            max_features=parameter_max_features,
    #                            criterion=parameter_criterion,
    #                            min_samples_split=parameter_min_samples_split,
    #                            min_samples_leaf=parameter_min_samples_leaf,
    #                            bootstrap=parameter_bootstrap,
    #                            oob_score=parameter_oob_score,
    #                            n_jobs=parameter_n_jobs)
    # rf.fit(X_train, Y_train)
    #
    st.subheader('2. Lorem Ipsum')
    #
    st.markdown('**2.1. Lorem Ipsum**')
    # Y_pred_train = rf.predict(X_train)
    # st.write('Coefficient of determination ($R^2$):')
    # st.info(r2_score(Y_train, Y_pred_train))
    #
    # st.write('Error (MSE or MAE):')
    # st.info(mean_squared_error(Y_train, Y_pred_train))
    #
    # st.markdown('**2.2. Test set**')
    # Y_pred_test = rf.predict(X_test)
    # st.write('Coefficient of determination ($R^2$):')
    # st.info(r2_score(Y_test, Y_pred_test))
    #
    # st.write('Error (MSE or MAE):')
    # st.info(mean_squared_error(Y_test, Y_pred_test))
    #
    # st.subheader('3. Model Parameters')
    # st.write(rf.get_params())


# ---------------------------------#
st.write("""
# The Data Distillery - prototype v1.0
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
""")

# ---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload Weekly Sales Report'):
    uploaded_file = st.sidebar.file_uploader("Upload the most recent 'Sales Report - XX.XX.2022.xlsx' from AgData FTP", type=["csv"])
    st.sidebar.markdown("""
[sample CSV input file](https://drive.google.com/file/d/13Tndqil7L_ubrjI4CsC14-z6qsHfcO5I/view?usp=sharing)
""")

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Clean Data'):
    split_size = st.sidebar.slider('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 10, 90, 80, 5)

with st.sidebar.subheader('2.1. Matching Records'):
    #parameter_n_estimators = st.sidebar.slider('Number of estimators (n_estimators)', 0, 1000, 100, 100)
    parameter_max_features = st.sidebar.select_slider('Lorem ipsum', options=['low', 'medium', 'high'])
    #parameter_min_samples_split = st.sidebar.slider(
        # 'Minimum number of samples required to split an internal node (min_samples_split)', 1, 10, 2, 1)
    #parameter_min_samples_leaf = st.sidebar.slider(
        # 'Minimum number of samples required to be at a leaf node (min_samples_leaf)', 1, 10, 2, 1)

# with st.sidebar.subheader('2.2. General Parameters'):
#     parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
#     parameter_criterion = st.sidebar.select_slider('Performance measure (criterion)', options=['mse', 'mae'])
#     parameter_bootstrap = st.sidebar.select_slider('Bootstrap samples when building trees (bootstrap)',
#                                                    options=[True, False])
    parameter_oob_score = st.sidebar.select_slider(
        'Lorem ipsum dolor sit amet.', options=[False, True])
    # parameter_n_jobs = st.sidebar.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])

# ---------------------------------#
# Main panel

# Displays the dataset
st.subheader('1. Input Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df)
    build_model(df)
else:
    st.info('Awaiting for Weekly Sales Report file to be uploaded.')
    if st.button('Press to use Sample Dataset'):

        # 2021 Invoices dataset
        # sample = load_sample()
        # X = pd.DataFrame(sample.data, columns=sample.feature_names)
        # Y = pd.Series(sample.target, name='response')
        df_sample = load_sample()
        st.markdown('A sample data set from the Jan 7 Weekly Sales Report has been loaded below. Below are the first 5 rows.')
        st.write(df_sample.head(5))

        build_model(df_sample)