#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
#%%
st.set_page_config(
    page_title="LCA",
    page_icon="LCAlogo.png",
)

st.image('LCAlogo.png', width=100)
st.write('# LCA - Life Cycle Assessment of Food Systems ')  

'''Food systems are complex and interlinked with national and global systems. In Iowa, about 90% of table food is imported from outside of the state. In this project models are being used to predict the effects of transitions in land use that would support local production of 50% of residents’ dietary needs.'''
'''Life Cycle Assessment (LCA) is a modeling tool that accounts for energy use and environmental impacts of the food system cycle. Our team uses an LCA model to determine the amount of energy used at each food system stage and to assess related changes in the production of greenhouse gas emissions.'''
'''Currently, fruit and vegetable farms in Iowa are much smaller (8 acres on average) compared to California (59 acres), where about half of fruits and vegetables in the US are currently grown.  Production on smaller scale farms affects cultivation methods such as whether labor is done by hand or with equipment and the quantity of pesticides used. In addition, there are important differences such as temperature, rainfall and production seasonality.'''
'''Several crop specialists were involved in characterizing the current local food production system to characterize conditions for table food production in Iowa, and the LCA will be used to predict future food system changes and related outputs, such as energy use.'''



#%%
chart_data_base = pd.read_pickle(r'lca_base.pickle')

chart_data_local = pd.read_pickle(r'lca_local.pickle')
 
#%%
#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})
#%%
# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

# Drop columns and rows not needed for plotting 
localplot= chart_data_local.drop(chart_data_local.columns[[0,2,3,5]],axis=1)
localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
#localplot 
# Load the Raw data from LCA 

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw

# postprocess raw results before plotting to compare with cosim 
rbaseplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='BASE'")
rbaseplot=rbaseplot.query("`year`==2020 |`year`==2050")
rlocalplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='LOCAL'")

#%%

st.header('Land Use Patterns - Current Baseline')


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

#%%
st.header('Current vs Future scenario:')

cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    '''Current amount of local food production (about 5% local) in Des Moines metropolitan area for land use and crop yield in 2020.'''
with colb:
    st.subheader('Future Scenario')
    ''' Increased local food production (50% local) in Des Moines metro area for land use and yield in 2050.'''


#%%

# Plot a line graph for all years for the two scenarios to show land use for protein dariy fruits vegetables grains oil and sugar
fig_lca_lu_pog = go.Figure()
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Protein_cropland']+chart_data_base['Protein_pasture_forage'], name='Protein: future', 
                        line = dict(color='darkred', width=4, dash='dash')))      
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Oil'], name='Oil: future', 
                        line = dict(color='darkgoldenrod', width=4, dash='dash')))
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Grains'], name='Grains: future', 
                        line = dict(color='darkkhaki', width=4, dash='dash')))
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Protein_cropland']+chart_data_local['Protein_pasture_forage'], name='Protein: current', marker_color='blue',
                        line=dict(color='darkred', width=4, dash='solid')))
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Oil'], name='Oil: current', marker_color='gold',
                        line=dict(color='darkgoldenrod', width=4, dash='solid')))
fig_lca_lu_pog.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Grains'], name='Grains: current', marker_color='green',
                        line=dict(color='darkkhaki', width=4, dash='solid')))


fig_lca_lu_pog.update_layout(
                    title='Land Use Patterns for Protein, Oil and Grains',
                   xaxis_title='Year',
                   yaxis_title='Total agricultural land use (ha)')
st.plotly_chart(fig_lca_lu_pog)



