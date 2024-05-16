import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go




st.write('# :city_sunrise: Iowa Urban FEWS Dashboard :deciduous_tree:')  #st.title('Avocado Prices dashboard')

st.markdown(
    '''     **👈 Select a page from the sidebar** to get started exploring the data  '''
)
# Include the image MSAInFlow.png
st.image('MSAInFlow.png')

st.markdown(
    '''    
    ### Want to learn more?
    - Check out [Iowa Urban FEWS website](https://iowa-urbanfews.cber.iastate.edu/)
    - :speech_balloon: Have a suggestion? Please leave your comments in the [feedback survey](https://iastate.qualtrics.com/jfe/form/SV_5BVuGwhpC1s1RR4) 
    - Contact us at '''
    '<a href="mailto:infews@iastate.edu">infews@iastate.edu!</a>', unsafe_allow_html=True

)

