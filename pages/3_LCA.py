import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go



#st.set_page_config(layout="wide")

st.set_page_config(
    page_title="LCA",
    page_icon="🌾",
)

st.write('#  :ear_of_rice: LCA MSA Dashboard')  #st.title('Avocado Prices dashboard')

#col1, col2 = st.columns(2)

#with col1:

st.header('Current Baseline vs Future Local Scenario:')

chart_data_base = pd.read_pickle(r'lca_base.pickle')

chart_data = pd.read_pickle(r'lca_local.pickle')
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

#line_fig_base1=px.line(base_data_popLU,x='Model_Year_',y=['Model Population','Land Use (ha)'], markers=True)
#st.plotly_chart(line_fig_base1)


# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

#baseplot= baseplot.query("`Model_Year_`==2020")
#baseplot 
# Drop columns and rows not needed for plotting 
localplot= chart_data.drop(chart_data.columns[[0,2,3,5]],axis=1)
localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
#localplot 
# Load the Raw data from LCA 

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw

# postprocess raw results before plotting to compare with cosim 
rbaseplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='BASE'")
rbaseplot=rbaseplot.query("`year`==2020 |`year`==2050")
rlocalplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='LOCAL'")
#rbaseplot
#rlocalplot
#line_fig=px.line(localplot,x='Model_Year_',y=['Energy_Use_MJ','Global_Warming_Potential_kg_co2_eq'], markers=True)
#st.plotly_chart(line_fig)

st.subheader('Energy use in 2020 and 2050 for Food Scenarios')
fig_lca_eu = go.Figure(data=[
    
    go.Bar(name='Baseline: Current Condition', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ']),# marker_color=000000),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    go.Bar(name='Future Scenario', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ']),#,marker_color='blue'),
    #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Energy Use (MJ)'}
    }
)
# Change the bar mode
fig_lca_eu.update_layout(barmode='group')
st.plotly_chart(fig_lca_eu)



st.subheader('Global Warming Potential in 2020 and 2050 for Food Scenarios')
fig_lca_gw = go.Figure(data=[
    
    go.Bar(name='Baseline: Current Condition', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq']),# ,marker_color='crimson'),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
    go.Bar(name='Future Scenario', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq']),#,marker_color='blue'),
    #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['gwp']),#,marker_color='DarkSlateGrey')  
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Global Warming Potential (kg co2 eq)'}
    }
)
# Change the bar mode
fig_lca_gw.update_layout(barmode='group')
st.plotly_chart(fig_lca_gw)

st.header('Land Use Patterns')


col1, col2 = st.columns(2)

with col1:
    year_LU0 = st.selectbox(
    'Select First Year for Land Usage Patterns:',
        chart_data_base.Model_Year_)
#fig_lca_lu_1 = go.Figure()
#st.bar_chart(chart_data_base[year_LU0])
dflu = chart_data_base.loc[chart_data_base['Model_Year_'] == year_LU0].iloc[0]
dflu = dflu.drop(labels=['Model_Population','Energy_Use_MJ','Freshwater_withdrawals_m3',
                        'TSTAMP','Total_LU_ha',
                        'Global_Warming_Potential_kg_co2_eq'])
dflu=pd.DataFrame(dflu)
dflu0=dflu

lu_base = chart_data_base.drop(columns=['Model_Population','Energy_Use_MJ','Freshwater_withdrawals_m3',
                        'TSTAMP','Total_LU_ha',
                        'Commodity_crops_corn_soy',
                        'Pasture_LU_ha',
                        'Global_Warming_Potential_kg_co2_eq'])

yearchoice= lu_base.loc[lu_base['Model_Year_'] ==year_LU0]

# create a bar plot of the selected row
dflut=dflu.transpose()
newdf0=pd.DataFrame()
newdf0['Protein']=dflut['Protein_cropland']+dflut['Protein_pasture_forage']
newdf0['Dairy']=dflut['Dairy_cropland']+dflut['Dairy_pasture_forage']
newdf0['Fruit']=dflut['Fruit_orchard_vineyard']+dflut['Fruit_berry_melon']
newdf0['Vegetables']=dflut['Vegetables_specialty']+dflut['Vegetables_field']
newdf0['Grains']=dflut['Grains']
newdf0['Oil']=dflut['Oil']
newdf0['Sugar']=dflut['Sugar']

fig_lca_lu_1 = go.Figure(data=[go.Bar(x=newdf0.columns, y=newdf0.values.flatten())])

# add x-axis and y-axis labels
fig_lca_lu_1.update_layout(xaxis_title='Food Group', 
                    yaxis_title='Total agricultural land use (ha)',
                    margin=dict(l=10, r=10, t=10, b=10))

# show the plot
#st.plotly_chart(fig_lca_lu_1)


 

with col2:
    # have default value of selected year as 2050
    # reorder chart_data_base to have 2050 first
    chart_data_base = chart_data_base.sort_values(by='Model_Year_', ascending=False)
    year_LU1 = st.selectbox(
    'Select Second Year for Land Usage Patterns:',
        chart_data_base.Model_Year_)
#fig2 = go.Figure()
#st.bar_chart(chart_data_base[year_LU])
dflu = chart_data_base.loc[chart_data_base['Model_Year_'] == year_LU1].iloc[0]
dflu = dflu.drop(labels=['Model_Population','Energy_Use_MJ','Freshwater_withdrawals_m3',
                        'TSTAMP','Total_LU_ha',
                        'Global_Warming_Potential_kg_co2_eq'])
dflu=pd.DataFrame(dflu)

lu_base = chart_data_base.drop(columns=['Model_Population','Energy_Use_MJ','Freshwater_withdrawals_m3',
                        'TSTAMP','Total_LU_ha',
                        'Commodity_crops_corn_soy',
                        'Pasture_LU_ha',
                        'Global_Warming_Potential_kg_co2_eq'])

yearchoice= lu_base.loc[lu_base['Model_Year_'] ==year_LU1]

# create a bar plot of the selected row
dflut=dflu.transpose()
newdf1=pd.DataFrame()
newdf1['Protein']=dflut['Protein_cropland']+dflut['Protein_pasture_forage']
newdf1['Dairy']=dflut['Dairy_cropland']+dflut['Dairy_pasture_forage']
newdf1['Fruit']=dflut['Fruit_orchard_vineyard']+dflut['Fruit_berry_melon']
newdf1['Vegetables']=dflut['Vegetables_specialty']+dflut['Vegetables_field']
newdf1['Grains']=dflut['Grains']
newdf1['Oil']=dflut['Oil']
newdf1['Sugar']=dflut['Sugar']

fig_lca_lu_2 = go.Figure(data=[go.Bar(x=newdf1.columns, y=newdf1.values.flatten())])

# add x-axis and y-axis labels
fig_lca_lu_2.update_layout(xaxis_title='Food Group', 
                    yaxis_title='Total agricultural land use (ha)',
                    margin=dict(l=10, r=10, t=10, b=10))

# show the plot
#st.plotly_chart(fig_lca_lu_2)

figx= go.Figure()

figx.add_trace(go.Bar(x=newdf0.columns, y=newdf0.values.flatten(),name=year_LU0))
figx.add_trace(go.Bar(x=newdf1.columns, y=newdf1.values.flatten(),name=year_LU1))

st.plotly_chart(figx)
with col1:
    if st.checkbox(f'Land Use dataset for year {year_LU0}'):
            dflu0 
with col2:
    if st.checkbox(f'Land Use dataset for year {year_LU1} '):
            dflu 


if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   


