import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Co-Simulation",
    page_icon="🌾",
)

st.write('#  :ear_of_rice: LCA - Life Cycle Assessment of Food Systems :tomato:')  

'''
Co-simulation is an advanced technique that combines multiple simulation models to analyze complex systems more comprehensively. This method synchronizes different models to simulate how various parts of a system interact, offering a more detailed view than single simulations. By utilizing co-simulation, engineers and scientists can simulate complex interactions within systems like those found in engineering and environmental studies, without the need for costly and time-consuming physical prototypes.
''''''
In co-simulation, different models—often from legacy systems with vast amounts of code—are integrated using either "intrusive" or "non-intrusive" methods. Intrusive coupling melds these models into a new software package, while non-intrusive coupling treats them as separate but interactable units through advanced computing techniques. This can include creating 'wrapper' algorithms that help these systems communicate effectively, often through modern computational tools like cloud computing.
''''''
A practical application of non-intrusive co-simulation is in industries like automotive and aerospace, where different aspects such as manufacturing and safety are modeled separately but need to interact seamlessly. Co-simulation provides a powerful tool for these and other fields, helping to optimize systems for better performance and efficiency.
'''