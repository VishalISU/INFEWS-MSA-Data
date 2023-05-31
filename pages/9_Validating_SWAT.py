import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import os

st.write('# :droplet: :white_check_mark: LCA MSA Cosim Validation ')  

st.header('Current Baseline vs Future Local Scenario:')

chart_data_hist = pd.read_pickle(r'TxtInOutHist_output.pickle')

chart_data_fut = pd.read_pickle(r'TxtInOutFut_output.pickle')
 
st.subheader('Current Baseline')

# Read the current and future raw data from original SWAT Runs
current=pd.read_csv(r'current.csv')
future=pd.read_csv(r'future.csv')

# Allocate the first column as the index
current.set_index('YEAR', inplace=True)
future.set_index('YEAR', inplace=True)

current=current.transpose() 
future=future.transpose()

# Create the DataFrame
df = pd.DataFrame(chart_data_hist)
# Transpose for better plotting

df=df.transpose()

Choice1=st.selectbox('Pick a crop', ['APPL', 'CABG', 'CORN','SOYB'])

# Create the bar graph
fig = go.Figure()

fig.add_trace(go.Bar(x=df.index, y=current[Choice1],name='Isolated'))
fig.add_trace(go.Bar(x=df.index, y=df[Choice1], name='Co-Simulated' ))

# Iterate over the columns starting from the second column
#for i in range(1, len(df.columns)):
#    fig.add_trace(go.Bar(x=df.index, y=df.iloc[:, i], name=df.columns[i]))

# Set the layout
fig.update_layout(
    title='Current Baseline: '+Choice1,
    xaxis_title='Year',
    yaxis_title='Yields (kg/ha)',
    xaxis=dict(
        tickmode='linear',
        dtick = 1
    )
)    

st.plotly_chart(fig)


st.subheader('Future Scenario')

# Create the DataFrame
df = pd.DataFrame(chart_data_fut)
# Transpose for better plotting

df=df.transpose()

Choice2=st.selectbox('Pick a crop ', ['APPL', 'CABG', 'CORN','SOYB'])

# Create the bar graph
fig2 = go.Figure()

fig2.add_trace(go.Bar(x=df.index, y=future[Choice2],name='Isolated'))
fig2.add_trace(go.Bar(x=df.index, y=df[Choice2], name='Co-Simulated' ))

# Iterate over the columns starting from the second column
#for i in range(1, len(df.columns)):
#    fig.add_trace(go.Bar(x=df.index, y=df.iloc[:, i], name=df.columns[i]))

# Set the layout
fig2.update_layout(
    title='Future Scenario: '+Choice2,
    xaxis_title='Year',
    yaxis_title='Yields (kg/ha)',
    xaxis=dict(
        tickmode='linear',
        dtick = 1
    )
)    

st.plotly_chart(fig2)



if st.checkbox('Show Cosim current baseline dataset'):
    chart_data_hist

if st.checkbox('Show Cosim future scenario dataset'):
    chart_data_fut 

if st.checkbox('Show Isolation current baseline dataset'):
    current.transpose()

if st.checkbox('Show Isolatoin future scenario dataset'):
    future.transpose() 

# %%
