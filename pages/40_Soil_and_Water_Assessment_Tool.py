#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

#Force Streamlit to work in wide mode 
#%%
st.set_page_config(
    page_title="SWAT",
    page_icon="SWATlogo.png",
)


st.image('SWATlogo.png', width=100)

st.write('# SWAT - Soil and Water Assessment Tool') 



# swat_container = st.container()
# col1, col2 = st.columns([5,30]) # change to [1,1,20] to experiment with a mid col between col1 and col2
# with swat_container:
#     with col1:
#         st.image('SWATlogo.png', width=100)
#     with col2:
#         st.write('# SWAT - Soil and Water Assessment Tool') 


'''
The Soil and Water Assessment Tool (SWAT) can be used to model movement of water and associated nutrients and sediments, and quantify crop growth based on land management practices. 
''''''
The SWAT model requires inputs for climate, topography, soil, land cover, and crop management systems to generate outputs including streamflow rates, evapotranspiration, subsurface tile drainage flow, as well as nitrate, phosphorus, and sediment loads to characterize conditions for watersheds in specific areas. 
''''''
To allow detection of upstream and within-metro effects on water quality, our SWAT models include the North and South Raccoon River, North and South Skunk, the Middle Des Moines River, and the Lake Red Rock watersheds. 
''''''
Together, these watersheds are part of a large system that drains to and through the Des Moines area. Our SWAT experts are using data from the past 10 years or more to calibrate the initial models that will be used to create ‘what if?’ scenarios for the future. 
''''''
 Here we compare the current and future scenarios for local food production within the Des Moines Metropolitan Statistical Area (MSA)'''


st.image('swatimage.png', caption='Des Moines River Basin')



cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    '''Current amount of local food production '''
    '''Models land use and yield conditions for 2020'''
with colb:
    st.subheader('Future Scenario')
    '''Increased local food production within Des Moines Metropolitan Statistical Area (MSA)'''
    '''Models future land use with 50% local production and future yield conditions for 2050'''

# base file 
base_dir='SWAT_base/'

'''
BOX PLOT OF FLOW_OUTcms, SED_OUTtons, and NO3_OUTkg
'''
# Plot box plots of FLOW_OUTcms , SED_OUTtons and No3_OUTkg, comparing the Historical and Future scenarios from TxtInOutHist_rch_output and TxtInOutFut_rch_output
#%%
# base file 
#base_dir='SWAT_base/'
# Load the historical and future data
df_2020_rch = pd.read_csv(base_dir+'TxtInOutHist_rch_output.csv')
df_2050_rch = pd.read_csv(base_dir+'TxtInOutFut_rch_output.csv')
df_2020_rch.set_index('Unnamed: 0', inplace=True)
df_2050_rch.set_index('Unnamed: 0', inplace=True)

# Select all data for FLOW_OUTcms, SED_OUTtons and No3_OUTkg for df 2020 and 2050 for RCH column value of 1
#df_2020_rch = df_2020_rch.loc[['FLOW_OUTcms', 'SED_OUTtons', 'No3_OUTkg'], df_2020_rch.columns.str.contains('1')]

#df_2020_rch = df_2020_rch.loc[ '362'  ]
# df_2050_rch = df_2050_rch.loc[:, df_2050_rch.columns.str.contains('1')]

filtered_df_2020_rch = df_2020_rch[df_2020_rch['RCH'] == 362]
filtered_df_2020_rch = filtered_df_2020_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_2020_rch = filtered_df_2020_rch[filtered_df_2020_rch['MON'] >= 1000]

rch_data_Current = filtered_df_2020_rch  

filtered_df_2050_rch = df_2050_rch[df_2050_rch['RCH'] == 362]
filtered_df_2050_rch = filtered_df_2050_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_2050_rch = filtered_df_2050_rch[filtered_df_2050_rch['MON'] >= 1000]

rch_data_Future = filtered_df_2050_rch

# combine data
rch_data_Current['Dataset'] = 'Current Scenario'
rch_data_Future['Dataset'] = 'Future Scenario'
combined_data_rch = pd.concat([rch_data_Current, rch_data_Future])

# Plot boxplot for FLOW_OUTcms 
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='FLOW_OUTcms', title='Boxplot for Streamflow (cubic meters)')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Stream Flow (cubic meters)")
# Update layout to remove legend
fig_swat_box_rch.update_layout(showlegend=False)
# Plot 
st.plotly_chart(fig_swat_box_rch)

