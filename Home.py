import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


#Force Streamlit to work in wide mode 

#st.set_page_config(layout="wide")

st.set_page_config(
    page_title="IOWAUrbanFEWS",
    page_icon="🌾",
)

st.write('# :city_sunrise: Iowa Urban FEWS Dashboard :deciduous_tree:')  #st.title('Avocado Prices dashboard')

st.markdown(
    '''    This is an app framework built specifically for the IOWA Urban FEWS projects.

    **👈 Select a page from the sidebar** to get started exploring the data 
    ### Want to learn more?
    - Check out [Iowa Urban FEWS website](https://iowa-urbanfews.cber.iastate.edu/)
    - Contact us at '''
    '<a href="mailto:infews@iastate.edu">infews@iastate.edu!</a>', unsafe_allow_html=True

)


