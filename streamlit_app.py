import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.write('# LCA MSA Dashboard :ear_of_rice: ')  #st.title('Avocado Prices dashboard')
st.markdown('''

This dashboard models the Des Moines, Iowa, US, Statistical Metropolitan Area (DM-MSA) food system under current production and consumpion and in a future scenario where 50% of the nutritional requirements are produced locally within the MSA and where the diet within the MSA follows Dietary Guidelines for Americans 2015 - 2020 (from now on, this will be refered to as the healthy diet). 
The Model Controls tab can be used to generate Life Cycle Assessment (LCA) model outputs which vary by scenario. 
LCA outputs quantify some of the important environmental, economic, and social outcomes of the food system which are generated at a metropolitan scale and will be connected with additional models as part of the Iowa Urban FEWS project. 
All additional tabs in this spreadsheet are dataset the fuel this model.
The underlying LCA model is modified from the US Environmentally-Extended Input-Output Model (USEEIO) as described in Yang et al., 2017 (https://doi.org/10.1016/j.jclepro.2017.04.150).						
									

This is a dashboard showing the base and local scenarios.

Base scenario: Current production and consumption conditions to meet 50% of dietary needs for the DM-MSA	

Local scenario: Future production with 50% of dietary needs for the DM-MSA grown within the DM-MSA under current consumption conditions	

Reference: [Ref](https://www.kaggle.com)
''')
st.header('Summary statistics')

@st.cache_data
def load_data(path):
    dataset = pd.read_csv(path)
    return dataset

avocado = load_data('avocado.csv')
avocado_stats = avocado.groupby('type')['average_price'].mean()
st.dataframe(avocado_stats)

with st.form('line_chart'):
    selected_geography = st.selectbox(label='Geography', options=avocado['geography'].unique())
    submitted = st.form_submit_button('Submit')
    if submitted:
        filtered_avocado = avocado[avocado['geography'] == selected_geography]
        line_fig = px.line(filtered_avocado,
                           x='date', y='average_price',
                           color='type',
                           title=f'Avocado Prices in {selected_geography}')
        st.plotly_chart(line_fig)

chart_data = pd.read_pickle(r'lca_local.pickle')

if st.checkbox('Show dataframe 1'):
    local_data
    
st.header('Model Population, Land Use over Year')
local_data_popLU= chart_data.drop(chart_data.columns[[0,4,5,6]],axis=1)
local_data_popLU=local_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})
if st.checkbox('Show dataframe 2'):
    local_data_popLU
st.line_chart(local_data_popLU,x='Model Year ',y=['Model Population','Land Use (ha)'])

st.header('Model Population, Land Use over Year')
local_data_EWGW= chart_data.drop(chart_data.columns[[0,2,3]],axis=1)
local_data_EWGW=local_data_EWGW.rename(columns={'Total LU (ha)':'Land Use (ha)'})
local_data_EWGW["Freshwater withdrawals (m3)"]=(local_data_EWGW["Freshwater withdrawals (m3)"]/100).round(2)
local_data_EWGW=local_data_EWGW.rename(columns={"Freshwater withdrawals (m3)":"Freshwater withdrawals (L)"})

if st.checkbox('Show dataframe 3'):
    local_data_EWGW
st.line_chart(local_data_EWGW,x='Model Year ',y=['Energy Use (MJ)','Freshwater withdrawals (L)', 'Global Warming Potential (kg co2 eq)'])

line_fig=px.line(local_data_EWGW,x='Model Year ',y=['Energy Use (MJ)','Freshwater withdrawals (L)', 'Global Warming Potential (kg co2 eq)'], markers=True)
#line_fig=px.bar(local_data_EWGW,x='Model Year ',y='Energy Use (MJ)')

st.plotly_chart(line_fig)

with st.sidebar:
    st.subheader('About')
    st.markdown('This dashboard is made by the Iowa Urban FEWS Team, using **Streamlit**')
st.sidebar.image('https://streamlit.io/images/brand/streamlit-mark-color.png', width=50)
