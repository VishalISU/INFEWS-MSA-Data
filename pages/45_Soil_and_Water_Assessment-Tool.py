#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go 
import os 
import time

filepath = 'C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\output.rch'
#%%
def rch2csv(filepath):
    #%%
    # Extract the subdirectory name and file name for output
    subdirectory = os.path.dirname(filepath)
    opfile = os.path.basename(filepath)

    # Read the headers into a DataFrame
    
    df_rch = pd.read_csv(filepath, delimiter=r'\s+', header=None, skiprows=9)

    #df_rch = pd.read_fwf(path2hru, header=None, index_col=None, skiprows=9)
    #%%
    # Rename the headers

    df_rch.columns = [
    'REACH', 'RCH', 'GIS', 'MON', 'AREAkm2', 'FLOW_INcms', 'FLOW_OUTcms', 'EVAPcms', 'TLOSScms',
    'SED_INtons', 'SED_OUTtons', 'SEDCONCmg/L', 'ORGN_INkg', 'ORGN_OUTkg', 'ORGP_INkg', 'ORGP_OUTkg',
    'NO3_INkg', 'NO3_OUTkg', 'NH4_INkg', 'NH4_OUTkg', 'NO2_INkg', 'NO2_OUTkg', 'MINP_INkg', 'MINP_OUTkg',
    'CHLA_INkg', 'CHLA_OUTkg', 'CBOD_INkg', 'CBOD_OUTkg', 'DISOX_INkg', 'DISOX_OUTkg',
    'SOLPST_INmg', 'SOLPST_OUTmg', 'SORPST_INmg', 'SORPST_OUTmg', 'REACTPSTmg', 'VOLPSTmg',
    'SETTLPSTmg', 'RESUSP_PSTmg', 'DIFFUSEPSTmg', 'REACBEDPSTmg', 'BURYPSTmg', 'BED_PSTmg',
    'BACTP_OUTct', 'BACTLP_OUTct', 'CMETAL#1kg', 'CMETAL#2kg', 'CMETAL#3kg', 'TOT Nkg', 'TOT Pkg',
    'NO3ConcMg/l', 'WTMPdegc', 'Salt1', 'Salt2', 'Salt3', 'Salt4', 'Salt5', 'Salt6', 'Salt7', 'Salt8',
    'Salt9', 'Salt10', 'SAR', 'EC'
]
    # Drop the "REACH" column
    df_rch = df_rch.drop(columns=['REACH'])
    #%%
    # Filter RCH column only for values ==360 
    df_rch = df_rch[df_rch['RCH'] == 360]
    # Filter MON value for values =2020 and <=2050
    df_rch = df_rch[(df_rch['MON'] >= 2020) & (df_rch['MON'] <= 2050)]
    #%%
    # Write the DataFrame to a CSV file
    output_file = os.path.join(os.getcwd(), f"{os.path.basename(subdirectory)}_rch_{opfile.replace('.rch', '.csv')}")
    df_rch.to_csv(output_file)
    # Print the output file path
    print(f"File written to: {output_file}")
    
    # Write the DataFrame to a pickle file
    df_rch.to_pickle(output_file.replace('.csv', '.pickle'))
    print(f"Pickle file written to: {output_file.replace('.csv', '.pickle')}")

    
    #%%

