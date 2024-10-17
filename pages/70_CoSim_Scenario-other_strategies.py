#%%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as n_colors
import plotly.express as px
#%%
st.set_page_config(page_title="CoSim-Base", page_icon="INFEWS_icon_whitebg.png")
st.title('CoSimulation Scenario : Base Case')

st.header('ABM Base Scenario')


# Now read from the pickle
df_avg = pd.read_pickle("ABM_exp/df_exp_avg.pkl")

#df_avg 
# Rename for each exp_id rename exp_name as follows: 
# For exp_id = 6 -> Frequent Extension agent intervetion 
df_avg.loc[df_avg['exp_id'] == 1, 'exp_name'] = 'Default Conditions'
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

# Just for this plot, drop the rows where exp_id is not 1 or 41
#df_avg = df_avg[df_avg['exp_id'].isin([1, 41])]

# Loop through each experiment name to create individual traces for the line and bands
for idx, exp_name in enumerate(unique_experiments):
# Set the index for the experiment name
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
        line=dict(color=color, width=2)  # Assign a unique color to the line
    ))

    # Add the upper bound trace (invisible, just to define the band)
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]']+2020, 
        y=df_exp['upper_bound_sa'], 
        mode='lines', 
        line=dict(width=0),
        showlegend=False,
        #hoverinfo='skip',  # No hover info for this trace
        legendgroup=exp_name
    ))

    # Add the lower bound trace with fill to create the band
    fig_exp.add_trace(go.Scatter(
        x=df_exp['[step]']+2020, 
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
    xaxis_title='Year',
    yaxis_title='Specialty crops (Acres)',
    hovermode='x',
    margin=dict(l=0, r=0, t=50, b=50),  # Adjust margins for better fit in Streamlit   
)

# Display the figure in Streamlit
st.plotly_chart(fig_exp) 


## _________________________________________________SWAT ________________________________________________________________________
#%%
st.header('SWAT maps farmer activity to available HRUs ') 

# Base file directory
base_dir='SWAT_base/'

# Load the historical and future data
df_2020_rch = pd.read_csv(base_dir+'TxtInOutABM_Co_sim_base_rch_output.csv')
df_ABM_rch = pd.read_csv(base_dir+'TxtInOutABM_Co_sim_experiment_50_percent_reach_rch_output.csv')
df_2020_rch.set_index('Unnamed: 0', inplace=True)
df_ABM_rch.set_index('Unnamed: 0', inplace=True)

# Load extension agent data 
df_ext_rch= pd.read_csv(base_dir+'TxtInOutABM_Co_sim_experiment_extension_4_sm_rch_output.csv')
df_ext_rch.set_index('Unnamed: 0', inplace=True)

# Load specialty policy data
df_specialty_rch= pd.read_csv(base_dir+'TxtInOutABM_Co_sim_experiment_specialty_pc_5_75_rch_output.csv')
df_specialty_rch.set_index('Unnamed: 0', inplace=True)

# Load commodity policy data
df_commodity_rch= pd.read_csv(base_dir+'TxtInOutABM_Co_sim_experiment_commodity_pc_5_65_50_rch_output.csv')
df_commodity_rch.set_index('Unnamed: 0', inplace=True)

# Load 

# Select all data for FLOW_OUTcms, SED_OUTtons and No3_OUTkg for df 2020 and 2050 for RCH column value of 1
#df_2020_rch = df_2020_rch.loc[['FLOW_OUTcms', 'SED_OUTtons', 'No3_OUTkg'], df_2020_rch.columns.str.contains('1')]

#df_2020_rch = df_2020_rch.loc[ '362'  ]
# df_ABM_rch = df_ABM_rch.loc[:, df_ABM_rch.columns.str.contains('1')]

filtered_df_2020_rch = df_2020_rch[df_2020_rch['RCH'] == 362]
filtered_df_2020_rch = filtered_df_2020_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_2020_rch = filtered_df_2020_rch[filtered_df_2020_rch['MON'] >= 1000]

rch_data_Current = filtered_df_2020_rch  

filtered_df_ABM_rch = df_ABM_rch[df_ABM_rch['RCH'] == 362]
filtered_df_ABM_rch = filtered_df_ABM_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_ABM_rch = filtered_df_ABM_rch[filtered_df_ABM_rch['MON'] >= 1000]

rch_data_Future = filtered_df_ABM_rch

filtered_df_ext_rch = df_ext_rch[df_ext_rch['RCH'] == 362]
filtered_df_ext_rch = filtered_df_ext_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_ext_rch = filtered_df_ext_rch[filtered_df_ext_rch['MON'] >= 1000]

rch_data_Ext = filtered_df_ext_rch

filtered_df_specialty_rch = df_specialty_rch[df_specialty_rch['RCH'] == 362]
filtered_df_specialty_rch = filtered_df_specialty_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_specialty_rch = filtered_df_specialty_rch[filtered_df_specialty_rch['MON'] >= 1000]

rch_data_Specialty = filtered_df_specialty_rch

filtered_df_commodity_rch = df_commodity_rch[df_commodity_rch['RCH'] == 362]
filtered_df_commodity_rch = filtered_df_commodity_rch[['RCH', 'MON','FLOW_OUTcms', 'SED_OUTtons', 'NO3_OUTkg']]
filtered_df_commodity_rch = filtered_df_commodity_rch[filtered_df_commodity_rch['MON'] >= 1000]

rch_data_Commodity = filtered_df_commodity_rch

# combine data
rch_data_Current['Dataset'] = 'Current Scenario'
rch_data_Future['Dataset'] = 'All Strategies: 50% Reach Scenario'
rch_data_Ext['Dataset'] = 'Extension Agent Scenario'
rch_data_Specialty['Dataset'] = 'Specialty Policy Scenario'
rch_data_Commodity['Dataset'] = 'Commodity Policy Scenario'
combined_data_rch = pd.concat([rch_data_Current, rch_data_Ext, rch_data_Specialty , rch_data_Commodity, rch_data_Future])

# Plot boxplot for FLOW_OUTcms 
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='FLOW_OUTcms', color='Dataset', title='Boxplot for Streamflow (cubic meters)')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Stream Flow (cubic meters)")
# Update layout to remove legend
# fig_swat_box_rch.update_layout(showlegend=False)
# Plot 
st.plotly_chart(fig_swat_box_rch)

