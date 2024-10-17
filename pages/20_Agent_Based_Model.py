import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as n_colors
import pickle

st.set_page_config(page_title="ABM", page_icon="ABMlogo.png")

st.image('ABMlogo.png', width=100)
st.write('# ABM - Agent Based Model')


# Include a brief description of the model 
'''Agent-based models (ABM)  can be used to simulate behaviors of individuals and/or defined  groups of individuals. In the UrbanFEWS project, the agents simulate Iowa farmers and their decisions about crop production (e.g. to grow row crops or table food crops).'''
'''The agents in the model can engage in independent decision-making and action, acquire new information, adjusttheir behavior, and revise or refine their decisions over time based on their goals and interactions with others.'''
'''We used information from focus groups and surveys conducted in our study area to construct "personas" representing Iowa farmers.  The ABM model allows experimentation to assess the effects of various policy changes or other factors on farmer agent decisions and behaviors. The output of the ABM model indicates land area allocated for different crops (for example, corn and soybean, or fruits and vegetables) which can then be used as input to other models.'''
#___________________________________________________________________________________________
# # OLD visualization code with bar graphs for ABM - No longer preferred 
# base_dir = "ABM_base/"

# # Read data from CSV files
# df_2020 = pd.read_csv(base_dir + 'total_msa_sum_20.csv', header=None, index_col=0, names=['Value 2020'])
# df_2050 = pd.read_csv(base_dir + 'total_msa_sum_50.csv', header=None, index_col=0, names=['Value 2050'])
# df_combined = df_2020.join(df_2050)

# categories = df_2020.index.tolist()
# default_categories = categories[:-1]
# selected_categories = st.multiselect('One instance of an ABM gives us the below land use patterns:', categories, default=default_categories)
# filtered_df = df_combined.loc[selected_categories]

# fig = go.Figure(data=[
#     go.Bar(name='2020', x=filtered_df.index, y=filtered_df['Value 2020'], marker_color='olive'),
#     go.Bar(name='2050', x=filtered_df.index, y=filtered_df['Value 2050'], marker_color='turquoise')
# ])
# fig.update_layout(
#     barmode='group',
#     title='Comparison of Agent Based Land Use in 2020 vs 2050',
#     xaxis=dict(title='Categories', tickangle=-45),
#     yaxis=dict(type='log', title='Amount in acres (log scale)'),
#     bargap=0.15
# )
# fig.update_yaxes(showgrid=True, gridwidth=1)
# st.plotly_chart(fig)

# ''' Note: '''
# '''Fruit (orchard/vineyard) includes all perennial fruits - Apple, Cherry, Grape, Pear		'''
# '''Fruit (berry/melon) includes Melon, Blueberry, Raspberry, Strawberry		'''
# '''Vegetable (field) include sweet corn, pumpkin, snap beans, dried beans, and pea''' 
# '''All other vegetables are listed as Vegetable (specialty)		'''
#___________________________________________________________________________________________
### HERE WE BEGIN THE EXP PLOTS

# Now read from the pickle
df_avg = pd.read_pickle("ABM_exp/df_exp_avg.pkl")

#df_avg 
# Rename for each exp_id rename exp_name as follows: 
# For exp_id = 6 -> Frequent Extension agent intervetion 
df_avg.loc[df_avg['exp_id'] == 6, 'exp_name'] = 'Frequent Extension Agent Intervention'
df_avg.loc[df_avg['exp_id'] == 11, 'exp_name'] = 'Change in Specialty Crops Policies'
df_avg.loc[df_avg['exp_id'] == 27, 'exp_name'] = 'Change in Commodity Crops Policies'
df_avg.loc[df_avg['exp_id'] == 41, 'exp_name'] = 'All Strategies Adopted'

# For 
# Generate distinct colors for each experiment name
unique_experiments = df_avg['exp_name'].unique()
colors = n_colors.qualitative.Bold

# Plot line with band for standard deviation
fig_exp = go.Figure()

# Loop through each experiment name to create individual traces for the line and bands
for idx, exp_name in enumerate(unique_experiments):
    df_exp = df_avg[df_avg['exp_name'] == exp_name]
    
    # Get the color for the current experiment
    color = colors[idx]
    
    # Add the main line for the experiment
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]']+2020, 
        y=df_exp['specialty-acres'], 
        mode='lines',
        name=exp_name,
        legendgroup=exp_name,
        #line=dict(color=color, width=2)  # Assign a unique color to the line
    ))
    
    # # Add the upper bound trace (invisible, just to define the band)
    # fig_exp.add_trace(go.Scatter(
    #     x=df_exp['[step]']+2020, 
    #     y=df_exp['upper_bound_sa'], 
    #     mode='lines', 
    #     line=dict(width=0),
    #     showlegend=False,
    #     #hoverinfo='skip',  # No hover info for this trace
    #     legendgroup=exp_name
    # ))
    
    # # Add the lower bound trace with fill to create the band
    # fig_exp.add_trace(go.Scatter(
    #     x=df_exp['[step]']+2020, 
    #     y=df_exp['lower_bound_sa'], 
    #     mode='lines', 
    #     fill='tonexty', 
    #     line=dict(width=0),
    #     showlegend=False,
    #     #hoverinfo='skip',  # No hover info for this trace
    #     legendgroup=exp_name,
    #     fillcolor=f'rgba{color[3:-1]},0.2)',  # Set same color but with opacity for the band
    # ))

