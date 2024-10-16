import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Integrated Modeling", page_icon="INFEWS_icon_whitebg.png")
st.title('Integrated Modeling Framework')

'''
To generate information about combined impacts of food-energy-water systems, a framework was developed to combine the various models that describe both current conditions and potential future conditions. The integrated models rely on output from one model (e.g. the ABM) to provide estimates of future land use for production of different crop types (such as row crops or table food crops) which serve as inputs to other models (ABM and SWAT) used to determine associated environmental impacts.''''''
'''
'''
After establishing a baseline, the ABM can be used to generate outputs for hypothetical situations in which producers have access to more/improved information and can respond to changes in profitability or demand for different crops (or other factors), which can again be used as inputs to the other models. This allows analyses of different levels of production for row crops and table foods at different scales and over different time periods in a data-driven approach known as co-simulation.
'''

# Include the image MSAInFlow.png
st.image('Outer_MSA_Flow.png')