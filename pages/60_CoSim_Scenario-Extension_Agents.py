#%%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
#%%
st.set_page_config(page_title="CoSim-Extension Agents", page_icon="INFEWS_icon_whitebg.png")
st.title('CoSimulation Scenario : Extension Agents')

st.header('ABM Extension Agent Intervention')
base_dir = "ABM_ext/"

# Read data from CSV files
df_2020 = pd.read_csv(base_dir + 'total_msa_sum_20.csv', header=None, index_col=0, names=['Value 2020'])
df_2050 = pd.read_csv(base_dir + 'total_msa_sum_50.csv', header=None, index_col=0, names=['Value 2050'])
df_combined = df_2020.join(df_2050)

categories = df_2020.index.tolist()
default_categories = categories[:-1]
selected_categories = st.multiselect('Select categories to display:', categories, default=default_categories)
filtered_df = df_combined.loc[selected_categories]

fig = go.Figure(data=[
    go.Bar(name='2020', x=filtered_df.index, y=filtered_df['Value 2020'], marker_color='blue'),
    go.Bar(name='2050', x=filtered_df.index, y=filtered_df['Value 2050'], marker_color='red')
])
fig.update_layout(
    barmode='group',
    title='Comparison of Agent Based Land Use in 2020 vs 2050',
    xaxis=dict(title='Categories', tickangle=-45),
    yaxis=dict(type='log', title='Amount in acres (log scale)'),
    bargap=0.15
)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
st.plotly_chart(fig)


# # County level data display
# counties = ['Guthrie', 'Jasper', 'Polk', 'Madison', 'Dallas', 'Warren']
# selected_county = st.selectbox('Select a county:', counties)

# county_data_2020 = pd.read_csv(base_dir + f'{selected_county.lower()}_20.csv', header=None, index_col=0, names=['Value 2020'])
# county_data_2050 = pd.read_csv(base_dir + f'{selected_county.lower()}_50.csv', header=None, index_col=0, names=['Value 2050'])
# county_data_combined = county_data_2020.join(county_data_2050).loc[selected_categories]

# fig2 = go.Figure(data=[
#     go.Bar(name='2020', x=county_data_combined.index, y=county_data_combined['Value 2020'], marker_color='blue'),
#     go.Bar(name='2050', x=county_data_combined.index, y=county_data_combined['Value 2050'], marker_color='red')
# ])
# fig2.update_layout(
#     #barmode='group',
#     title=f'Comparison of {selected_county} County Land Use in 2020 vs 2050',
#     xaxis=dict(title='Categories', tickangle=-45),
#     yaxis=dict(type='log', title='Amount in acres (log scale)'),
#     bargap=0.15
# )
# st.plotly_chart(fig2)


# Also plot row crops vs the rest in a pie chart for 2020 and 2050 

# Write the overall description below the charts
# ''' **Contribution of row crops vs table crops in 2050** '''

# fig_pie = go.Figure(data=[go.Pie(labels=df_combined.index, values=df_combined['Value 2050'], hole=0.3)])
# fig_pie.update_layout(title='2050', title_x=0.5)  # Center the title
# # Adjust the figure size here
# st.plotly_chart(fig_pie, use_container_width=True)  # This makes the plot responsive to the column width

# fig_pie.update_layout(legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=-0.5,
#         xanchor="right",
#         x=1,
#         font=dict(size=10),itemwidth=30
#     ))
''' 
Even after intervention by extension agents, the overall contribution of row crops to the land use patterns remains significant.
'''
## _________________________________________________SWAT ________________________________________________________________________
#%%
st.header('SWAT maps farmer activity to available HRUs ') 

import plotly.express as px
# Updated Crop codes dictionary with "CANA" for Canola oil
crop_codes = {
    "ALFA": "Alfalfa", "APPL": "Apple", "BLUE": "Blueberry", "BROC": "Broccoli",
    "CABG": "Cabbage", "CHER": "Cherry", "COLG": "Collard greens", "CORN": "Corn",
    "CRRT": "Carrot", "CUCM": "Cucumber", "DRYB": "Dry beans", "KALE": "Kale",
    "GRAP": "Grape", "HMEL": "Honeydew melon", "LETT": "Lettuce", "ONIO": "Onion",
    "PEAR": "Pear", "POTA": "Potato", "PUMP": "Pumpkin", "RASP": "Raspberry",
    "SCRN": "Sweet corn", "SOYB": "Soybean", "SPIN": "Spinach", "SPOT": "Sweet potato",
    "SQUA": "Squash", "STRW": "Strawberry", "TOMA": "Tomato", "FESC": "Tall Fescue",
    #"BROM": "Meadow Bromegrass", 
    "WWHT" : "Winter Wheat",
    "HAY": "Hay", "CANA": "Canola oil", "SGBT": "Sugar beet",
    "SNPB": "Snap beans"
}

