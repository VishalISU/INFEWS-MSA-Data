import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# include an image
st.image('IowaUrbanFEWSlogo.png')

st.title(':city_sunrise: Metropolitan Statistical Area CoSimulation :deciduous_tree:') 

''' **Welcome to the Metropolitan Statistical Area CoSimulation dashboard!** ''' 
'''     **👈 Before you navigate to a page from the sidebar** let us introduce our study to you...'''
''' ''' 
''' ''' 
'''Our study site is the Des Moines-West Des Moines Metropolitan Statistical Area (MSA), Iowa. 
We've created a framework that allows us to look at how the climate, land use, buildings, energy consumption, and environmental impacts all interact. 
We're particularly interested in understanding how different factors like policies, farming methods, technology, social interactions, and market trends affect food production.
re 
To do this, we use a method called data-driven **co-simulation**... but first let's get to know our models!'''

st.image('MSA_models.jpg')





st.markdown(
    '''    
    ### Want to learn more?
    :bookmark_tabs: Check out [Iowa Urban FEWS website](https://iowa-urbanfews.cber.iastate.edu/)

    :speech_balloon: Have a suggestion? Please leave your comments in the [feedback survey](https://iastate.qualtrics.com/jfe/form/SV_5BVuGwhpC1s1RR4) 
    
    :email: Contact us at '''
    '<a href="mailto:infews@iastate.edu">infews@iastate.edu!</a>', unsafe_allow_html=True

)

# Include QR code 
st.image('Streamlit_QR_Code.png')
