import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as n_colors

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

### HERE WE BEGIN THE EXP PLOTS

file_path = "ABM_exp\output_table_Co_sim_base.csv"
df1 = pd.read_csv(file_path, skiprows=6)
df1 = df1.sort_values(by=['[run number]', '[step]'], ascending=[True, True]).reset_index(drop=True)
df1['exp_id'] = 1

file_path = "ABM_exp\output_table_Co_sim_experiment_extension_4_smt.csv"
df6 = pd.read_csv(file_path, skiprows=6)
df6 = df6.sort_values(by=['[run number]', '[step]'], ascending=[True, True]).reset_index(drop=True)
df6['exp_id'] = 6

file_path = "ABM_exp\output_table_Co_sim_experiment_specialty_pc_5_75.csv"
df11 = pd.read_csv(file_path, skiprows=6)
df11 = df11.sort_values(by=['[run number]', '[step]'], ascending=[True, True]).reset_index(drop=True)
df11['exp_id'] = 11

file_path = "ABM_exp\output_table_Co_sim_experiment_commodity_pc_5_65_50.csv"
df27 = pd.read_csv(file_path, skiprows=6)
df27 = df27.sort_values(by=['[run number]', '[step]'], ascending=[True, True]).reset_index(drop=True)
df27['exp_id'] = 27

file_path = "ABM_exp\output_table_Co_sim_50_percent.csv"
df41 = pd.read_csv(file_path, skiprows=6)
df41 = df41.sort_values(by=['[run number]', '[step]'], ascending=[True, True]).reset_index(drop=True)
df41['exp_id'] = 41


df_main = pd.concat([df1
                    ,df6, df11, df27, df41
                    #  df2, df3, df4, df5, df6, df7, df8, df9, df10,
                    #  df11, df12, df13, df14, df15, df16, df17, df18, df19, df20,
                    #  df21, df22, df23, df24, df25, df26, df27, df28, df29, df30,
                    #  df31, df32, df33, df34, df35, df36, df37, df38, df39, df40, df41
                    ], ignore_index=True)


df_main = df_main.sort_values(by=['exp_id', '[run number]', '[step]'], ascending=[True, True, True]).reset_index(drop=True)

df_main.loc[df_main['[step]'] == 0, 'specialty-acres-change'] = 0

# numeric data columns to take average of outputs
numeric_cols = ["specialty-acres",
                "specialty-acres-change",
                "specialty-supportive",
                "specialty-maybe",
                "specialty-traditional",
                "bad-xp-agents",
                "good-xp-agents",
                "fruit1-g",
                "fruit2-g",
                "veg1-g",
                "veg2-g",
                "grain-g",
                "livestock-g",
                "protein-cropland-g",
                "dairy-cropland-g",
                "oil-g",
                "sugar-g",
                "pasture-g",
                "protein-pasture-g",
                "dairy-pasture-g",
                "commodity-g",
                "fruit1-d",
                "fruit2-d",
                "veg1-d",
                "veg2-d",
                "grain-d",
                "livestock-d",
                "protein-cropland-d",
                "dairy-cropland-d",
                "oil-d",
                "sugar-d",
                "pasture-d",
                "protein-pasture-d",
                "dairy-pasture-d",
                "commodity-d",
                "fruit1-p",
                "fruit2-p",
                "veg1-p",
                "veg2-p",
                "grain-p",
                "livestock-p",
                "protein-cropland-p",
                "dairy-cropland-p",
                "oil-p",
                "sugar-p",
                "pasture-p",
                "protein-pasture-p",
                "dairy-pasture-p",
                "commodity-p",
                "fruit1-j",
                "fruit2-j",
                "veg1-j",
                "veg2-j",
                "grain-j",
                "livestock-j",
                "protein-cropland-j",
                "dairy-cropland-j",
                "oil-j",
                "sugar-j",
                "pasture-j",
                "protein-pasture-j",
                "dairy-pasture-j",
                "commodity-j",
                "fruit1-m",
                "fruit2-m",
                "veg1-m",
                "veg2-m",
                "grain-m",
                "livestock-m",
                "protein-cropland-m",
                "dairy-cropland-m",
                "oil-m",
                "sugar-m",
                "pasture-m",
                "protein-pasture-m",
                "dairy-pasture-m",
                "commodity-m",
                "fruit1-w",
                "fruit2-w",
                "veg1-w",
                "veg2-w",
                "grain-w",
                "livestock-w",
                "protein-cropland-w",
                "dairy-cropland-w",
                "oil-w",
                "sugar-w",
                "pasture-w",
                "protein-pasture-w",
                "dairy-pasture-w",
                "commodity-w"
                ]

