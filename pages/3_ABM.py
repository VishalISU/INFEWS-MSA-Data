import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="ABM", page_icon="👨‍🌾")
st.write('# :female-farmer: ABM Dashboard :male-farmer:')

# Read total data from total_msa_data.csv 
csv_file = 'total_msa_data.csv'
df0 = pd.read_csv(csv_file, header=None, index_col=0, names=['Value'])
categories = df0.index.tolist()
values = df0['Value'].tolist()

# Create a bar chart for total data
fig0 = go.Figure(go.Bar(
    x=categories,
    y=values,
    marker=dict(color=['green', 'green', 'blue', 'blue', 'purple', 'purple',
                       'orange', 'orange', 'brown', 'yellow', 'pink', 'gray']),
    text=values,
    textposition='auto',
    texttemplate='%{text:.2s}'
))

# Original layout and configuration
original_layout = {
    'yaxis': {'type': 'log', 'title': 'Amount in hectares (log scale)'},
    'title': 'Agent Based Land Use in Hectares (Logarithmic Scale)',
    'xaxis': {'title': 'Categories', 'tickangle': 45},
    'bargap': 0.15
}

fig0.update_layout(**original_layout)
fig0.update_layout(
    updatemenus=[{
        # Add a button that does plotly reset axes 
        
        'direction': 'down',
        'showactive': False,
        'x': 0.1,
        'xanchor': 'left',
        'y': 1.15,
        'yanchor': 'top'
    }]
)
fig0.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
st.plotly_chart(fig0)

### Add county level data
counties = ['Guthrie', 'Jasper', 'Polk', 'Madison', 'Dallas', 'Warren']
data = {}
for county in counties:
    file_name = f'{county.lower()}_data.csv'
    df = pd.read_csv(file_name, header=None, index_col=0, names=['Value'])
    formatted_df = pd.DataFrame({
        'Category': df.index.tolist(),
        'Value': df['Value'].tolist()
    })
    data[county] = formatted_df

# Function to update the plot based on selected county
def update_plot(county):
    df = data[county]
    return {
        'x': [df['Category'].tolist()],
        'y': [df['Value'].tolist()],
        'type': 'bar',
        'marker': {
            'color': ['green', 'green', 'blue', 'blue', 'purple', 'purple', 'orange', 'orange', 'brown', 'yellow', 'pink', 'gray']
        },
        'text': [df['Value'].tolist()],
        'textposition': 'auto',
        'texttemplate': '%{text:.2s}'
    }

# Initialize the figure with the first county data and set up dropdown
fig = go.Figure(data=[go.Bar(x=data['Guthrie']['Category'], y=data['Guthrie']['Value'], marker=dict(color=['green', 'green', 'blue', 'blue', 'purple', 'purple', 'orange', 'orange', 'brown', 'yellow', 'pink', 'gray']), text=data['Guthrie']['Value'], textposition='auto', texttemplate='%{text:.2s}')])

fig.update_layout(
    yaxis=dict(type='log', title='Amount in hectares (log scale)'),
    title=f'Commodity Production by Land Use in Hectares - County Level (Logarithmic Scale)',
    xaxis=dict(title='Categories', tickangle=45),
    bargap=0.15,
    updatemenus=[{
        'type': 'buttons',  # Specify the type as 'buttons' to always show all buttons
        'buttons': [{'method': 'restyle', 'label': county, 'args': [update_plot(county)]} for county in counties],
        'direction': 'right',
        #'pad': {'r': 10, 't': 10},
        'showactive': True,
        'x': 0.1,
        'xanchor': 'left',
        'y': 1.1,
        'yanchor': 'top'
    }]
)
st.plotly_chart(fig)


