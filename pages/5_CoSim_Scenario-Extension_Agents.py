import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ABM", page_icon="👨‍🌾")
st.write('# :female-farmer: ABM Dashboard - Extension Agents Scenario :male-farmer:')

base_dir = "ABM_ext/"

# Read data from CSV files
df_2020 = pd.read_csv(base_dir + 'total_msa_sum_20.csv', header=None, index_col=0, names=['Value 2020'])
df_2050 = pd.read_csv(base_dir + 'total_msa_sum_50.csv', header=None, index_col=0, names=['Value 2050'])
df_combined = df_2020.join(df_2050)

categories = df_2020.index.tolist()
default_categories = categories[:-1]
selected_categories = st.multiselect('Select categories to display:', categories, default=default_categories)
filtered_df = df_combined.loc[selected_categories]

fig = go.Figure(data=[
    go.Bar(name='2020', x=filtered_df.index, y=filtered_df['Value 2020'], marker_color='blue'),
    go.Bar(name='2050', x=filtered_df.index, y=filtered_df['Value 2050'], marker_color='red')
])
fig.update_layout(
    barmode='group',
    title='Comparison of Agent Based Land Use in 2020 vs 2050',
    xaxis=dict(title='Categories', tickangle=-45),
    yaxis=dict(type='log', title='Amount in acres (log scale)'),
    bargap=0.15
)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
st.plotly_chart(fig)


# County level data display
counties = ['Guthrie', 'Jasper', 'Polk', 'Madison', 'Dallas', 'Warren']
selected_county = st.selectbox('Select a county:', counties)

county_data_2020 = pd.read_csv(base_dir + f'{selected_county.lower()}_20.csv', header=None, index_col=0, names=['Value 2020'])
county_data_2050 = pd.read_csv(base_dir + f'{selected_county.lower()}_50.csv', header=None, index_col=0, names=['Value 2050'])
county_data_combined = county_data_2020.join(county_data_2050).loc[selected_categories]

fig2 = go.Figure(data=[
    go.Bar(name='2020', x=county_data_combined.index, y=county_data_combined['Value 2020'], marker_color='green'),
    go.Bar(name='2050', x=county_data_combined.index, y=county_data_combined['Value 2050'], marker_color='orange')
])
fig2.update_layout(
    #barmode='group',
    title=f'Comparison of {selected_county} County Land Use in 2020 vs 2050',
    xaxis=dict(title='Categories', tickangle=-45),
    yaxis=dict(type='log', title='Amount in acres (log scale)'),
    bargap=0.15
)
st.plotly_chart(fig2)


# Also plot row crops vs the rest in a pie chart for 2020 and 2050 

# Write the overall description below the charts
st.write('Contribution of row crops vs table crops in 2050')

fig_pie = go.Figure(data=[go.Pie(labels=df_combined.index, values=df_combined['Value 2050'], hole=0.3)])
fig_pie.update_layout(title='2050', title_x=0.5)  # Center the title
# Adjust the figure size here
st.plotly_chart(fig_pie, use_container_width=True)  # This makes the plot responsive to the column width
fig_pie.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=1,
        font=dict(size=10),itemwidth=30
    ))
    

st.write('#  :ear_of_rice: LCA Insights')  #st.title('Avocado Prices dashboard')

#col1, col2 = st.columns(2)

#with col1:

st.header('Current Baseline vs Future Local Scenario:')

chart_data_base = pd.read_pickle(r'lca_base.pickle')

chart_data = pd.read_pickle(r'lca_abm_base.pickle')
 

#st.subheader('Base Model Population, Land Use over Year')
base_data_popLU= chart_data_base.drop(chart_data_base.columns[[0,4,5,6]],axis=1)
base_data_popLU=base_data_popLU.rename(columns={'Total LU (ha)':'Land Use (ha)'})

#line_fig_base1=px.line(base_data_popLU,x='Model_Year_',y=['Model Population','Land Use (ha)'], markers=True)
#st.plotly_chart(line_fig_base1)


# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

#baseplot= baseplot.query("`Model_Year_`==2020")
#baseplot 
# Drop columns and rows not needed for plotting 
localplot= chart_data.drop(chart_data.columns[[0,2,3,5]],axis=1)
localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
#localplot 
# Load the Raw data from LCA 

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw

# postprocess raw results before plotting to compare with cosim 
rbaseplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='BASE'")
rbaseplot=rbaseplot.query("`year`==2020 |`year`==2050")
rlocalplot=chart_data_raw.query("cosim=='LCA' & fsscenario=='LOCAL'")
#rbaseplot
#rlocalplot
#line_fig=px.line(localplot,x='Model_Year_',y=['Energy_Use_MJ','Global_Warming_Potential_kg_co2_eq'], markers=True)
#st.plotly_chart(line_fig)

st.subheader('Energy use in 2020 and 2050 for Food Scenarios')
fig_lca_eu = go.Figure(data=[
    
    go.Bar(name='Baseline: Current Condition', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ']),# marker_color=000000),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
    go.Bar(name='Future Scenario', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ']),#,marker_color='blue'),
    #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Energy Use (MJ)'}
    }
)
# Change the bar mode
fig_lca_eu.update_layout(barmode='group')
st.plotly_chart(fig_lca_eu)


st.subheader('Global Warming Potential in 2020 and 2050 for Food Scenarios')
fig_lca_gw = go.Figure(data=[
    
    go.Bar(name='Baseline: Current Condition', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq']),# ,marker_color='crimson'),
    #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
    go.Bar(name='Future Scenario', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq']),#,marker_color='blue'),
    #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['gwp']),#,marker_color='DarkSlateGrey')  
    ],
    layout={
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Global Warming Potential (kg co2 eq)'}
    }
)
# Change the bar mode
fig_lca_gw.update_layout(barmode='group')
st.plotly_chart(fig_lca_gw)
