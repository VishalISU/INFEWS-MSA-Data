import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


#Force Streamlit to work in wide mode 

st.set_page_config(
    page_title="SWAT",
    page_icon="💧",
)


st.write('# :seedling: SWAT MSA Dashboard :droplet: ')  #st.title('Avocado Prices dashboard')

#col1, col2 = st.columns(2)

#with col1:

st.header('Current Baseline vs Future Local Scenario:')

chart_data_hist = pd.read_pickle(r'TxtInOutHist_output.pickle')

chart_data_fut = pd.read_pickle(r'TxtInOutFut_output.pickle')
 
st.subheader('Current Baseline')

# Create the DataFrame
df = pd.DataFrame(chart_data_hist)
# Transpose for better plotting
df=df.transpose()

Choice1 = st.selectbox(
    'Select Crop 1:',
     df.columns)
Choice2 = st.selectbox(
    'Select Crop 2:',
     df.columns)
# Create the bar graph
fig = go.Figure()

fig.add_trace(go.Bar(x=df.index, y=df[Choice1], name=Choice1 ))
fig.add_trace(go.Bar(x=df.index, y=df[Choice2],name=Choice2))

# Iterate over the columns starting from the second column
#for i in range(1, len(df.columns)):
#    fig.add_trace(go.Bar(x=df.index, y=df.iloc[:, i], name=df.columns[i]))

# Set the layout
fig.update_layout(
    title='Crops Yields by year',
    xaxis_title='Year',
    yaxis_title='Yields (kg/ha)',
    xaxis=dict(
        tickmode='linear',
        dtick = 1
    )
)    

st.plotly_chart(fig)


if st.checkbox('Show historical dataset'):
    chart_data_hist

if st.checkbox('Show future dataset'):
    chart_data_fut 

