#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go 
import os 
import time

#%%
#Force Streamlit to work in wide mode 
#%%s
st.set_page_config(
    page_title="SWAT",
    page_icon="SWATlogo.png",
)


st.image('SWATlogo.png', width=100)

st.write('# SWAT - Soil and Water Assessment Tool') 

'''The Soil and Water Assessment Tool (SWAT) can be used to model movement of water and associated nutrients and sediments, and to quantify crop growth based on  land management practices. '''
'''The SWAT model requires inputs for climate, topography, soil type, land cover, and crop management systems to generate outputs including streamflow rates  and nitrate, phosphorus, and sediment loads to characterize conditions for watersheds in specific areas.'''
'''To allow examination of upstream and within-metro effects on water quality, our SWAT models include the North and South Raccoon Rivers, the North and South Skunk, the Middle Des Moines River, and the Lake Red Rock watersheds (Figure 1). Together, these watersheds are part of a large system that drains to and through the Des Moines area. Historical data for river and stream parameters are used to calibrate initial models that are then  used to assess 'what if?' scenarios for the future.'''

st.image('DMRBforWebsite.png', caption='Figure 1. Watershed boundaries for river systems in the area (dark line), county boundaries for the Des Moines metropolitan area (brown line) and location of the City of Des Moines (gray shaded area).')

'''Here we compare SWAT outputs for current and future scenarios of local food production within the Des Moines Metropolitan Statistical Area (MSA).'''



cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    '''Current amount of local food production (about 5% local) in Des Moines metropolitan area for land use and crop yield in 2020'''
with colb:
    st.subheader('Future Scenario')
    '''Increased local food production (50% local) in Des Moines metro  area for land use and yield in 2050.'''

# base file 
base_dir='SWAT_base_2025/'

# Invoke mgt2pkl function for SWAT_base_2025
# mgt2pkl('SWAT_base_2025','output.mgt')
# Invoke rch2csv function for SWAT_base_2025
# rch2csv('SWAT_base_2025\\output.rch')

# LINE PLOT OF FLOW_OUTcms, SED_OUTtons, and NO3_OUTkg on separate plots
df_20to50_rch = pd.read_csv(base_dir+'SWAT_base_2025_rch_output.csv')

# Plot line plot of FLOW_OUTcms vs MON, renaming MON for Year
df_20to50_rch.rename(columns={'MON': 'Year'}, inplace=True)
fig_flow = px.line(df_20to50_rch, x='Year', y='FLOW_OUTcms', title='Current and future yearly streamflow')
# Update x-axis label
fig_flow.update_xaxes(title_text="Year")
# Update y-axis label to say m^3/s
fig_flow.update_yaxes(title_text="Stream Flow (m^3/s)")
# Plot linear trendline
# fig_flow.add_traces(px.line(df_20to50_rch, x='Year', y='FLOW_OUTcms', trendline="ols").data)

# --- Compute trendline using px.scatter ---
trend_fig = px.scatter(df_20to50_rch, x='Year', y='FLOW_OUTcms', trendline="ols")

# Extract only the trendline trace (usually trace index 1)
trendline_trace = [
    t for t in trend_fig.data
    if t.mode == 'lines'   # this filters out the raw data points
]

# Add trendline to original figure
for t in trendline_trace:
    t.update(line=dict(dash='dot', width=1))
    fig_flow.add_trace(t)
# Use plotly go muted blue color for FLOW plot
fig_flow.update_traces(line=dict(color='royalblue'))
# Plot
st.plotly_chart(fig_flow)

# Plot line plot of SED_OUTtons vs MON, renaming MON for Year
fig_sed = px.line(df_20to50_rch, x='Year', y='SED_OUTtons', title='Current and future yearly sediment load')
# Update x-axis label
fig_sed.update_xaxes(title_text="Year")
# Update y-axis label
fig_sed.update_yaxes(title_text="Sediment Load (metric tons)")

# Add trendline to SED plot
trend_fig_sed = px.scatter(df_20to50_rch, x='Year', y='SED_OUTtons', trendline="ols")
# Extract only the trendline trace (usually trace index 1)  
trendline_trace_sed = [
    t for t in trend_fig_sed.data
    if t.mode == 'lines'   # this filters out the raw data points
]
# Add trendline to original figure
for t in trendline_trace_sed:
    t.update(line=dict(dash='dot', width=1))
    fig_sed.add_trace(t)

# use plotly go cooked asparagus green for SED plot
fig_sed.update_traces(line=dict(color='darkgreen'))