fig_exp.update_layout(
    title='Specialty crops yield over time with different strategies',
    xaxis_title='Year',
    yaxis_title='Specialty crops (Acres)',
    hovermode='x',
    margin=dict(l=0, r=0, t=50, b=50),  # Adjust margins for better fit in Streamlit   
)

# Display the figure in Streamlit
st.plotly_chart(fig_exp) 

# Brief description of the experiments
'''
**Strategy: Increased communication between row crop farmers and specialty farmers via social networks**  
Row crop farmers and specialty crop farmers do not regularly engage in communication. However, if Row crop farmers observe the production success of specialty crop farmers, they might become interested in adopting specialty crop farming practices. This experiment explores the impact of communication between row crop farmers and specialty crop farmers on specialty crop production levels. The experiment examines whether increased interaction between these groups influences row crop farmers to transition to specialty crops, ultimately impacting production output and diversity.

**Strategy: Inclusion of extension agents that support specialty crop production**   
Access to information about new farming technologies and practices is crucial for adoption. One primary way farmers gain such information is through extension services. This experiment assesses the impact of extension agent visits on farmer behavior, specifically regarding the adoption of specialty crops. Two key factors are measured: The number of visits per year – how often extension agents interact with farmers. Typology of row crop farmers – the types of farmers extension agents engage with, focusing on their openness to new practices. The study explores whether frequent, targeted visits by extension agents can accelerate the adoption of specialty crops.

**Strategy: Implementation of policies that support specialty crop production**   
Current policies for specialty crops lag behind those for row crops in areas such as government support, incentives, insurance, supply chain infrastructure, and market access. This experiment investigates the impact of collective policy improvements on the adoption of specialty crops. Policy utility is currently set at 0.5, and the experiment measures the effects of incremental policy improvements: Small change (0.55) – Slight Improvement in at least one factor (e.g., slight increase in incentives or market access). Moderate change (0.6) – Improvement in two or more factors, or a major change in one (e.g., significantly higher incentives). Substantial change (0.65) – Major improvements in two or more areas (e.g., better insurance schemes). High change (0.7) – Significant improvements in multiple factors, such as insurance and supply chain infrastructure. Very high change (0.75) – Comprehensive enhancements across most policy areas, including increased incentives, better insurance, and improved supply chain infrastructure.

**Strategy: Wholescale market demand and accessibility that supports specialty crops production**   
One of the major challenges for specialty crop farmers is the availability of wholesale markets with benchmark prices. This experiment explores the potential possibility of direct wholesale markets or contract opportunities with large institutions as a farmer gains experience with specialty crops. The experiment measures two factors: Years of experience – how long a farmer has been involved in specialty crops. Size of specialty crop operation – the scale at which the farmer produces specialty crops. This experiment aims to assess whether market access improves as farmers gain expertise and expand their operations and whether those who observe this may also adopt specialty crops.

**Strategy: Scaling back policies that support row crop production**   
Policies for row crops are generally more favorable, offering strong government support, incentives, insurance, and supply chain infrastructure. This experiment investigates the potential impact of a decline in these supportive policies. Since the effects may not be uniformly experienced by all farmers, some may face harsher conditions sooner than others. The current maximum policy utility is 0.85, and the experiment considers the following scenarios: Utility between 0.65 and 0.6 – Decline in row crop markets and a reduction in crop subsidies, with low volatility. Utility between 0.65 and 0.5 – Stricter criteria for subsidies and a significant reduction in support, leading to high volatility. Utility between 0.75 and 0.6 – Increased difficulty in securing insurance for row crops, with high market volatility. Utility between 0.75 and 0.5 – Stricter criteria for both insurance approval and subsidies, with very high market volatility.

**Strategy: Reduced price/demand for row crops**      
Row crop farming is highly yield-focused, but many farmers may not fully realize the actual profit utility derived from their production. This experiment explores the factors that lead to a reduction in row crop profits, such as declining market prices or unfavorable market conditions. The experiment focuses on the current profit utility of row crops, set at 0.75, and examines scenarios where farmers might become more aware of declining profits or where market conditions erode their profit margins. The goal is to assess how these realizations might influence a shift toward specialty crops or changes in farming practices.
'''
#  

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

# st.write('Even a substantial increase in production of table crops does not significantly reduce the overall contribution of row crops to the land use patterns.')
# st.write('The pie chart below illustrates the contribution of row crops vs table crops in 2050.')
# st.write('')


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
    

