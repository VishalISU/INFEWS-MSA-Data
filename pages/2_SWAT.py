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


st.write('# :seedling: SWAT MSA Dashboard :droplet: ') 

st.header('Current Baseline vs Future Local Scenario:')


# Crop codes dictionary
crop_codes = {
    "ALFA": "Alfalfa", "APPL": "Apple", "BLUE": "Blueberry", "BROC": "Broccoli",
    "CABG": "Cabbage", "CHER": "Cherry", "COLG": "Collard greens", "CORN": "Corn",
    "CRRT": "Carrot", "CUCM": "Cucumber", "DRYB": "Dry beans", "KALE": "Kale",
    "GRAP": "Grape", "HMEL": "Honeydew melon", "LETT": "Lettuce", "ONIO": "Onion",
    "PEAR": "Pear", "POTA": "Potato", "PUMP": "Pumpkin", "RASP": "Raspberry",
    "SCRN": "Sweet corn", "SOYB": "Soybean", "SPIN": "Spinach", "SPOT": "Sweet potato",
    "SQUA": "Squash", "STRW": "Strawberry", "TOMA": "Tomato", "FESC": "Tall Fescue",
    "BROM": "Meadow Bromegrass", "HAY": "Hay", "CANP": "Canola oil", "SGBT": "Sugar beat",
    "SNPB": "Snap beans"
}

# base file 
base_dir='SWAT_base/'
# Load the historical and future data
df_2020 = pd.read_csv(base_dir+'TxtInOutHist_output.csv')
df_2050 = pd.read_csv(base_dir+'TxtInOutFut_output.csv')
df_2020.set_index('Unnamed: 0', inplace=True)
df_2050.set_index('Unnamed: 0', inplace=True)

# Filter and clean data
unwanted_values = ["HAY", "WATR", "WETF", "WETN", "WWHT"]
df_2020_filtered = df_2020[~df_2020.index.isin(unwanted_values)]
df_2050_filtered = df_2050[~df_2050.index.isin(unwanted_values)]
df_2020_filtered.drop(columns=['AVG'], inplace=True)
df_2050_filtered.drop(columns=['AVG'], inplace=True)

# Select a crop
selected_crop_code = st.selectbox('Select a Crop', options=list(crop_codes.keys()), format_func=lambda x: crop_codes[x])

# Extract data for selected crop and specific years
data_1995_2004 = df_2020_filtered.loc[selected_crop_code, '1995':'2004'].reset_index()
data_2039_2048 = df_2050_filtered.loc[selected_crop_code, '2039':'2048'].reset_index()
data_1995_2004['Year Range'] = '1995-2004'
data_2039_2048['Year Range'] = '2039-2048'

# Combine data
combined_data = pd.concat([data_1995_2004, data_2039_2048])

# Plot boxplot
fig = px.box(combined_data, x='Year Range', y=selected_crop_code, title=f'Boxplot for {crop_codes[selected_crop_code]} over the Selected Years')
st.plotly_chart(fig)
