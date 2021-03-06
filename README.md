# Data-X: Hondezvous x 99P Labs: Vehicle Destination & Dwell Time Prediction Project

## Project Overview:
### Value Proposition:
#### Give your car a new purpose.

Have you ever needed something delivered to you while you’re at work? Have you ever wanted your car repaired while you’re out at the movies? What about earning passive income from your parked car?

**With our solutions, you can make your car a delivery location,  get services on the move, and enter your car into the gig economy.**
### Summary:
We teamed up with 99P Labs to work on building predictive models for dwell time duration and location, giving drivers the ability to opt-in to a variety of services, such as Amazon Key, and giving partner services the ability to thrive in a hungry market.

### Objective:
A crucial step towards our team’s success was approaching the problem through an entrepreneurial lens, not as data scientists and engineers; and doing so, we were able to start asking the right questions. We shifted our thinking from “Can we create a probability distribution for a car’s dwell time given a location?” to **“Can this service be fulfilled or not?”** We restructured our approach to the model implementations to predict a binary yes or no rather than an exact distribution. This switch in approach better fit what our service providers were looking for and helped us optimize accuracy.

## Approach
* Clustering/KNN Model for Dwell Time Prediction
  * Dataset containing Location (Latitude and Longitude), timestamp (UNIX), and dwell time duration (time elapsed between consecutive engine cycles) was used in this model.
  * A Density Based Spacial Clustering of Applications with Noise (DBScan) was applied to the dataset to generate a "network" of clusters. These clusters capture trends and patterns between time of day, location, and dwell time. Epsilon and Minimum Sample values for DBScan were identified through trial and error and a common-sense methodology.
  * After these clusters were created, a KNN/XGboost model was trained and tuned to predict what cluster a new data-point (containing latitude, longitude, time of day) belongs to. That new point was then predicted the mode dwell-time of its predicted cluster. 
* XGBoost for Dwell Time Prediction
  * Dataset containing Location (Latitude and Longitude), timestamp (UNIX), and dwell time duration (time elapsed between consecutive engine cycles) was used in this model 
  * An additional XGboost model was trained and tuned to solve a binary classification variation of our problem space - is the dwell time greater than 10 hours?
  * This model utilised the location and time of day to predict if a new datapoint will have a dwell time that is greater than 10 hours or not. I.e. will a car that just stopped be stationary for 10+ hours
  * Highest accuracy model due to 10+ hour stops having a strong relationship with time of day and location.


* Markov Model for Location Prediction
  * Markov models work by having a set of states, for which each pair of states i, j in the set has an associated probability of moving from state i to state j. To apply a Markov model to our data, we initially set location clusters as unique states in the Markov chain and calculated the probabilities of moving from the current location to a different location for each car. To process the data, we dropped all rows with no dwell time durations in order to only use completed trips, and kept latitude and longitude for only start and end locations.
  * For the model architecture, we first set a buffer in order to prevent an excessive amount of coordinates that were generally in the same area (e.g. driveway vs the street in front of a house) and grouped these locations under one state. After we found the set of all unique states (read: locations) a car visited, we wrote a transition function that calculates the probability of the car starting in location i and ending in location j for all locations in the set of states. To do this, we utilized the prob140 data science library, created for UC Berkeley’s Data140 course.
  * After we calculated the transition probabilities for every state, we wrote a function that took in a car’s ID number and returned the next most likely states, and their corresponding probabilities, given its last recorded state in the dataset.
  * We converted all the top locations for each vehicle into a separate data frame with corresponding probabilities that summed up to 80% since we didn’t want to consider the rest with very low probabilities. We then appended all data frames together to add a dwell time column to the final one and add it to our UI.


## Files
#### Data
* Newdataset.csv
   * This file contains about 47,000 rows of filtered data from the 99PLabs API. The original file contained about 35 million rows of raw data and was grouped by vin and sequence for each vehicle and trip in the original dataset. The timestamp column was converted into a datetime object in the form of seconds from milliseconds, and the dwell time calculations between the end of the previous trip and current trip were added into another separate column. With the data fully preprocessed, this csv file was used in both the Markov and dwell time prediction notebooks to proceed with model implementation.
* Locationpredictions.csv
   * Towards the end of the Markov.ipynb notebook, we created a function that finds the top few location predictions for each vehicle and creates a dataframe with the vin, sequence, predicted latitude, predicted longitude, and probabilities to then add a column for dwell time predictions.
