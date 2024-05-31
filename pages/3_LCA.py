import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="LCA",
    page_icon="🌾",
)

st.image('LCAlogo.png', width=100)
st.write('#  :ear_of_rice: LCA - Life Cycle Assessment of Food Systems :tomato:')  

st.write(rf'Food systems in the US are complex and often have embedded largescale elements (national and global). In Iowa, about 90% of table food is imported from outside of the state. Our team of researchers are using models to explore what would happen if up to half of the food eaten in the Des Moines area was produced locally.') 
st.write(rf'Life Cycle Assessment (LCA) is a modeling tool that accounts for energy use and environmental impacts of the food system cycle. Our team is using an LCA model developed by scientists at the US Environmental Protection Agency to determine the amount of energy used at every food system stage and to adjust the model for some important (Iowa-specific) local differences.')
st.write(rf'For example, the scale of fruit and vegetable farms in Iowa is much smaller on average (8 acres) compared to California (59 acres) where about half of fruits and vegetables in the US are currently grown. This smaller scale has an effect on production methods: for example, which labor is done by hand or with equipment, and what quantity of pesticides are used. In addition, there are important environmental differences such as temperature, rainfall and production seasonality (of course in Des Moines and surrounding areas we don’t grow vegetables outside during the winter!).')
st.write(rf'We have met with a set of production specialists to quantify the current local food system and build a model for current conditions, and our next step will be to make projections to allow us to model future food system changes and energy use. ')


chart_data_base = pd.read_pickle(r'lca_base.pickle')

chart_data = pd.read_pickle(r'lca_local.pickle')
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

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



st.header('Land Use Patterns')


col1, col2 = st.columns(2)

with col1:
    year_LU0 = st.selectbox(
    'Select Year 1 to view Land Use Patterns:',
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

# Show the land use patterns 

with col2:
    # have default value of selected year as 2050
    # reorder chart_data_base to have 2050 first
    chart_data_base = chart_data_base.sort_values(by='Model_Year_', ascending=False)
    year_LU1 = st.selectbox(
    'Select Year 2 to view Land Use Patterns:',
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

# Show the drop down menus for the two years
fig_lca_lu= go.Figure()

fig_lca_lu.add_trace(go.Bar(x=newdf0.columns, y=newdf0.values.flatten(),name=year_LU0, marker_color='blue'))
fig_lca_lu.add_trace(go.Bar(x=newdf1.columns, y=newdf1.values.flatten(),name=year_LU1, marker_color='red'))

#add x-axis and y-axis labels on fig_lca_lu 
fig_lca_lu.update_layout(xaxis_title='Food Group', 
                yaxis_title='Total agricultural land use (ha)',
                margin=dict(l=10, r=10, t=10, b=10))

st.plotly_chart(fig_lca_lu)

''' Note: '''
'''Fruit (orchard/vineyard) includes all perennial fruits - Apple, Cherry, Grape, Pear		'''
'''Fruit (berry/melon) includes Melon, Blueberry, Raspberry, Strawberry		'''
'''Vegetable (field) include sweet corn, pumpkin, snap beans, dried beans, and pea, all other vegetables are listed as Vegetable (specialty)		'''


st.header('Current vs Future scenario:')

cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    ''' Current amount of local food production '''
    '''Models 50% of dietary requirements in 2020 with current production (about 5% local and 45% distant) based on consumption patterns ''' 

with colb:
    st.subheader('Future Scenario')
    '''Increased local food production within Des Moines Metropolitan Statistical Area (MSA)'''
    '''Models 50% of dietary requirements in 2040 with all local production based on current consumption patterns'''




st.subheader('Energy use in 2020 and 2050 for Food Scenarios')
fig_lca_eu = go.Figure(data=[
    
    go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], marker_color='blue'),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'],marker_color='red')
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
    
    go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq'], marker_color='blue'),# ,marker_color='crimson'),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
    go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq'],marker_color='red'),#,marker_color='blue'),
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


if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   


# To show just th bar plot of the selected row
#fig_lca_lu_2 = go.Figure(data=[go.Bar(x=newdf1.columns, y=newdf1.values.flatten())])

# show the plot
#st.plotly_chart(fig_lca_lu_2)