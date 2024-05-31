import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="CoSim", page_icon=":computer:")
st.title(':computer: :handshake: CoSim : CoSimulation  :computer: ')

'''
We're particularly interested in understanding how different factors like policies, farming methods, technology, social interactions, and market trends affect food production.
''''''
To do this, we use a method called data-driven **co-simulation**'''
''' 
This means we combine various models that simulate food, energy, and water systems, allowing us to analyze them together at different scales and over different time periods.
'''

# Include the image MSAInFlow.png
st.image('Outer_MSA_Flow.png')