#### Data Cleaning and Processing
* DataProcessing.ipynb
  * Raw data is event-based, pulled from cars' telemetry and navigation systems. Due to the nature of the event-based gathering system, the contained NaN-valued rows at a exceedingly high ratio to non-NaN valued rows. Data cleaning retention of 10%, meaning after sifting out NaNs we had 10% of the amount of data we started with. This required implementation of a pagination method to succesfully pull a large enough, cleaned dataset from Honda's API. Addtionaly geofencing was added into the pagination methodology to select trips that within the vicinity of Columbus, OH.
  * The data was trip-based and recorded at a near milisecond interval, meaning a single car driving for an hour is 3.6e+6 rows of data. 
  * The data was aggregated and logic was implemented to extract the start and end location of each trip sequence, and the time elapsed between engine cycles (difference in timestamp from last stop to next start) was calculated and named dwell time duration
  * This aggregated data-set contained roughly 40 thousand records, each with a location, dwell time, and timestamp.
  * This notebook was used to preprocess all of our data straight from the 99PLabs API. Since we needed to deal with millions of rows of data, we didn’t initially have enough compute power through our collaborative notebook, so we followed these steps locally to filter the huge csv file with 35 million rows of data, narrow it down, and import it into the notebook to begin model implementation. The example shown in the notebook uses the original csv file we started off with, which included about 760,000 rows of data.


#### Models
* Dwell_prediction.ipynb
  * Utilised Sklearn, XGBoost, matplotlib, Pandas, NumPy, Seaborn, GeoPandas
  
  Dwell Time Prediction model has X key functions:
   * gen_dbs_clusters
      * inputs: DataFrame containing location and dwell time interval, epsilon and min_samples values for DBSCAN
      * output: DataFrame containing location, dwell time interval, associated DBS clusters
   * plot_clusters
      * inputs: DataFrame containing location, dwell time interval, associated DBS clusters
      * output: Visualisation of created clusters on a geographic map
   * gen_bins_pointwise
      * inputs: df1 = DataFrame, containing lat,long, dwell time duration (seconds), minimum interval value, maximum interval value 
      * output: A DataFrame containing location, dwell time interval, associated interval bins
   * train_pred_model
      * inputs: DataFrame containing location, dwell time interval, associated DBS clusters, two boolean flags (knn, svm)
      * output: A trained prediction model with tuned hyperparameters to predict dbs_cluster, prints CV score
   * predicted_cluster_vals
      * inputs: DataFrame, containing lat, long, daylight, dbs_cluster and a trained prediction model
      * output: DataFrame containing Lat,Long, predicted_cluster
   * get_interval_pred
      * inputs: DataFrame, containing lat, long, daylight, predicted DBS Cluster and a Dataframe containing true values
      * output: DataFrame containing lat, long, dwell time interval, associated interval bins (Predictions for interval bins)

* Markov.ipynb
  * Used the prob140 data science library from UC Berkeley's Data 140 course to implement some of the Markov predictions.
  * [Link to Prob 140 Github repository](https://github.com/prob140/prob140)
 
  The Markov Chain model has 3 key functions:
   * vehicle_locations
      * input: vehicle ID (string), table of all cars (dataframe)
      * output: a dictionary of all locations that the unique car has been to, within a specified buffer
   * make_markov_function
      * input: vehicle ID (string), table of all cars (dataframe), all locations the car has been to (dictionary)
      * output: a callable markov function that is compatible with the prob140 package
   * get_all_locations
      * input: vehicle ID (string), table of all cars (dataframe)
      * output: a dataframe with columns for a car's next predicted location and associated probability

 #### UI

* STREAMLIT-UI.ipynb
  * This notebook installs Streamlit and generates the URL for our UI. Run through all the cells and copy the output URL of this cell into the browser:
```python:
!curl -s http://localhost:4040/api/tunnels | python3 -c \
    'import sys, json; print("Execute the next cell and the go to the following URL: " +json.load(sys.stdin)["tunnels"][0]["public_url"])'
```
* HONDEZVOUS_UI_PREDLOC.py
  * THis python file takes input from our two individual models with the generated data frame. It plots the clusters of all the vehicles, and has a sidebar to filter through vehicle IDs and clusters. The filtered result will be plotted with the predicted locations of the specific vehicles, as well as the binary predicted dewell time. Filtered results for clusters plots a map with that cluster and its coordinates.
  