# avg of outputs for same experiment number
df_avg = df_main.groupby(['exp_id', '[step]'])[numeric_cols].mean().reset_index()
df_std = df_main.groupby(['exp_id', '[step]'])[numeric_cols].std().reset_index()

#
df_avg.loc[df_avg['exp_id'] == 1, 'exp_name'] = 'Default Conditions'
df_avg.loc[df_avg['exp_id'] == 2, 'exp_name'] = 'Experiment: Good communication between commodity and specialty agents'
# df_avg.loc[df_avg['exp_id'] == 3, 'exp_name'] = 'Experiment: Extension agent, yearly intervention = 1, target strategy = all commodity persona'
# df_avg.loc[df_avg['exp_id'] == 4, 'exp_name'] = 'Experiment: Extension agent, yearly intervention = 4, target strategy = all commodity persona'
# df_avg.loc[df_avg['exp_id'] == 5, 'exp_name'] = 'Experiment: Extension agent, yearly intervention = 1, target strategy = supportive and maybe commodity persona'
df_avg.loc[df_avg['exp_id'] == 6, 'exp_name'] = 'Experiment: Extension agent, yearly intervention = 4, target strategy = supportive and maybe commodity persona'
# df_avg.loc[df_avg['exp_id'] == 7, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2025 (early change), max utility value of specialty crops policies = 0.55 (very less change)'
# df_avg.loc[df_avg['exp_id'] == 8, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2025 (early change), max utility value of specialty crops policies = 0.60 (less change)'
# df_avg.loc[df_avg['exp_id'] == 9, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2025 (early change), max utility value of specialty crops policies = 0.65 (medium change)'
# df_avg.loc[df_avg['exp_id'] == 10, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2025 (early change), max utility value of specialty crops policies = 0.70 (high change)'
df_avg.loc[df_avg['exp_id'] == 11, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2025 (early change), max utility value of specialty crops policies = 0.75 (very high change)'
# df_avg.loc[df_avg['exp_id'] == 12, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2040 (late change), max utility value of specialty crops policies = 0.55 (very less change)'
# df_avg.loc[df_avg['exp_id'] == 13, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2040 (late change), max utility value of specialty crops policies = 0.60 (less change)'
# df_avg.loc[df_avg['exp_id'] == 14, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2040 (late change), max utility value of specialty crops policies = 0.65 (medium change)'
# df_avg.loc[df_avg['exp_id'] == 15, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2040 (late change), max utility value of specialty crops policies = 0.70 (high change)'
# df_avg.loc[df_avg['exp_id'] == 16, 'exp_name'] = 'Experiment: Change is specialty crops policies, change timestep = 2040 (late change), max utility value of specialty crops policies = 0.75 (very high change)'
# df_avg.loc[df_avg['exp_id'] == 17, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 8 OR minimum acerage required = 25'
# df_avg.loc[df_avg['exp_id'] == 18, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 8 OR minimum acerage required = 30'
# df_avg.loc[df_avg['exp_id'] == 19, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 8 OR minimum acerage required = 35'
# df_avg.loc[df_avg['exp_id'] == 20, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 8 OR minimum acerage required = 40'
# df_avg.loc[df_avg['exp_id'] == 21, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 12 OR minimum acerage required = 25'
# df_avg.loc[df_avg['exp_id'] == 22, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 12 OR minimum acerage required = 30'
# df_avg.loc[df_avg['exp_id'] == 23, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 12 OR minimum acerage required = 35'
# df_avg.loc[df_avg['exp_id'] == 24, 'exp_name'] = 'Experiment: Chance of entering wholesale market, minimum years of experience required = 12 OR minimum acerage required = 40'
# df_avg.loc[df_avg['exp_id'] == 25, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2025 (early change), range of utility value for commodity crops policies = 0.65 to 0.60 (low change, low variability)'
# df_avg.loc[df_avg['exp_id'] == 26, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2025 (early change), range of utility value for commodity crops policies = 0.75 to 0.60 (low change, medium variability)'
df_avg.loc[df_avg['exp_id'] == 27, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2025 (early change), range of utility value for commodity crops policies = 0.65 to 0.50 (high change, medium variability)'
# df_avg.loc[df_avg['exp_id'] == 28, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2025 (early change), range of utility value for commodity crops policies = 0.75 to 0.50 (high change, high variability)'
# df_avg.loc[df_avg['exp_id'] == 29, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2040 (late change), range of utility value for commodity crops policies = 0.65 to 0.60 (low change, low variability)'
# df_avg.loc[df_avg['exp_id'] == 30, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2040 (late change), range of utility value for commodity crops policies = 0.75 to 0.60 (low change, medium variability)'
# df_avg.loc[df_avg['exp_id'] == 31, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2040 (late change), range of utility value for commodity crops policies = 0.65 to 0.50 (high change, medium variability)'
# df_avg.loc[df_avg['exp_id'] == 32, 'exp_name'] = 'Experiment: Change in commodity crops policies, change timestep = 2040 (late change), range of utility value for commodity crops policies = 0.75 to 0.50 (high change, high variability)'
# df_avg.loc[df_avg['exp_id'] == 33, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.50 (very high change)'
# df_avg.loc[df_avg['exp_id'] == 34, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.55 (high change)'
# df_avg.loc[df_avg['exp_id'] == 35, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.60 (low change)'
# df_avg.loc[df_avg['exp_id'] == 36, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.65 (very low change)'
# df_avg.loc[df_avg['exp_id'] == 37, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.50 (very high change)'
# df_avg.loc[df_avg['exp_id'] == 38, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.55 (high change)'
# df_avg.loc[df_avg['exp_id'] == 39, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.60 (low change)'
# df_avg.loc[df_avg['exp_id'] == 40, 'exp_name'] = 'Experiment: Change in commodity crops profit, change timestep = 2025 (early change), max utility value of commodity crops profit = 0.65 (very low change)'
df_avg.loc[df_avg['exp_id'] == 41, 'exp_name'] = 'Experiment: All active, all experiment activation timestep = 5, yearly intervention = 4, target strategy = supportive and maybe commodity persona, max utility value of specialty crops policies = 0.70 (high change), minimum years of experience required = 10 OR minimum acerage required = 30, range of utility value for commodity crops policies = 0.75 to 0.50 (high change, high variability), max utility value of commodity crops profit = 0.55 (high change)'

# Add upper and lower bounds
df_avg['upper_bound_sac'] = df_avg['specialty-acres-change'] + df_std['specialty-acres-change']
df_avg['lower_bound_sac'] = df_avg['specialty-acres-change'] - df_std['specialty-acres-change']

df_avg['upper_bound_sa'] = df_avg['specialty-acres'] + df_std['specialty-acres']
df_avg['lower_bound_sa'] = df_avg['specialty-acres'] - df_std['specialty-acres']

# Generate distinct colors for each experiment name
unique_experiments = df_avg['exp_name'].unique()
colors = n_colors.qualitative.Bold
#colors = n_colors('rgb(0, 100, 200)', 'rgb(200, 0, 100)', len(unique_experiments), colortype='rgb')

# Plot line with band for standard deviation
fig_exp = go.Figure()

# Loop through each experiment name to create individual traces for the line and bands
for idx, exp_name in enumerate(unique_experiments):
    df_exp = df_avg[df_avg['exp_name'] == exp_name]
    
    # Get the color for the current experiment
    color = colors[idx]
    
    # Add the main line for the experiment
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]'], 
        y=df_exp['specialty-acres'], 
        mode='lines',
        name=exp_name,
        legendgroup=exp_name,
        line=dict(color=color, width=2)  # Assign a unique color to the line
    ))
    
    # Add the upper bound trace (invisible, just to define the band)
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]'], 
        y=df_exp['upper_bound_sa'], 
        mode='lines', 
        line=dict(width=0),
        showlegend=False,
        #hoverinfo='skip',  # No hover info for this trace
        legendgroup=exp_name
    ))
    
    # Add the lower bound trace with fill to create the band
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]'], 
        y=df_exp['lower_bound_sa'], 
        mode='lines', 
        fill='tonexty', 
        line=dict(width=0),
        showlegend=False,
        #hoverinfo='skip',  # No hover info for this trace
        legendgroup=exp_name,
        fillcolor=f'rgba{color[3:-1]},0.2)',  # Set same color but with opacity for the band
    ))