# Plot boxplot for SED_OUTtons
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='SED_OUTtons', title='Boxplot for Sediment Load (metric tons)',color='Dataset')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Sediment Load (metric tons)")
# Update layout to remove legend
# fig_swat_box_rch.update_layout(showlegend=False)

# Plot
st.plotly_chart(fig_swat_box_rch)

# Plot boxplot for No3_OUTkg
fig_swat_box_rch = px.box(combined_data_rch, x='Dataset', y='NO3_OUTkg', title='Boxplot for Nitrate (kilograms)', color='Dataset')
# Update x-axis label
fig_swat_box_rch.update_xaxes(title_text="Scenario")
# Update y-axis label
fig_swat_box_rch.update_yaxes(title_text="Nitrate (kilograms)")
# Update layout to remove legend
# fig_swat_box_rch.update_layout(showlegend=False)
# Plot
st.plotly_chart(fig_swat_box_rch)


    
## _________________________________________________LCA ________________________________________________________________________


st.header(' Life Cycle Analysis of Food Systems ')  

st.subheader('Base vs Extension Agent scenario:')

chart_data_base = pd.read_pickle(r'lca_abm_Co_sim_base.pickle')

chart_data_extension = pd.read_pickle(r'lca_abm_Co_sim_experiment_extension_4_sm.pickle')

chart_data_specialty = pd.read_pickle(r'lca_abm_Co_sim_experiment_specialty_pc_5_75.pickle')

chart_data_commodity = pd.read_pickle(r'lca_abm_Co_sim_experiment_commodity_pc_5_65_50.pickle')

chart_data_50_rch = pd.read_pickle(r'lca_abm_Co_sim_experiment_50_percent_reach.pickle')

 
# chart_data_base 

# chart_data_50_rch

# Drop columns and rows not needed for plotting 
baseplot= chart_data_base.drop(chart_data_base.columns[[0,2,3,5]],axis=1)
#baseplot= baseplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
# Drop 2050 for base condition for the following reason: 

# Drop columns and rows not needed for plotting 
localplot= chart_data_50_rch.drop(chart_data_50_rch.columns[[0,2,3,5]],axis=1)
#localplot= localplot.query("`Model_Year_`==2020 | `Model_Year_`==2050")
#localplot 
# Load the Raw data from LCA 

