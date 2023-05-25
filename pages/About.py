import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.write('#:information_source: Iowa UrbanFEWS ')  


if st.checkbox('Show avocado demo'):
    @st.cache_data
    def load_data(path):
        dataset = pd.read_csv(path)
        return dataset
    avocado = load_data('avocado.csv')
    avocado_stats = avocado.groupby('type')['average_price'].mean()
    st.dataframe(avocado_stats)
    with st.form('line_chart'):
        selected_geography = st.selectbox(label='Geography', options=avocado['geography'].unique())
        submitted = st.form_submit_button('Submit')
        if submitted:
            filtered_avocado = avocado[avocado['geography'] == selected_geography]
            line_fig = px.line(filtered_avocado,
                            x='date', y='average_price',
                            color='type',
                            title=f'Avocado Prices in {selected_geography}')
            st.plotly_chart(line_fig)