#%%
# Base file directory
base_dir='SWAT_base/'

#%%
# Load the historical and future data
df_swat_abm_base = pd.read_csv(base_dir+'TxtInOutABM_base_output.csv')
df_swat_abm_ext = pd.read_csv(base_dir+'TxtInOutABM_ext_output.csv')
df_swat_abm_base.set_index('Unnamed: 0', inplace=True)
df_swat_abm_ext.set_index('Unnamed: 0', inplace=True)

# Filter and clean data
unwanted_values = [ "WATR", "WETF", "WETN"] # Removed HAY and WWHT from unwanted values
df_swat_abm_base_filtered = df_swat_abm_base[~df_swat_abm_base.index.isin(unwanted_values)]
df_swat_abm_ext_filtered = df_swat_abm_ext[~df_swat_abm_ext.index.isin(unwanted_values)]
df_swat_abm_base_filtered.drop(columns=['AVG'], inplace=True)
df_swat_abm_ext_filtered.drop(columns=['AVG'], inplace=True)

# Order crop_codes alphabetically by value
crop_codes = dict(sorted(crop_codes.items(), key=lambda item: item[1]))
selected_crop_code = st.selectbox('Select a Crop', options=list(crop_codes.keys()), format_func=lambda x: crop_codes[x])
#%%
# Extract data for selected crop across all available years
data_swat_abm_base = df_swat_abm_base_filtered.loc[selected_crop_code].reset_index()
data_swat_abm_ext = df_swat_abm_ext_filtered.loc[selected_crop_code].reset_index()
data_swat_abm_base['Dataset'] = 'Base Scenario'
data_swat_abm_ext['Dataset'] = 'Extension Agents Intervention'

# Combine data
combined_data = pd.concat([data_swat_abm_base, data_swat_abm_ext])
#%%
# Plot boxplot
fig_swat_box = px.box(combined_data, x='Dataset', y=selected_crop_code, color='Dataset', 
                      title=f'Boxplot Comparison for {crop_codes[selected_crop_code]} ')

# Update x-axis label
fig_swat_box.update_xaxes(title_text="Scenario")

# Update y-axis label
fig_swat_box.update_yaxes(title_text="Yield (kg/ha)")

# Update layout to remove legend
fig_swat_box.update_layout(showlegend=False)

st.plotly_chart(fig_swat_box)

''' At the end of swat the marketable yields are calculated for each crop and this is used as input to LCA'''
    
## _________________________________________________LCA ________________________________________________________________________


st.header(' Life Cycle Analysis of Food Systems ')  

st.subheader('Base vs Extension Agent scenario:')

chart_data_base = pd.read_pickle(r'lca_abm_base.pickle')

chart_data = pd.read_pickle(r'lca_abm_ext.pickle')
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
#baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

# Drop columns and rows not needed for plotting 
localplot= chart_data.drop(chart_data.columns[[0,2,3,5]],axis=1)
#localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
#localplot 
# Load the Raw data from LCA 

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw


st.subheader('Energy use in 2020 and 2050 for Food Scenarios')

fig_lca_eu = go.Figure() 
fig_lca_eu.add_trace(go.Scatter(x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], name='Base Scenario',
                                line=dict(color='deepskyblue', width=4, dash='solid')))
fig_lca_eu.add_trace(go.Scatter(x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'], name='Extension Agent Scenario', 
                                line=dict(color='deepskyblue', width=4, dash='dash')))


# fig_lca_eu = go.Figure(data=[
    
#     go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], marker_color='blue'),
#     #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
#     go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'],marker_color='red')
#     #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
#     ],
#     layout={
#         'xaxis': {'title': 'Year'},
#         'yaxis': {'title': 'Energy Use (MJ)'}
#     }
# )
# #Change the bar mode
# fig_lca_eu.update_layout(barmode='group')

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

fig_lca_gw = go.Figure()
fig_lca_gw.add_trace(go.Scatter(x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq'], name='Base Scenario',
                                line=dict(color='orangered', width=4, dash='solid')))
fig_lca_gw.add_trace(go.Scatter(x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq'], name='Extension Agent Scenario',
                                line=dict(color='orangered', width=4, dash='dash')))

st.plotly_chart(fig_lca_gw)


if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   