# Plot boxplot for SED_OUTtons
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='SED_OUTtons', title='Boxplot for Sediment Load (metric tons)')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Sediment Load (metric tons)")
# Update layout to remove legend
fig_swat_box_rch.update_layout(showlegend=False)
# Plot
st.plotly_chart(fig_swat_box_rch)

# Plot boxplot for No3_OUTkg
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='NO3_OUTkg', title='Boxplot for Nitrate (kilograms)')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Nitrate (kilograms)")
# Update layout to remove legend
fig_swat_box_rch.update_layout(showlegend=False)
# Plot
st.plotly_chart(fig_swat_box_rch)


if st.checkbox('Show Historical Data'):
    st.write(df_2020_rch)
if st.checkbox('Show Future Data'):
    st.write(df_2050_rch)



'''
BOX PLOT OF CROP YIELDS
'''

#%%
# Crop codes dictionary
crop_codes = {
    "ALFA": "Alfalfa", "APPL": "Apple", "BLUE": "Blueberry", "BROC": "Broccoli",
    "CABG": "Cabbage", "CHER": "Cherry", "COLG": "Collard greens", "CORN": "Corn",
    "CRRT": "Carrot", "CUCM": "Cucumber", "DRYB": "Dry beans", "KALE": "Kale",
    "GRAP": "Grape", "HMEL": "Honeydew melon", "LETT": "Lettuce", "ONIO": "Onion",
    "PEAR": "Pear", "POTA": "Potato", "PUMP": "Pumpkin", "RASP": "Raspberry",
    "SCRN": "Sweet corn", "SNPB": "Snap beans", "SOYB": "Soybean", "SPIN": "Spinach", "SPOT": "Sweet potato",
    "SQUA": "Squash", "STRW": "Strawberry", "TOMA": "Tomato", 
    "WWHT" : "Winter Wheat",
    #"BROM": "Meadow Bromegrass", "HAY": "Hay", 
    #"CANA": "Canola oil", "SGBT": "Sugar beet", 
    # Above are missing in TxtInOutHist and Fut
    "FESC": "Tall Fescue"
    
}


#%%
# Load the historical and future data
df_2020 = pd.read_csv(base_dir+'TxtInOutHist_output.csv')
df_2050 = pd.read_csv(base_dir+'TxtInOutFut_output.csv')
df_2020.set_index('Unnamed: 0', inplace=True)
df_2050.set_index('Unnamed: 0', inplace=True)

# Filter and clean data
unwanted_values = ["HAY", "WATR", "WETF", "WETN"]
df_2020_filtered = df_2020[~df_2020.index.isin(unwanted_values)]
df_2050_filtered = df_2050[~df_2050.index.isin(unwanted_values)]

#%%
# df_2020_filtered.drop(columns=['AVG'], inplace=True)
# df_2050_filtered.drop(columns=['AVG'], inplace=True)

df_2020_filtered = df_2020_filtered.loc[:, df_2020_filtered.columns != 'AVG']
df_2050_filtered = df_2050_filtered.loc[:, df_2050_filtered.columns != 'AVG']


# Select a crop
# order crop_codes alphabetically by value but from the second value 

crop_codes = dict(sorted(crop_codes.items(), key=lambda item: item[1]))
selected_crop_code = st.selectbox('Select a Crop', options=list(crop_codes.keys()), format_func=lambda x: crop_codes[x])

# Extract data for selected crop and specific years
data_1995_2004 = df_2020_filtered.loc[selected_crop_code, '1995':'2004'].reset_index()
data_2039_2048 = df_2050_filtered.loc[selected_crop_code, '2039':'2048'].reset_index()
#%%
data_1995_2004['Dataset'] = 'Current Scenario'
data_2039_2048['Dataset'] = 'Future Scenario'

# Combine data
combined_data = pd.concat([data_1995_2004, data_2039_2048])

#%%
# Plot boxplot
fig_swat_box = px.box(combined_data, x='Dataset', y=selected_crop_code, title=f'Boxplot for {crop_codes[selected_crop_code]}')
# Update x-axis label
fig_swat_box.update_xaxes(title_text="Scenario")

# Update y-axis label
fig_swat_box.update_yaxes(title_text="Yield (kg/ha)")

# Update layout to remove legend
fig_swat_box.update_layout(showlegend=False)

#Plot
st.plotly_chart(fig_swat_box)