# Plot
st.plotly_chart(fig_sed)


# Plot line plot of NO3_OUTkg vs MON, renaming MON for Year
fig_no3 = px.line(df_20to50_rch, x='Year', y='NO3_OUTkg', title='Current and future yearly nitrate load')
# Update x-axis label
fig_no3.update_xaxes(title_text="Year") 
# Update y-axis label
fig_no3.update_yaxes(title_text="Nitrate Load (kg)")

# Add trendline to NO3 plot
trend_fig_no3 = px.scatter(df_20to50_rch, x='Year', y='NO3_OUTkg', trendline="ols")
# Extract only the trendline trace (usually trace index 1)
trendline_trace_no3 = [
    t for t in trend_fig_no3.data
    if t.mode == 'lines'   # this filters out the raw data points
]
# Add trendline to original figure
for t in trendline_trace_no3:
    t.update(line=dict(dash='dot', width=1))
    fig_no3.add_trace(t)

# use plotly go brick red for no3 plot
fig_no3.update_traces(line=dict(color='firebrick'))
# Plot
st.plotly_chart(fig_no3)

# Plot line plot of TOT Pkg vs MON, renaming MON for Year 
fig_totp = px.line(df_20to50_rch, x='Year', y='TOT Pkg', title='Current and future yearly total phosphorus load')
# Update x-axis label   
fig_totp.update_xaxes(title_text="Year")
# Update y-axis label
fig_totp.update_yaxes(title_text="Total Phosphorus Load (kg)")
# Add trendline to TOT P plot
trend_fig_totp = px.scatter(df_20to50_rch, x='Year', y='TOT Pkg', trendline="ols")
# Extract only the trendline trace (usually trace index 1)
trendline_trace_totp = [
    t for t in trend_fig_totp.data
    if t.mode == 'lines'   # this filters out the raw data points
] 
# Add trendline to original figure
for t in trendline_trace_totp:
    t.update(line=dict(dash='dot', width=1))
    fig_totp.add_trace(t)
# use plotly go dark orange for totp plot
fig_totp.update_traces(line=dict(color='mediumorchid'))
# Plot
st.plotly_chart(fig_totp)

# Insert option to show dataframe upon clicking 
if st.checkbox('Show Streamflow, Sediment, Nitrate and Phosphate Data'):
    st.write(df_20to50_rch)

# '''
# LINE PLOT OF CROP YIELDS
# '''
st.subheader('Crop Yields after SWAT Simulation')
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
# Load the continuous data : 
df_20to50=pd.read_pickle(base_dir+'/'+'mktbl_2020_2029.pickle')

# Filter and clean data
unwanted_values = ["HAY", "WATR", "WETF", "WETN"]
df_20to50 = df_20to50[~df_20to50.index.isin(unwanted_values)]

# Further filter out some row crops such as ALFA, FESC, SWRN, HAY
unwanted_rowcrops = ["ALFA", "FESC", "SWRN", "HAY"]
df_20to50 = df_20to50[~df_20to50.index.isin(unwanted_rowcrops)] 
# make new crop_codes dictionary without unwanted crops
crop_codes = {k: v for k, v in crop_codes.items() if k not in unwanted_rowcrops}


# Select a crop
# order crop_codes alphabetically by value but from the second value

crop_list = sorted(crop_codes.items(), key=lambda item: item[1])
selected_crop = st.selectbox('Select a Crop', options=crop_list, format_func=lambda x: x[1])
selected_crop_code = selected_crop[0]

# Plot a line plot of the selected crop yields over the years
crop_series = df_20to50.loc[selected_crop_code]
# convert the row into a long dataframe 
crop_df = crop_series.reset_index()
crop_df.columns = ['Year', 'Yield']
# crop_df['Year'] = crop_df['Year'].astype(int)

# Create line plot
fig_crop_yield = px.line(crop_df, x="Year", y="Yield", title=f'Crop Yield over Years for {selected_crop[1]}')
# Update x-axis label
fig_crop_yield.update_xaxes(title_text="Year")
# Update y-axis label
fig_crop_yield.update_yaxes(title_text="Yield (kg/ha)")
# Plot
st.plotly_chart(fig_crop_yield)

# Show data if checkbox is selected
if st.checkbox(f'Show Crop Yield Data for {selected_crop[1]}'):
    st.write(crop_df)
# Show the dataframe if checkbox is selected
if st.checkbox('Show All Crop Yield Data'):
    st.write(df_20to50)