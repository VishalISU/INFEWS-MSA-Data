#%%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as n_colors
import plotly.express as px
import os
#%%
st.set_page_config(page_title="CoSim-Comparison", page_icon="INFEWS_icon_whitebg.png")
st.title('CoSimulation Scenario Comparasion')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

st.header('Agent-based model (ABM)')


# Now read from the pickle
# df_avg = pd.read_pickle("ABM_exp/df_exp_avg.pkl")
ABM_DIR = os.path.join(BASE_DIR, "ABM_exp")
df_avg = pd.read_pickle(os.path.join(ABM_DIR, "df_exp_avg.pkl"))

#df_avg 
# Rename for each exp_id rename exp_name as follows: 
# For exp_id = 6 -> Frequent Extension agent intervetion 
df_avg.loc[df_avg['exp_id'] == 1, 'exp_name'] = 'Current Scenario'
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
        legendgroup=exp_name
       # line=dict(color=color, width=2)  # Assign a unique color to the line
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


## _________________________________________________SWAT ________________________________________________________________________
#%%
st.header('SWAT maps farmer activity to available HRUs ') 

# ---------------------------------------------------------
# SWAT postprocessed outputs (from your new postproc script)
# ---------------------------------------------------------
# SWAT_OUT_DIR = r"\SWAT_Cosim_results"  # <- change if needed
SWAT_OUT_DIR = os.path.join(BASE_DIR, "SWAT_Cosim_results")

SCENARIOS = {
    "Current Scenario": "Co_sim_base",
    "Extension Agent Scenario": "Co_sim_experiment_extension_4_sm",
    "Specialty Policy Scenario": "Co_sim_experiment_specialty_pc_5_75",
    "Commodity Policy Scenario": "Co_sim_experiment_commodity_pc_5_65_50",
    "All Strategies: 50% Reach Scenario": "Co_sim_experiment_50_percent_reach",
}

def load_rch_scenario(output_dir: str, scenario_suffix: str) -> pd.DataFrame:
    """
    Loads the scenario RCH time series produced by your postproc script:
      output_<scenario>.csv
    """
    path = os.path.join(output_dir, f"output_{scenario_suffix}.csv")
    df = pd.read_csv(path)

    # Standardize names
    df = df.rename(columns={"MON": "Year"})
    return df


def load_marketable_2020_2050(output_dir: str, scenario_suffix: str) -> pd.DataFrame:
    """
    Loads the scenario marketable yields produced by your postproc script:
      mktbl_2020_2050_<scenario>.pickle
    """
    path = os.path.join(output_dir, f"mktbl_2020_2050_{scenario_suffix}.pickle")
    return pd.read_pickle(path)

def plot_rch_multiscenario(
    output_dir: str,
    rch_id: int,
    variable: str,
    title: str,
    y_label: str,
    year_min: int = 2020,
    year_max: int = 2050,
):
    fig = go.Figure()

    for display_name, suffix in SCENARIOS.items():
        df = load_rch_scenario(output_dir, suffix)

        # filter to one reach and year range (match your postproc conventions)
        df = df[df["RCH"] == rch_id]
        df = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

        fig.add_trace(go.Scatter(
            x=df["Year"],
            y=df[variable],
            mode="lines",
            name=display_name
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_label,
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=50),
    )

    st.plotly_chart(fig)


# ---------------------------------------------------------
# SWAT line plots (replace the old boxplots)
# ---------------------------------------------------------
RCH_TO_PLOT = 360  # or 362 if that is your intended reach; keep consistent with postproc

st.subheader("SWAT yearly water quality time series (5 scenarios)")

plot_rch_multiscenario(
    SWAT_OUT_DIR, RCH_TO_PLOT,
    variable="FLOW_OUTcms",
    title="Yearly Streamflow across Co-Simulation Scenarios",
    y_label="Streamflow (m³/s)"
)

plot_rch_multiscenario(
    SWAT_OUT_DIR, RCH_TO_PLOT,
    variable="SED_OUTtons",
    title="Yearly Sediment Load across Co-Simulation Scenarios",
    y_label="Sediment Load (tons)"
)

plot_rch_multiscenario(
    SWAT_OUT_DIR, RCH_TO_PLOT,
    variable="NO3_OUTkg",
    title="Yearly Nitrate Load across Co-Simulation Scenarios",
    y_label="Nitrate Load (kg)"
)

# Extra plot requested: phosphorus
plot_rch_multiscenario(
    SWAT_OUT_DIR, RCH_TO_PLOT,
    variable="TOT Pkg",
    title="Yearly Total Phosphorus Load across Co-Simulation Scenarios",
    y_label="Total Phosphorus (kg)"
)

#4a
st.subheader("Marketable crop yields (2020–2050) across scenarios")