fig_exp.update_layout(
    title='Specialty crops acres vs timestep for different experiments',
    xaxis_title='[step]',
    yaxis_title='specialty-acres',
    hovermode='x',
    margin=dict(l=0, r=0, t=50, b=50),  # Adjust margins for better fit in Streamlit
    legend=dict(
        orientation="h",  # Horizontal legend
        # yanchor="bottom",  # Align the bottom of the legend
        # y=-0.2,  # Position the legend just below the plot
        # xanchor="center",  # Center the legend horizontally
        # x=0.5  # Center the legend relative to the plot
        # make legend text wrap around if too long
        font=dict(size=10), itemwidth=30
    )
)

# Display the figure in Streamlit
st.plotly_chart(fig_exp, use_container_width=True)


# Include a description 

'''
Experiment: Communication Amongst Farmers
Currently, commodity crop farmers and specialty crop farmers do not regularly engage in communication. However, if commodity farmers observe the production success of specialty crop farmers, they might become interested in adopting specialty crop farming practices. This experiment explores the impact of communication between commodity and specialty crop farmers on specialty crop production levels. The experiment examines whether increased interaction between these groups influences commodity farmers to transition to specialty crops, ultimately impacting production output and diversity.

Experiment: Extension Agents
Access to information about new farming technologies and practices is crucial for adoption. One primary way farmers gain such information is through extension services. This experiment assesses the impact of extension agent visits on farmer behavior, specifically regarding the adoption of specialty crops. Two key factors are measured:
Number of visits per year – how often extension agents interact with farmers.
Typology of commodity farmers – the types of farmers extension agents engage with, focusing on their openness to new practices.
The study explores whether frequent, targeted visits by extension agents can accelerate the adoption of specialty crops.

Experiment: Specialty Crops Policy Change
Current policies for specialty crops lag behind those for commodity crops in areas such as government support, incentives, insurance, supply chain infrastructure, and market access. This experiment investigates the impact of collective policy improvements on the adoption of specialty crops. Policy utility is currently set at 0.5, and the experiment measures the effects of incremental policy improvements:
Small change (0.55) – Slight Improvement in at least one factor (e.g., slight increase in incentives or market access).
Moderate change (0.6) – Improvement in two or more factors, or a major change in one (e.g., significantly higher incentives).
Substantial change (0.65) – Major improvements in two or more areas (e.g., better insurance schemes).
High change (0.7) – Significant improvements in multiple factors, such as insurance and supply chain infrastructure.
Very high change (0.75) – Comprehensive enhancements across most policy areas, including increased incentives, better insurance, and improved supply chain infrastructure.

Experiment: Wholesale Markets
One of the major challenges for specialty crop farmers is the availability of wholesale markets with benchmark prices. This experiment explores the potential possibility of direct wholesale markets or contract opportunities with large institutions as a farmer gains experience with specialty crops. The experiment measures two factors:
Years of experience – how long a farmer has been involved in specialty crops.
Size of specialty crop operation – the scale at which the farmer produces specialty crops.
This experiment aims to assess whether market access improves as farmers gain expertise and expand their operations and whether those who observe this may also adopt specialty crops.

Experiment: Commodity Crops Policy Change
Policies for commodity crops are generally more favorable, offering strong government support, incentives, insurance, and supply chain infrastructure. This experiment investigates the potential impact of a decline in these supportive policies. Since the effects may not be uniformly experienced by all farmers, some may face harsher conditions sooner than others. The current maximum policy utility is 0.85, and the experiment considers the following scenarios:
Utility between 0.65 and 0.6 – Decline in commodity crop markets and a reduction in crop subsidies, with low volatility.
Utility between 0.65 and 0.5 – Stricter criteria for subsidies and a significant reduction in support, leading to high volatility.
Utility between 0.75 and 0.6 – Increased difficulty in securing insurance for commodity crops, with high market volatility.
Utility between 0.75 and 0.5 – Stricter criteria for both insurance approval and subsidies, with very high market volatility.

Experiment: Commodity Crops Profit Reduction
Commodity crop farming is highly yield-focused, but many farmers may not fully realize the actual profit utility derived from their production. This experiment explores the factors that lead to a reduction in commodity crop profits, such as declining market prices or unfavorable market conditions. The experiment focuses on the current profit utility of commodity crops, set at 0.75, and examines scenarios where farmers might become more aware of declining profits or where market conditions erode their profit margins. The goal is to assess how these realizations might influence a shift toward specialty crops or changes in farming practices.
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
    

