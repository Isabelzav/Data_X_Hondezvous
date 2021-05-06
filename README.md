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
* Clustering/KNN Model


* Markov Model
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
  * This notebook was used to preprocess all of our data straight from the 99PLabs API. Since we needed to deal with millions of rows of data, we didn’t initially have enough compute power through our collaborative notebook, so we followed these steps locally to filter the huge csv file with 35 million rows of data, narrow it down, and import it into the notebook to begin model implementation. The example shown in the notebook uses the original csv file we started off with, which included about 760,000 rows of data.


#### Models
* Dwell_prediction.ipynb

* Markov.ipynb
 * Used the prob140 data science  library from UC Berkeley's Data 140 course to implement some of the Markov predictions.
 * [Link to Prob 140 Github repository](https://github.com/prob140/prob140)#### UI

* STREAMLIT-UI.ipynb

* HONDEZVOUS_UI.py
  
