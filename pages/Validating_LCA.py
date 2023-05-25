import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import os




st.write('# LCA MSA Cosim Validation :ear_of_rice: :white_check_mark:')  #st.title('Avocado Prices dashboard')



#col1, col2 = st.columns(2)

#with col1:

#Get CWD 
parent_dir = os.path.dirname(os.getcwd())

pickle_file_path_base = os.path.join(parent_dir, 'data-msa', 'lca_base.pickle')

pickle_file_path_local = os.path.join(parent_dir, 'data-msa', 'lca_local.pickle')


st.header('Current Baseline vs Future Local Scenario:')

chart_data_base = pd.read_pickle(r'lca_base.pickle')
#chart_data_base = pd.read_pickle(pickle_file_path_base)
chart_data = pd.read_pickle(r'lca_local.pickle')
#chart_data = pd.read_pickle(pickle_file_path_local)
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

#line_fig_base1=px.line(base_data_popLU,x='Model_Year_',y=['Model Population','Land Use (ha)'], markers=True)
#st.plotly_chart(line_fig_base1)


# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2040")
# Drop 2040 for base condition for the following reason: 

# baseplot= baseplot.query("`Model_Year_`==2020")
#baseplot 
# Drop columns and rows not needed for plotting 
localplot= chart_data.drop(chart_data.columns[[0,2,3,5]],axis=1)
localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2040")
#localplot 
# Load the Raw data from LCA 

file_path_raw = os.path.join(parent_dir, 'data-msa', 'lca_dataset.csv')

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw = pd.read_csv(file_path_raw)

# postprocess raw results before plotting to compare with cosim 
rbaseplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='BASE'")
rbaseplot=rbaseplot.query("`year`==2020 |`year`==2040")
rlocalplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='LOCAL'")
#rbaseplot
#rlocalplot
#line_fig=px.line(localplot,x='Model_Year_',y=['Energy_Use_MJ','Global_Warming_Potential_kg_co2_eq'], markers=True)
#st.plotly_chart(line_fig)

st.subheader('Energy use in 2020 and 2040 for Food Scenarios')
fig0 = go.Figure(data=[
    
    go.Bar(name='Baseline, co-simulation', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ']),# marker_color=000000),
    go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    go.Bar(name='Local, co-simulation', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ']),#,marker_color='blue'),
    go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Energy Use (MJ)'}
    }
)
# Change the bar mode
fig0.update_layout(barmode='group')
st.plotly_chart(fig0)



st.subheader('Global Warming Potential in 2020 and 2040 for Food Scenarios')
fig1 = go.Figure(data=[
    
    go.Bar(name='Baseline, co-simulation', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq']),# ,marker_color='crimson'),
    go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
    go.Bar(name='Local, co-simulation', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq']),#,marker_color='blue'),
    go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['gwp']),#,marker_color='DarkSlateGrey')  
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Global Warming Potential (kg co2 eq)'}
    }
)
# Change the bar mode
fig1.update_layout(barmode='group')
st.plotly_chart(fig1)




if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   

if st.checkbox('Show raw dataset from LCA in isolation'):
    chart_data_raw  
