import streamlit as st
import pandas as pd
import numpy as np
import datetime
import importlib
import jinja2
from ipywidgets import HTML
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px

import KNNLite # slimmed down version of KNN for clusters 
exec(open('KNNLite.py').read()) # run KNN Lite

# read mapbox token
mapbox_access_token = open(".mapbox_token").read()

# Read csv file
df_binary_pred = pd.read_csv("/work/Data/BinaryPredictedDwelltime.csv")
df_clusters = pd.read_csv("/work/Data/clusters.csv")

# LAYING OUT THE TOP SECTION OF THE APP WITH DASHBOARD INFO AND CLUSTER MAP ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
row1_1, row1_2 = st.beta_columns((2,3))

with row1_1:  
    st.title('Hondezvous Dashboard') # Dashboard title
    st.write(
    """
    ##
    Predicting vehicle dwell times and location.
    You can use the sidebar to filter for specific vehicles
    and will be returned a map with predicted locations and
    binary dwell time prediction. You can also choose to view
    a selected cluster. New filter features coming soon!
    """) # Dashboard description

with row1_2:
    st.subheader('Vehicle Clusters') # Vehicle cluster header
    st.map(dbs_df) # Plot vehicle clusters  


today = datetime.date.today() # Defining today's date
tomorrow = today + datetime.timedelta(days=1) # Defining tomorrow's date

# LAYING OUT THE SIDE BAR OF THE APP ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.header('Dashboard Filters') # Set the sidebar header

# choose a vin to track
vin_to_track = st.sidebar.selectbox(
    'Choose a Vin to track',
    (df_binary_pred['vin'])
)

# Choose a cluster to view
cluster_to_track = st.sidebar.selectbox(
    'Choose a cluster to track',
    (dbs_df['dbs_cluster'].unique())
)

st.sidebar.subheader('New Filters Coming Soon:') # Set the sidebar subheader

start_date = st.sidebar.date_input('Start date', today) # Define start date in the sidebar
end_date = st.sidebar.date_input('End date', tomorrow) # Define end date in the sidebar

# Save latitude and longitude values of the selected vehicle into data frame
matched_rows = df_binary_pred.index[df_binary_pred.vin.str.match(vin_to_track)]
matched_lat = df_binary_pred.iloc[matched_rows,2]
matched_lon = df_binary_pred.iloc[matched_rows,3]

# Add dwell time interval information to the data frame
matched_dwell = []
display_text = []
for i in np.arange(len(matched_rows)):
    matched_dwell.append(df_binary_pred.iloc[matched_rows[i],4])
    display_text.append('Predicted Location for VIN ' + str(vin_to_track) + ', ' + 'Dwell Time > 10hr: ' + str(df_binary_pred.iloc[matched_rows[i],4]))



# Save latitude and longitude values of the selected cluster into data frame
matched_cluster_rows = list(df_clusters['dbs_cluster']).index(cluster_to_track)

#= df_clusters.index[df_clusters.dbs_cluster.str.match(str(cluster_to_track))]
matched_cluster_lat = df_clusters.iloc[matched_cluster_rows,2]
matched_cluster_lon = df_clusters.iloc[matched_cluster_rows,3]


#Plot figure for predicted locations using mapbox scatter function
fig_pred = go.Figure(go.Scattermapbox(
   lat=matched_lat, # define the latitudes to plot
   lon=matched_lon, # define the longitudes to plot
   mode='markers', 
    marker=go.scattermapbox.Marker(
       size=12
   ),
    text=display_text, # text to display with each point
))

# Setting up map layout and map parameteres
fig_pred.update_layout(height=500, width=350, # change layout size
   margin=dict(l=20, r=20, t=20, b=20), # define margins
   autosize=True,
   hovermode='closest',
   mapbox=dict(
       accesstoken=mapbox_access_token,
       bearing=0,
       center=dict( # map centering
                lat=matched_lat[matched_lat.index[0]], # centering latitude on first matched latitude
                lon=matched_lon[matched_lon.index[0]] # centering longitude on first matched longitude
        ),
        pitch=0,
        zoom=10
    ),
)





#Plot figure for selected cluster using mapbox scatter function
fig_clust = go.Figure(go.Scattermapbox(
   lat=[matched_cluster_lat], # define the latitudes to plot
   lon=[matched_cluster_lon], # define the longitudes to plot
   mode='markers', 
    marker=go.scattermapbox.Marker(
       size=12
   ),
    text=['Cluster ' + str(cluster_to_track)], # text to display with each point
))

# Setting up map layout and map parameteres
fig_clust.update_layout(height=500, width=350, # change layout size
   margin=dict(l=20, r=20, t=20, b=20), # define margins
   autosize=True,
   hovermode='closest',
   mapbox=dict(
       accesstoken=mapbox_access_token,
       bearing=0,
       center=dict( # map centering
                lat=matched_cluster_lat, # centering latitude on first matched latitude
                lon=matched_cluster_lon # centering longitude on first matched longitude
        ),
        pitch=0,
        zoom=10
    ),
)



# LAYING OUT THE BOTTOM SECTION OF THE APP WITH PREDICTED LOCATION & SELECTED CLUSTER MAPS -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

row2_1, row2_2 = st.beta_columns((2,2))

with row2_1:  
    st.subheader('Next Predicted Location')
    st.plotly_chart(fig_pred, height=500, width=350)

with row2_2:
    st.subheader('Selected Cluster')
    st.plotly_chart(fig_clust, height=500, width=350)



if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date)) # Show succesful selection
else:
    st.error('Error: End date must fall after start date.') # Return error for incorrect user input