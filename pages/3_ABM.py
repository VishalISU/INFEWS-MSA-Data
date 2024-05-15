import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="ABM",
    page_icon="👨‍🌾",
)

st.write('# :female-farmer: ABM Dashboard :male-farmer: ')  #st.title('Avocado Prices dashboard')


# Data provided by the user
categories = ['Protein (Cropland)', 'Protein (Pasture)', 'Dairy (Cropland)', 'Dairy (Pasture)',
              'Fruit1', 'Fruit2', 'Veg1', 'Veg2', 'Grain', 'Oil', 'Sugar', 'Commodity']
values = [3058.309274, 24401.91894, 83.06602052, 4355.651536, 35.31102581, 8.740770844,
          7.416743226, 1.523870968, 544.2243564, 1.323174194, 1.923870968, 246241.6858]


st.subheader('Barchart')
# Create a bar chart
fig1 = go.Figure(go.Bar(
    x=categories,
    y=values,
    marker=dict(color=['green', 'green', 'blue', 'blue', 'purple', 'purple',
                       'orange', 'orange', 'brown', 'yellow', 'pink', 'gray']),
    text=values,  # This adds text labels to each bar
    textposition='auto',  # Automatically places the text on the bars
    texttemplate='%{text:.2s}'  # Text template for formatting the hover info
))

# Set the y-axis to a logarithmic scale
fig1.update_layout(
    yaxis=dict(type='log', title='Amount (log scale)'),
    title='Commodity Production by Land Use in Grams (Logarithmic Scale)',
    xaxis=dict(title='Categories', tickangle=45),
    bargap=0.15,  # Adjust the distance between bars
)

# Add a grid to the chart
fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')

# Show the figure
st.plotly_chart(fig1)
