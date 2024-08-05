# sqlalchemy-challenge
module 10

## Data Analysis
### Climate Data Analysis
**Precipitation Analysis** 
- Looks at one year's worth of data from the last entry date
- Plots the precipitation by day for the last year

**Station Analysis** 
- Finds the most active station
- Calculates the lowest, highest, and average temperatures
- Plots the temperature frequency for the most active station

## Climate App 
Takes the completed analysis and creates a Flask API.
- **/api/v1.0/precipitation** percipitation analysis
- **/api/v1.0/stations** lists the stations in the dataset
- **/api/v1.0/tobs** dates and temperature observations over the past year for the most active station
- **/api/v1.0/<start>** for a specified start date, calculates temperature data points
- **/api/v1.0/<start>/<end>** for dates between the start and end dates, calculates temperature data points

## Resources
- Climate Data Analysis: [climate_starter.ipynb](https://github.com/megan-oconnor/sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb)
- Climate App: [app.py](https://github.com/megan-oconnor/sqlalchemy-challenge/blob/main/SurfsUp/app.py)
- Dataset: [hawaii.sqlite](https://github.com/megan-oconnor/sqlalchemy-challenge/blob/main/SurfsUp/hawaii.sqlite)
