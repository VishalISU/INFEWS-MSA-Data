import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ABM", page_icon="ABMlogo.png")

st.image('ABMlogo.png', width=100)
st.write('# ABM - Agent Based Model')


# Include a brief description of the model 
'''Agent-based models (ABM)  can be used to simulate behaviors of individuals and/or defined  groups of individuals. In the UrbanFEWS project, the agents simulate Iowa farmers and their decisions about crop production.'''
'''The agents in the model can engage in independent decision-making and action, acquire new information, adjusttheir behavior, and revise or refine their decisions over time based on their goals and interactions with others.'''
'''We used information from focus groups and surveys conducted in our study area to construct "personas" representing Iowa farmers ,  .  The ABM model allows experimentation to assess the effects of various policy changes or other factors on agent decisions and behaviors.The output of the ABM model indicates land area allocated for different crops (corn and soybean, or fruits and vegetables) which can then be used as input to other models.'''

base_dir = "ABM_base/"

# Read data from CSV files
df_2020 = pd.read_csv(base_dir + 'total_msa_sum_20.csv', header=None, index_col=0, names=['Value 2020'])
df_2050 = pd.read_csv(base_dir + 'total_msa_sum_50.csv', header=None, index_col=0, names=['Value 2050'])
df_combined = df_2020.join(df_2050)

categories = df_2020.index.tolist()
default_categories = categories[:-1]
selected_categories = st.multiselect('One instance of an ABM gives us the below land use patterns:', categories, default=default_categories)
filtered_df = df_combined.loc[selected_categories]

fig = go.Figure(data=[
    go.Bar(name='2020', x=filtered_df.index, y=filtered_df['Value 2020'], marker_color='olive'),
    go.Bar(name='2050', x=filtered_df.index, y=filtered_df['Value 2050'], marker_color='turquoise')
])
fig.update_layout(
    barmode='group',
    title='Comparison of Agent Based Land Use in 2020 vs 2050',
    xaxis=dict(title='Categories', tickangle=-45),
    yaxis=dict(type='log', title='Amount in acres (log scale)'),
    bargap=0.15
)
fig.update_yaxes(showgrid=True, gridwidth=1)
st.plotly_chart(fig)

''' Note: '''
'''Fruit (orchard/vineyard) includes all perennial fruits - Apple, Cherry, Grape, Pear		'''
'''Fruit (berry/melon) includes Melon, Blueberry, Raspberry, Strawberry		'''
'''Vegetable (field) include sweet corn, pumpkin, snap beans, dried beans, and pea''' 
'''All other vegetables are listed as Vegetable (specialty)		'''


# # County level data display
# st.write('Individual county land use patterns are also modeled')

# counties = ['Guthrie', 'Jasper', 'Polk', 'Madison', 'Dallas', 'Warren']
# selected_county = st.selectbox('Select a county below to view the land use patterns:', counties)

# county_data_2020 = pd.read_csv(base_dir + f'{selected_county.lower()}_20.csv', header=None, index_col=0, names=['Value 2020'])
# county_data_2050 = pd.read_csv(base_dir + f'{selected_county.lower()}_50.csv', header=None, index_col=0, names=['Value 2050'])
# county_data_combined = county_data_2020.join(county_data_2050).loc[selected_categories]

# fig2 = go.Figure(data=[
#     go.Bar(name='2020', x=county_data_combined.index, y=county_data_combined['Value 2020'], marker_color='blue'),
#     go.Bar(name='2050', x=county_data_combined.index, y=county_data_combined['Value 2050'], marker_color='red')
# ])
# fig2.update_layout(
#     #barmode='group',
#     title=f'Comparison of {selected_county} County Land Use in 2020 vs 2050',
#     xaxis=dict(title='Categories', tickangle=-45),
#     yaxis=dict(type='log', title='Amount in acres (log scale)'),
#     bargap=0.15
# )
# st.plotly_chart(fig2)


# Also plot row crops vs the rest in a pie chart for 2020 and 2050 

st.write('Even a substantial increase in production of table crops does not significantly reduce the overall contribution of row crops to the land use patterns.')
st.write('The pie chart below illustrates the contribution of row crops vs table crops in 2050.')
st.write('')


# # Write the overall description below the charts
# st.write(' **Contribution of row crops vs table crops in 2050** ')

# fig_pie = go.Figure(data=[go.Pie(labels=df_combined.index, values=df_combined['Value 2050'], hole=0.3)])
# fig_pie.update_layout(title='2050', title_x=0.5)  # Center the title
# # Adjust the figure size here
# st.plotly_chart(fig_pie, use_container_width=True)  # This makes the plot responsive to the column width
# fig_pie.update_layout(legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=-0.5,
#         xanchor="right",
#         x=1,
#         font=dict(size=10),itemwidth=30
#     ))
    

