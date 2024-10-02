import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Iowa UrbanFEWS", page_icon="INFEWS_icon_whitebg.png")

# include an image
st.image('IowaUrbanFEWSlogo.png')

st.title('Integrated Models for the Des Moines Metropolitan Area') 

''' **Welcome to the integrated models dashboard!** ''' 
'''     **👈 Please use the sidebar to explore  specific models/pages describing the project framework.**'''
''' ''' 
''' '''
'''This dashboard was developed for the Iowa Urban Food- Energy- Water Systems (FEWS) integrated modeling project.  The project is designed to assess the potential for and impact of scaling up table food production near urban areas in the rainfed landscapes of the Midwest. Many cities in this region are heavily dependent on table food imported from great distances which can have negative environmental and social effects. ''' 
'''The Des Moines Metropolitan Statistical Area (MSA) in central Iowa is the focus of this study. An integrated modeling framework allows investigation of how climate, crop production, land use, buildings, energy consumption, and environmental impacts are related to one another.  This approach allows us to examine current impacts and predict the likely future effects of expected or hypothetical changes in policies, farming methods, technology, social interactions, and market trends that affect table food production.'''
''' '''
''' The set of models used in this project include an agent-based model (ABM), a life-cycle assessment (LCA) model, a soil and water assessment model (SWAT), and a weather (climate) research and forecasting (WRF) model (please use the sidebar to access additional information on the individual models).'''

abm_container = st.container()
col1, mid, col2 = st.columns([1, 1,20]) # change to [1,1,20] to experiment with a mid col between col1 and col2
with abm_container:
    with col1:
        st.image('ABMlogo.png', width=70)
    with col2:
        '''Agent-based model (ABM): Based on characteristics and intentions of producers in the study area, the ABM includes simulated “agents” who can respond to changes in factors (such as markets, profitability, technical innovation and information) as they make decisions about land allocation for production of different crop types (e.g., row crops or table food crops).'''

lca_container = st.container()
col1, mid, col2 = st.columns([1, 1,20]) # change to [1,1,20] to experiment with a mid col between col1 and col2
with lca_container:
    with col1:
        st.image('LCAlogo.png', width=70)
    with col2:
        '''Life-cycle assessment model (LCA): Using data for the local food system, LCA models include estimates of energy inputs, product outputs and environmental impacts associated with different potential patterns of land allocation for row crop or table food production.  Specific impacts measured include global warming potential (from greenhouse gas emissions associated with production), as well as energy, water and land used for production.'''

swat_container = st.container()
col1, mid, col2 = st.columns([1, 1,20]) # change to [1,1,20] to experiment with a mid col between col1 and col2
with swat_container:
    with col1:
        st.image('SWATlogo.png', width=70)
    with col2:
        '''Soil and Water Assessment Tool (SWAT):'''




# add MSA image 
# st.image('MSA_models.jpg')

st.markdown(
    '''    
    ### Want to learn more?
    :bookmark_tabs: Return to the [Iowa UrbanFEWS website](https://iowa-urbanfews.cber.iastate.edu/)

    :speech_balloon: Have a suggestion? Please leave your comments in the [feedback survey](https://iastate.qualtrics.com/jfe/form/SV_5BVuGwhpC1s1RR4) 
    
    :email: Contact us at '''
    '<a href="mailto:infews@iastate.edu">infews@iastate.edu!</a>', unsafe_allow_html=True

)

# Include QR code 
# st.image('Streamlit_QR_Code.png')