extensionplot= chart_data_extension.drop(chart_data_extension.columns[[0,2,3,5]],axis=1)
specialtyplot= chart_data_specialty.drop(chart_data_specialty.columns[[0,2,3,5]],axis=1)
commodityplot= chart_data_commodity.drop(chart_data_commodity.columns[[0,2,3,5]],axis=1)

chart_data_raw = pd.read_csv(r'lca_dataset.csv')
#chart_data_raw


st.subheader('Energy use in 2020 and 2050 for Food Scenarios')

fig_lca_eu = go.Figure() 
fig_lca_eu.add_trace(go.Scatter(x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], name='Base Scenario',
                                #line=dict(color='deepskyblue', width=4, dash='solid')
                                ))
fig_lca_eu.add_trace(go.Scatter(x=extensionplot['Model_Year_'], y=extensionplot['Energy_Use_MJ'], name='Extension Agent Scenario')) 
fig_lca_eu.add_trace(go.Scatter(x=specialtyplot['Model_Year_'], y=specialtyplot['Energy_Use_MJ'], name='Specialty Policy Scenario'))
fig_lca_eu.add_trace(go.Scatter(x=commodityplot['Model_Year_'], y=commodityplot['Energy_Use_MJ'], name='Commodity Policy Scenario'))

fig_lca_eu.add_trace(go.Scatter(x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'], name='Extension Agent Scenario', 
                                #line=dict(color='deepskyblue', width=4, dash='dash')
                                ))


# fig_lca_eu = go.Figure(data=[
    
#     go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Energy_Use_MJ'], marker_color='blue'),
#     #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['energy']),#,marker_color='green'),
#     go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Energy_Use_MJ'],marker_color='red')
#     #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['energy']),#,marker_color='DarkSlateGrey')
#     ],
#     layout={
#         'xaxis': {'title': 'Year'},
#         'yaxis': {'title': 'Energy Use (MJ)'}
#     }
# )
# #Change the bar mode
# fig_lca_eu.update_layout(barmode='group')

st.plotly_chart(fig_lca_eu)

st.subheader('Global Warming Potential in 2020 and 2050 for Food Scenarios')


# fig_lca_gw = go.Figure(data=[
    
#     go.Bar(name='Current', x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq'], marker_color='blue'),# ,marker_color='crimson'),
#     #go.Bar(name='Baseline, isolation', x=rbaseplot['year'], y=rbaseplot['gwp']),#,marker_color='green'),
#     go.Bar(name='Future', x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq'],marker_color='red'),#,marker_color='blue'),
#     #go.Bar(name='Local, isolation', x=rlocalplot['year'], y=rlocalplot['gwp']),#,marker_color='DarkSlateGrey')  
#     ],
#     layout={
#         'xaxis': {'title': 'Year'},
#         'yaxis': {'title': 'Global Warming Potential (kg co2 eq)'}
#     }
# )
# # Change the bar mode
# fig_lca_gw.update_layout(barmode='group')

fig_lca_gw = go.Figure()
fig_lca_gw.add_trace(go.Scatter(x=baseplot['Model_Year_'], y=baseplot['Global_Warming_Potential_kg_co2_eq'], name='Base Scenario',
                                #line=dict(color='orangered', width=4, dash='solid')
                                ))
fig_lca_gw.add_trace(go.Scatter(x=extensionplot['Model_Year_'], y=extensionplot['Global_Warming_Potential_kg_co2_eq'], name='Extension Agent Scenario'))
fig_lca_gw.add_trace(go.Scatter(x=specialtyplot['Model_Year_'], y=specialtyplot['Global_Warming_Potential_kg_co2_eq'], name='Specialty Policy Scenario'))
fig_lca_gw.add_trace(go.Scatter(x=commodityplot['Model_Year_'], y=commodityplot['Global_Warming_Potential_kg_co2_eq'], name='Commodity Policy Scenario'))

fig_lca_gw.add_trace(go.Scatter(x=localplot['Model_Year_'], y=localplot['Global_Warming_Potential_kg_co2_eq'], name='Extension Agent Scenario',
                                #line=dict(color='orangered', width=4, dash='dash')
                                ))

st.plotly_chart(fig_lca_gw)


if st.checkbox('Show base dataset'):
    chart_data_base

if st.checkbox('Show local dataset'):
    chart_data   