# Plot a line graph for all years for the two scenarios to show land use for dairy, fruit, vegetables and sugar
fig_lca_lu_rest = go.Figure()
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Dairy_cropland']+chart_data_base['Dairy_pasture_forage'], name='Dairy: future', 
                        line = dict(color='dodgerblue', width=4, dash='dash')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Fruit_orchard_vineyard']+chart_data_base['Fruit_berry_melon'], name='Fruit: future', 
                        line = dict(color='darkorange', width=4, dash='dash'))) 
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Vegetables_specialty']+chart_data_base['Vegetables_field'], name='Vegetables: future', 
                        line = dict(color='forestgreen', width=4, dash='dash')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Sugar'], name='Sugar: future', 
                        line = dict(color='grey', width=4, dash='dash')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Dairy_cropland']+chart_data_local['Dairy_pasture_forage'], name='Dairy: current', marker_color='blue',
                        line=dict(color='dodgerblue', width=4, dash='solid')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Fruit_orchard_vineyard']+chart_data_local['Fruit_berry_melon'], name='Fruit: current', marker_color='orange',
                        line=dict(color='darkorange', width=4, dash='solid')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Vegetables_specialty']+chart_data_local['Vegetables_field'], name='Vegetables: current', marker_color='green',
                        line=dict(color='forestgreen', width=4, dash='solid')))
fig_lca_lu_rest.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Sugar'], name='Sugar: current', marker_color='purple',
                        line=dict(color='grey', width=4, dash='solid')))

fig_lca_lu_rest.update_layout(
                    title='Land Use Patterns for Dairy, Fruit, Vegetables and Sugar',
                   xaxis_title='Year',
                   yaxis_title='Total agricultural land use (ha)')
st.plotly_chart(fig_lca_lu_rest)    

#%%

st.subheader('Energy use in 2020 and 2050 for Food Scenarios')

#fig_lca_eu = go.Figure(data=[
    
    #go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], marker_color='blue'),
    ##go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    #go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'],marker_color='red')
    ##go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
    #],
    #layout={
    #    'xaxis': {'title': 'Year'},
    #    'yaxis': {'title': 'Energy Use (MJ)'}
    #}
#)
# Change the bar mode
#fig_lca_eu.update_layout(barmode='group')
#st.plotly_chart(fig_lca_eu)

# Plot a line graph of the energy use for all years for all years for the two scenarios
fig_lca_eu = go.Figure()
fig_lca_eu.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Energy_Use_MJ'], name='Current', 
                    line=dict(color='deepskyblue', width=4, dash='solid')))
fig_lca_eu.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Energy_Use_MJ'], name='Future', 
                    line=dict(color='deepskyblue', width=4, dash='dash')))
fig_lca_eu.update_layout(
                   xaxis_title='Year',
                   yaxis_title='Energy Use (MJ)')
st.plotly_chart(fig_lca_eu)


st.subheader('Global Warming Potential in 2020 and 2050 for Food Scenarios')
# fig_lca_gw = go.Figure(data=[
    
#     go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq'], marker_color='blue'),# ,marker_color='crimson'),
#     #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
#     go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq'],marker_color='red'),#,marker_color='blue'),
#     #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['gwp']),#,marker_color='DarkSlateGrey')  
#     ],
#     layout={
#         'xaxis': {'title': 'Year'},
#         'yaxis': {'title': 'Global Warming Potential (kg co2 eq)'}
#     }
# )
# # Change the bar mode
# fig_lca_gw.update_layout(barmode='group')
# st.plotly_chart(fig_lca_gw)

# Plot a line graph of the global warming potential for all years for two scenarios
fig_lca_gw = go.Figure()
fig_lca_gw.add_trace(go.Scatter(x=chart_data_base['Model_Year_'], y=chart_data_base['Global_Warming_Potential_kg_co2_eq'], name='Current', 
                                line=dict(color='orangered', width=4, dash='solid')))
fig_lca_gw.add_trace(go.Scatter(x=chart_data_local['Model_Year_'], y=chart_data_local['Global_Warming_Potential_kg_co2_eq'], name='Future',  
                                line=dict(color='orangered', width=4, dash='dash')))
fig_lca_gw.update_layout(
                   xaxis_title='Year',
                   yaxis_title='Global Warming Potential (kg co2 eq)')
st.plotly_chart(fig_lca_gw)




if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data_local   




# To show just th bar plot of the selected row
#fig_lca_lu_pog = go.Figure(data=[go.Bar(x=newdf1.columns, y=newdf1.values.flatten())])

# show the plot
#st.plotly_chart(fig_lca_lu_pog)