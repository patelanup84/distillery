import streamlit as st
import pandas as pd
import requests


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
This program will join the latest email data to the AI Grower Master File and provide some overall insights.
""")

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