import streamlit as st
import pandas as pd
import numpy as np
import plost
from PIL import Image
import plotly.express as px

# Get Data
agentname = pd.read_csv('agentname.csv')
alr = pd.read_csv('alr.csv')
pollingunit = pd.read_csv('pollingunit.csv')
states = pd.read_csv('states.csv')
ward = pd.read_csv('ward.csv')
party = pd.read_csv('party.csv')
lga = pd.read_csv('lga.csv')
awr = pd.read_csv('awr.csv')
asr = pd.read_csv('asr.csv')
apr = pd.read_csv('apr.csv')
poll = pd.read_csv('poll.csv')
lgaresult = pd.read_csv('lgaresults.csv')

st.set_page_config(layout = 'wide')


st.header('BINCOM ASSESSMENT')

# Row C
c1, c2 = st.columns((7,7))
# Question 1
with c1:
    st.markdown(' Question 1: Individual Polling units and their respective results')
    plost.donut_chart(
        data=poll,
        theta='polling_unit_name',
        color='party_score')

# Question 2
with c2:
    st.markdown(' Question 2: Total votes by LGA')
    lrg = lgaresult.groupby(by = 'lga_name')['party_score'].sum()
    lga_list = st.selectbox("Select Local Goverment Area", lgaresult["lga_name"].unique())
    st.write('You have selected', lga_list)
    st.markdown(f'Total votes for {lga_list}:') 
    st.markdown(lrg[lga_list])

# Question 3
st.markdown('### Question 3: New polling unit')

if 'data' not in st.session_state:
    data = pd.read_csv('apr.csv')
    st.session_state.data = data

data = st.session_state.data

st.dataframe(data)

def add_form():
    row = pd.DataFrame({'result_id':[st.session_state.input_col1],
            'party_abbreviation': [st.session_state.input_col2],
            'party_score':[st.session_state.input_col3],

            })
    st.session_state.data = pd.concat([st.session_state.data, row])

newform = st.form(key = 'newform')

with newform:
    columns = st.columns(2)
    with columns[0]:
        st.number_input('result_id', key = 'input_col1')
    with columns[1]:
        st.selectbox('Select party to add to dataframe: ', apr['party_abbreviation'].unique(), key='input_col2')
        st.number_input('Party Votes', key = 'input_col3')
    st.form_submit_button(on_click=add_form) 
