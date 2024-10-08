import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="Contact Us!", page_icon="INFEWS_icon_whitebg.png")


st.write('# Contact Us!')  #st.title('Avocado Prices dashboard')


st.markdown(
    '''    
    ### Want to learn more?
    :bookmark_tabs: Check out [Iowa Urban FEWS website](https://iowa-urbanfews.cber.iastate.edu/)

    :speech_balloon: Have a suggestion? Please leave your comments in the [feedback survey](https://iastate.qualtrics.com/jfe/form/SV_5BVuGwhpC1s1RR4) 
    
    :email: Contact us at '''
    '<a href="mailto:infews@iastate.edu">infews@iastate.edu!</a>', unsafe_allow_html=True

)

# Include QR code  
#st.image('Streamlit_QR_Code.png')
