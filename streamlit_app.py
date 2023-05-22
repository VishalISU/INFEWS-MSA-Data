import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


st.write('# LCA MSA Dashboard :ear_of_rice: ')  #st.title('Avocado Prices dashboard')

#col1, col2 = st.columns(2)

#with col1:

st.header('Current Baseline vs Future Local Scenario:')

chart_data_base = pd.read_pickle(r'lca_base.pickle')

chart_data = pd.read_pickle(r'lca_local.pickle')
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

#line_fig_base1=px.line(base_data_popLU,x='Model Year ',y=['Model Population','Land Use (ha)'], markers=True)
#st.plotly_chart(line_fig_base1)


# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model Year `==2020 | `Model Year `==2040")
# Drop 2040 for base condition for the following reason: 

# baseplot= baseplot.query("`Model Year `==2020")
#baseplot 
# Drop columns and rows not needed for plotting 
localplot= chart_data.drop(chart_data.columns[[0,2,3,5]],axis=1)
localplot= localplot.query("`Model Year `==2020 | `Model Year `==2040")
#localplot 
# Load the Raw data from LCA 

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw

# postprocess raw results before plotting to compare with cosim 
rbaseplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='BASE'")
rbaseplot=rbaseplot.query("`year`==2020 |`year`==2040")
rlocalplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='LOCAL'")
#rbaseplot
#rlocalplot
#line_fig=px.line(localplot,x='Model Year ',y=['Energy Use (MJ)','Global Warming Potential (kg co2 eq)'], markers=True)
#st.plotly_chart(line_fig)
st.subheader('Energy use in 2020 and 2040 for Food Scenarios')
fig0 = go.Figure(data=[
    
    go.Bar(name='Baseline, co-simulation', x=baseplot['Model Year '], y=baseplot['Energy Use (MJ)']),# marker_color=000000),
    go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    go.Bar(name='Local, co-simulation', x=localplot['Model Year '], y=localplot['Energy Use (MJ)']),#,marker_color='blue'),
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
    
    go.Bar(name='Baseline, co-simulation', x=baseplot['Model Year '], y=baseplot['Global Warming Potential (kg co2 eq)']),# ,marker_color='crimson'),
    go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
    go.Bar(name='Local, co-simulation', x=localplot['Model Year '], y=localplot['Global Warming Potential (kg co2 eq)']),#,marker_color='blue'),
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



year_LU = st.selectbox(
    'What column to you want to display',
     chart_data_base.columns[[1]])



st.line_chart(df[column])
if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   


if st.checkbox('Show avocado demo'):
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