def mgt2pkl(subdirectory,opfile): 
    #%%
    path2op= 'C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\output.mgt'
    #os.getcwd()+'\\'+subdirectory+'\\'+opfile
    #Function converts output.mgt to a csv and pd dataframe and finally pickles the df. 
    df = pd.read_csv(path2op,header=[0],index_col=None,skiprows=[1,2,3],delim_whitespace=True)
    # Rename problematic column headers
    df=df.rename(columns={
                        "Sub":"SUB",
                        "Hru":"HRU",
                        "Year":"YEARIDX",
                        "Mon":"MONIDX",
                        "Day":"DAYIDX",
                        "AREAkm2":"AREA",
                        "crop/fert/pest":"CROP", 
                        "Operation":"OPERATION",
                        "phubase":"PHUBASE",
                        "phuacc":"PHUACC",
                        "sol_sw":"SOL_SW",
                        "bio_ms":"BIO_MASS",
                        "sol_rsd":"SOL_SUMNO3",
                        "sol":"SOL_SUMSOLP",
                        "sol.1":"SOL",
                        "yield":"YIELD" })
    # Drop uneccesary columns 

    df=df.drop(columns={
                    "strsw","strsa","strsp","strstmp","irrsc", "grain",
                    "biomass","tuber","irr", "amt","amt.1","mix","eff","strsn",
                    "irrno","residue","nit","phos"})

    # Insert new column TSTAMP
    TS=[time.time()]*(df.shape[0]) #retrieve current timestamp ts=time.time()
    df.insert(0,"TSTAMP",TS)
    # replace the character / with _ 
    df=df.replace(regex=['/'],value='_')
    # replace the character - with _ 
    df=df.replace(regex=['-'],value='_')
    # Remove any nan values that may create problems while pickling 
    da=df.fillna(0)
 
    # PostProcessing for LCA
    # Select only the six columns of interest
    db=da.filter(['SUB','HRU','YEARIDX','CROP','OPERATION','BIO_MASS','YIELD'])
    #select rows where 'OPERATION' column is equal to HARVEST or HARV_KILL or END_DORM
    #db=db.loc[db['OPERATION'] == 'HARVEST' or 'HARV_KILL' ]
    db=db.query('OPERATION == "HARVEST" | OPERATION == "HARV_KILL" | OPERATION == "END_DORM"')
   
    # Remove the first two years of simulation
    # Generally these two years are run as the warmup years and need to be excluded
    first2=db['YEARIDX'].unique()
    querystring="YEARIDX!="+str(first2[0])+"& YEARIDX!="+str(first2[1])
    db=db.query(querystring)
    # Soon, we will want to loop over these values
    # First find the list of years & list of crops
    listofyears = db['YEARIDX'].unique() 
    crop_list=db['CROP'].unique()
    blacklist=['ALFA','FESC','SWRN','HAY']

    # _______
    # --------------------------------------------------------------
    # Create df_final25 for years 2020–2029 and HARVEST ONLY / HARV_KILL
    # --------------------------------------------------------------

    # Filter years 2020–2029
    df_20s = db.query("2020 <= YEARIDX <= 2029")

    # Keep only HARVEST and HARV_KILL
    # df_20s = df_20s.query('OPERATION == "HARVEST" | OPERATION == "HARV_KILL"')

    # Build list of years and crops
    years_20s = df_20s['YEARIDX'].unique()
    crops_20s = df_20s['CROP'].unique()

    # Initialize output DF
    df_final25 = pd.DataFrame(columns=years_20s, index=crops_20s)

    # Loop over crops and years to compute mean yield/biomass
    blacklist = ['ALFA', 'FESC', 'SWRN', 'HAY']   # biomass crops

    for yr in years_20s:
        df_year = df_20s[df_20s['YEARIDX'] == yr]
        for crop in crops_20s:
            df_crop = df_year[df_year['CROP'] == crop]

            # Averaging rule:
            if crop in blacklist:
                # average only values where operation is "HARVEST ONLY"
                mean_val = df_crop[df_crop['OPERATION'] == "HARVEST ONLY"]["BIO_MASS"].mean()
            else:
                # average only values where operation is "HARVEST ONLY" or "HARV_KILL"
                mean_val = df_crop[df_crop['OPERATION'].isin(["HARVEST ONLY", "HARV_KILL"])]["YIELD"].mean()
            df_final25.at[crop, yr] = mean_val

    # Add average column
    df_final25["AVG"] = df_final25.mean(axis=1)

    # Sort alphabetically
    df_final25 = df_final25.sort_index()

    # _______
    
    # Initialize an empty DataFrame
    dc = pd.DataFrame(columns=listofyears,index=crop_list)

    for i in listofyears:
        qsi="YEARIDX=="+str(i)
        
        for j in crop_list:
            
            dd=db.query(qsi)
            qsj="CROP=="+"'"+j+"'"
            dd=dd.query(qsj)
            
            if j not in blacklist:
                mean=dd.YIELD.mean() 
            elif j in blacklist: 
                mean=dd.BIO_MASS.mean()
            # Write value of mean into approriate dataframe slot
            dc.at[j,i]= mean
    
    # Calculate Annual averages , arrange alphabetically
    dc["AVG"]= dc.mean(axis=1)
    dc=dc.sort_index()

    # Singular dataframe that has the averages only ; sort index alphabetically
    df=pd.DataFrame(dc["AVG"])
    df=df.sort_index()

    # Create a DataFrame with the given values for cropfactor
    data = {'CROP': ['ALFA', 'APPL', 'BLUE', 'BROC', 'CABG', 'CHER', 'COLG', 'CORN', 'CRRT', 'CUCM', 'DRYB', 'KALE',
                    'GRAP', 'HMEL', 'LETT', 'ONIO', 'PEAR', 'POTA', 'PUMP', 'RASP', 'SCRN', 'SOYB', 'SPIN', 'SPOT',
                    'SQUA', 'STRW', 'TOMA', 'FESC', 'SWRN', 'HAY', 'SNPB'],
            'FACTOR': [100, 65.34092534, 80.5226841, 96.38848756, 100, 74.00973032, 90.64078947, 67.49677654, 69.29841359,
                  65.34405788, 67.49677654, 90.64078947, 85.23348499, 65, 90.64078947, 69.29841359, 63.15054302,
                  95.27535719, 65, 63.28947368, 67.49677654, 67.49677654, 90.64078947, 95.27535719, 65, 27.36505263,
                  39.00461038, 100, 100, 100, 67.49677654]}
    
    # To the above we are going to add assumed crop factors for CANA 70, SGBT - 70,  WWHT change to -> 97
    
    # Add the new data to the DataFrame
    data['CROP'].extend(['CANA','SGBT','WWHT'])
    data['FACTOR'].extend([70,70,100])

    # Create a DataFrame from the data

    cropfactor = pd.DataFrame(data)
    # Reset index to crop column
    cropfactor.set_index('CROP',inplace=True)
    # Normalize percentages 
    cropfactor.FACTOR = cropfactor.FACTOR/100
    
    marketable = df.mul(cropfactor['FACTOR'], axis=0)

    marketable_20to30 = df_final25.mul(cropfactor['FACTOR'], axis=0)
    marketable_20to50 = dc.mul(cropfactor['FACTOR'], axis=0)
    #%%
    # Save marketable as a pickle file
    # marketable.to_pickle(subdirectory+'_'+opfile.replace('output.mgt','mktbl.pickle'));
    # marketable.to_csv(subdirectory+'_'+opfile.replace('output.mgt','mktbl.csv'));
    marketable.to_pickle('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl.pickle'));
    marketable.to_csv('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl.csv'));
    # Save marketable_20to30 as a pickle file
    # marketable_20to30.to_pickle(subdirectory+'_'+opfile.replace('output.mgt','mktbl_2020_2029.pickle'));
    # marketable_20to30.to_csv(subdirectory+'_'+opfile.replace('output.mgt','mktbl_2020_2029.csv'));
    marketable_20to30.to_pickle('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl_2020_2029.pickle'));
    marketable_20to30.to_csv('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl_2020_2029.csv'));
    # Save marketable_20to50 as a pickle file
    marketable_20to50.to_pickle('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl_2020_2050.pickle'));
    marketable_20to50.to_csv('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\'+opfile.replace('output.mgt','mktbl_2020_2050.csv'));

    # WRITE DATAFRAME TO A PICKLE FILE and .csv
    # Now convert to a pickle file to be saved in SWAT_base_2025
    # Write the dataframe to a pickle file
    #%%
    # dc.to_pickle('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\output.pickle')
    # # Write to a csv file
    # dc.to_csv('C:\\Users\\azureuser\\INFEWS-MSA-Data\\SWAT_base_2025\\output.csv')
    # print ("Pickle and CSV files written to SWAT_base_2025 directory  
    #%%
    # buffer

#%%
#Force Streamlit to work in wide mode 
#%%s
st.set_page_config(
    page_title="SWAT",
    page_icon="SWATlogo.png",
)


st.image('SWATlogo.png', width=100)

st.write('# SWAT - Soil and Water Assessment Tool') 

'''The Soil and Water Assessment Tool (SWAT) can be used to model movement of water and associated nutrients and sediments, and to quantify crop growth based on  land management practices. '''
'''The SWAT model requires inputs for climate, topography, soil type, land cover, and crop management systems to generate outputs including streamflow rates  and nitrate, phosphorus, and sediment loads to characterize conditions for watersheds in specific areas.'''
'''To allow examination of upstream and within-metro effects on water quality, our SWAT models include the North and South Raccoon Rivers, the North and South Skunk, the Middle Des Moines River, and the Lake Red Rock watersheds (Figure 1). Together, these watersheds are part of a large system that drains to and through the Des Moines area. Historical data for river and stream parameters are used to calibrate initial models that are then  used to assess 'what if?' scenarios for the future.'''

st.image('DMRBforWebsite.png', caption='Figure 1. Watershed boundaries for river systems in the area (dark line), county boundaries for the Des Moines metropolitan area (brown line) and location of the City of Des Moines (gray shaded area).')

'''Here we compare SWAT outputs for current and future scenarios of local food production within the Des Moines Metropolitan Statistical Area (MSA).'''



cola, colb = st.columns(2)
with cola:  
    st.subheader('Current Scenario')
    '''Current amount of local food production (about 5% local) in Des Moines metropolitan area for land use and crop yield in 2020'''
with colb:
    st.subheader('Future Scenario')
    '''Increased local food production (50% local) in Des Moines metro  area for land use and yield in 2050.'''

# base file 
base_dir='SWAT_base_2025/'

# Invoke mgt2pkl function for SWAT_base_2025
# mgt2pkl('SWAT_base_2025','output.mgt')
# Invoke rch2csv function for SWAT_base_2025
# rch2csv('SWAT_base_2025\\output.rch')

# LINE PLOT OF FLOW_OUTcms, SED_OUTtons, and NO3_OUTkg on separate plots
df_20to50_rch = pd.read_csv(base_dir+'SWAT_base_2025_rch_output.csv')

# Plot line plot of FLOW_OUTcms vs MON, renaming MON for Year
df_20to50_rch.rename(columns={'MON': 'Year'}, inplace=True)
fig_flow = px.line(df_20to50_rch, x='Year', y='FLOW_OUTcms', title='Current and future yearly streamflow')
# Update x-axis label
fig_flow.update_xaxes(title_text="Year")
# Update y-axis label to say m^3/s
fig_flow.update_yaxes(title_text="Stream Flow (m^3/s)")
# Plot linear trendline
# fig_flow.add_traces(px.line(df_20to50_rch, x='Year', y='FLOW_OUTcms', trendline="ols").data)

# --- Compute trendline using px.scatter ---
trend_fig = px.scatter(df_20to50_rch, x='Year', y='FLOW_OUTcms', trendline="ols")

# Extract only the trendline trace (usually trace index 1)
trendline_trace = [
    t for t in trend_fig.data
    if t.mode == 'lines'   # this filters out the raw data points
]

# Add trendline to original figure
for t in trendline_trace:
    t.update(line=dict(dash='dot', width=1))
    fig_flow.add_trace(t)
# Use plotly go muted blue color for FLOW plot
fig_flow.update_traces(line=dict(color='royalblue'))
# Plot
st.plotly_chart(fig_flow)

# Plot line plot of SED_OUTtons vs MON, renaming MON for Year
fig_sed = px.line(df_20to50_rch, x='Year', y='SED_OUTtons', title='Current and future yearly sediment load')
# Update x-axis label
fig_sed.update_xaxes(title_text="Year")
# Update y-axis label
fig_sed.update_yaxes(title_text="Sediment Load (metric tons)")

# Add trendline to SED plot
trend_fig_sed = px.scatter(df_20to50_rch, x='Year', y='SED_OUTtons', trendline="ols")
# Extract only the trendline trace (usually trace index 1)  
trendline_trace_sed = [
    t for t in trend_fig_sed.data
    if t.mode == 'lines'   # this filters out the raw data points
]
# Add trendline to original figure
for t in trendline_trace_sed:
    t.update(line=dict(dash='dot', width=1))
    fig_sed.add_trace(t)

# use plotly go cooked asparagus green for SED plot
fig_sed.update_traces(line=dict(color='darkgreen'))

# Plot
st.plotly_chart(fig_sed)


# Plot line plot of NO3_OUTkg vs MON, renaming MON for Year
fig_no3 = px.line(df_20to50_rch, x='Year', y='NO3_OUTkg', title='Current and future yearly nitrate load')
# Update x-axis label
fig_no3.update_xaxes(title_text="Year") 
# Update y-axis label
fig_no3.update_yaxes(title_text="Nitrate Load (kg)")

# Add trendline to NO3 plot
trend_fig_no3 = px.scatter(df_20to50_rch, x='Year', y='NO3_OUTkg', trendline="ols")
# Extract only the trendline trace (usually trace index 1)
trendline_trace_no3 = [
    t for t in trend_fig_no3.data
    if t.mode == 'lines'   # this filters out the raw data points
]
# Add trendline to original figure
for t in trendline_trace_no3:
    t.update(line=dict(dash='dot', width=1))
    fig_no3.add_trace(t)

# use plotly go brick red for no3 plot
fig_no3.update_traces(line=dict(color='firebrick'))
# Plot
st.plotly_chart(fig_no3)

# Insert option to show dataframe upon clicking 
if st.checkbox('Show Streamflow, Sediment, and Nitrate Data'):
    st.write(df_20to50_rch)

# '''
# LINE PLOT OF CROP YIELDS
# '''
st.subheader('Crop Yields after SWAT Simulation')
#%%
# Crop codes dictionary
crop_codes = {
    "ALFA": "Alfalfa", "APPL": "Apple", "BLUE": "Blueberry", "BROC": "Broccoli",
    "CABG": "Cabbage", "CHER": "Cherry", "COLG": "Collard greens", "CORN": "Corn",
    "CRRT": "Carrot", "CUCM": "Cucumber", "DRYB": "Dry beans", "KALE": "Kale",
    "GRAP": "Grape", "HMEL": "Honeydew melon", "LETT": "Lettuce", "ONIO": "Onion",
    "PEAR": "Pear", "POTA": "Potato", "PUMP": "Pumpkin", "RASP": "Raspberry",
    "SCRN": "Sweet corn", "SNPB": "Snap beans", "SOYB": "Soybean", "SPIN": "Spinach", "SPOT": "Sweet potato",
    "SQUA": "Squash", "STRW": "Strawberry", "TOMA": "Tomato", 
    "WWHT" : "Winter Wheat",
    #"BROM": "Meadow Bromegrass", "HAY": "Hay", 
    #"CANA": "Canola oil", "SGBT": "Sugar beet", 
    # Above are missing in TxtInOutHist and Fut
    "FESC": "Tall Fescue"
    
}

#%%
# Load the continuous data : 
df_20to50=pd.read_pickle(base_dir+'/'+'mktbl_2020_2029.pickle')

# Filter and clean data
unwanted_values = ["HAY", "WATR", "WETF", "WETN"]
df_20to50 = df_20to50[~df_20to50.index.isin(unwanted_values)]


# Select a crop
# order crop_codes alphabetically by value but from the second value

crop_list = sorted(crop_codes.items(), key=lambda item: item[1])
selected_crop = st.selectbox('Select a Crop', options=crop_list, format_func=lambda x: x[1])
selected_crop_code = selected_crop[0]

# Plot a line plot of the selected crop yields over the years
crop_series = df_20to50.loc[selected_crop_code]
# convert the row into a long dataframe 
crop_df = crop_series.reset_index()
crop_df.columns = ['Year', 'Yield']
# crop_df['Year'] = crop_df['Year'].astype(int)

# Create line plot
fig_crop_yield = px.line(crop_df, x="Year", y="Yield", title=f'Crop Yield over Years for {selected_crop[1]}')
# Update x-axis label
fig_crop_yield.update_xaxes(title_text="Year")
# Update y-axis label
fig_crop_yield.update_yaxes(title_text="Yield (kg/ha)")
# Plot
st.plotly_chart(fig_crop_yield)

# Show data if checkbox is selected
if st.checkbox(f'Show Crop Yield Data for {selected_crop[1]}'):
    st.write(crop_df)
# Show the dataframe if checkbox is selected
if st.checkbox('Show All Crop Yield Data'):
    st.write(df_20to50)