# Crop codes dictionary (copy from 45; you can trim if desired)
crop_codes = {
    "ALFA": "Alfalfa", "APPL": "Apple", "BLUE": "Blueberry", "BROC": "Broccoli",
    "CABG": "Cabbage", "CHER": "Cherry", "COLG": "Collard greens", "CORN": "Corn",
    "CRRT": "Carrot", "CUCM": "Cucumber", "DRYB": "Dry beans", "KALE": "Kale",
    "GRAP": "Grape", "HMEL": "Honeydew melon", "LETT": "Lettuce", "ONIO": "Onion",
    "PEAR": "Pear", "POTA": "Potato", "PUMP": "Pumpkin", "RASP": "Raspberry",
    "SCRN": "Sweet corn", "SNPB": "Snap beans", "SOYB": "Soybean", "SPIN": "Spinach",
    "SPOT": "Sweet potato", "SQUA": "Squash", "STRW": "Strawberry", "TOMA": "Tomato",
    "WWHT": "Winter Wheat", "FESC": "Tall Fescue"
}

# Optional: remove unwanted crops like 45 does
unwanted_rowcrops = ["ALFA", "FESC", "SWRN", "HAY"]
crop_codes = {k: v for k, v in crop_codes.items() if k not in unwanted_rowcrops}

crop_list = sorted(crop_codes.items(), key=lambda item: item[1])
selected_crop = st.selectbox("Select a Crop", options=crop_list, format_func=lambda x: x[1])
selected_crop_code = selected_crop[0]
selected_crop_name = selected_crop[1]

#4b
def plot_marketable_crop_multiscenario(output_dir: str, crop_code: str, crop_name: str):
    fig = go.Figure()

    for display_name, suffix in SCENARIOS.items():
        df = load_marketable_2020_2050(output_dir, suffix)

        if crop_code not in df.index:
            # Skip scenarios where crop is absent
            continue

        series = df.loc[crop_code]
        crop_df = series.reset_index()
        crop_df.columns = ["Year", "Yield"]

        fig.add_trace(go.Scatter(
            x=crop_df["Year"],
            y=crop_df["Yield"],
            mode="lines",
            name=display_name
        ))

    fig.update_layout(
        title=f"Marketable Yield over Time: {crop_name} (2020–2050)",
        xaxis_title="Year",
        yaxis_title="Yield",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=50),
    )

    st.plotly_chart(fig)


plot_marketable_crop_multiscenario(SWAT_OUT_DIR, selected_crop_code, selected_crop_name)


    
## _________________________________________________LCA ________________________________________________________________________


st.header(' Life Cycle Analysis of Food Systems ')  

# ---------------------------------------------------------
# LCA postprocessed outputs (scenario-based folders)
# ---------------------------------------------------------
LCA_BASE_DIR = BASE_DIR

LCA_SCENARIOS = {
    "Base Scenario": "Co_sim_base",
    "Extension Agent Scenario": "Co_sim_experiment_extension_4_sm",
    "Specialty Policy Scenario": "Co_sim_experiment_specialty_pc_5_75",
    "Commodity Policy Scenario": "Co_sim_experiment_commodity_pc_5_65_50",
    "50% Reach Scenario": "Co_sim_experiment_50_percent_reach",
}

#3 Load LCA data for each scenario


def load_lca_scenario(base_dir: str, scenario_suffix: str) -> pd.DataFrame:
    """
    Loads LCA results for a given scenario from:
      Outputs_<scenario>/lca_<scenario>.csv
    """
    folder = os.path.join(base_dir, f"Outputs_{scenario_suffix}")
    path = os.path.join(folder, f"lca_{scenario_suffix}.csv")

    df = pd.read_csv(path)

    # ---- Normalize column names ----
    df.columns = (
        df.columns
          .str.strip()
          .str.replace(" ", "_")
          .str.replace("(", "", regex=False)
          .str.replace(")", "", regex=False)
          .str.replace("/", "_")
    )

    # Keep only columns needed for plotting
    # Keep only columns needed for plotting
    required_cols = [
        "Model_Year",
        "Energy_Use_MJ",
        "Global_Warming_Potential_kg_co2_eq",
    ]

    df = df[[c for c in required_cols if c in df.columns]]

    return df


#4 Reuasable LCA multiscenario plot function

def plot_lca_multiscenario(
    base_dir: str,
    y_col: str,
    title: str,
    y_label: str,
    key: str,
):
    fig = go.Figure()

    for display_name, suffix in LCA_SCENARIOS.items():
        df = load_lca_scenario(base_dir, suffix)

        fig.add_trace(go.Scatter(
            x=df["Model_Year"],
            y=df[y_col],
            mode="lines+markers",
            name=display_name
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_label,
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=50),
    )

    st.plotly_chart(fig, key=key)


st.subheader("Energy Use across Food System Scenarios")

plot_lca_multiscenario(
    base_dir=LCA_BASE_DIR,
    y_col="Energy_Use_MJ",
    title="Energy Use over Time across Co-Simulation Scenarios",
    y_label="Energy Use (MJ)",
    key="lca_energy"
)


st.subheader("Global Warming Potential across Food System Scenarios")

plot_lca_multiscenario(
    base_dir=LCA_BASE_DIR,
    y_col="Global_Warming_Potential_kg_co2_eq",
    title="Global Warming Potential over Time across Co-Simulation Scenarios",
    y_label="Global Warming Potential (kg CO₂-eq)",
    key="lca_gwp"
)


