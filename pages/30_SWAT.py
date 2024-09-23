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
    page_icon="💧",
)


st.image('SWATlogo.png', width=100)

st.write('# :seedling: SWAT - Soil and Water Assessment Tool :droplet: ') 

st.image('swatimage.png', caption='Des Moines River Basin')




'''
The Soil and Water Assessment Tool (SWAT) is an eco-hydrological model that we are using to quantify crop growth, hydrological cycling, nutrient transport, erosion processes, sediment transport, and transport of pesticides/pathogens associated with cropping systems and other land management practices. 
''''''
We include inputs for climate, topography, soil, land cover, and crop management systems to generate outputs including streamflow rates, evapotranspiration, subsurface tile drainage flow, as well as nitrate, phosphorus, and sediment loads to characterize current conditions for watersheds linked to the Des Moines area. 
''''''
To allow detection of upstream and within-metro effects on water quality, our SWAT models include the North and South Raccoon River, North and South Skunk, the Middle Des Moines River, and the Lake Red Rock watersheds. 
''''''
Together, these watersheds are part of a large system that drains to and through the Des Moines area. Our SWAT experts are using data from the past 10 years or more to calibrate the initial models that will be used to create ‘what if?’ scenarios for the future. 
'''


st.header('Current vs Future scenario:')

''' Here we compare the current and future scenarios for local food production within the Des Moines Metropolitan Statistical Area (MSA)'''


cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    '''Current amount of local food production '''
    '''Models land use and yield conditions for 2020'''
with colb:
    st.subheader('Future Scenario')
    '''Increased local food production within Des Moines Metropolitan Statistical Area (MSA)'''
    '''Models future land use with 50% local production and future yield conditions for 2050'''

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

# base file 
base_dir='SWAT_base/'
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
df_2020_filtered.drop(columns=['AVG'], inplace=True)
df_2050_filtered.drop(columns=['AVG'], inplace=True)

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
fig_swat_box = px.box(combined_data, x='Dataset', y=selected_crop_code, title=f'Boxplot for {crop_codes[selected_crop_code]} over the Selected Years')
# Update x-axis label
fig_swat_box.update_xaxes(title_text="Scenario")

# Update y-axis label
fig_swat_box.update_yaxes(title_text="Yield (kg/ha)")

# Update layout to remove legend
fig_swat_box.update_layout(showlegend=False)

#Plot
st.plotly_chart(fig_swat_box)



