# CovidDataCollector

## Project aim
Download and parse covid data from local government websites
requires python 3.6+

Currently we're focusing on data located on this page and in particular grabbing the Community level data:
http://dashboard.publichealth.lacounty.gov/covid19_surveillance_dashboard/

We either need to automate the process of downloading the csv files from a button click or just grab the html table and convert it to a pandas dataframe. Ideally we'd want to grab this data daily and make sure it's timestamped. 

The Tabs in question with table data:
- Community Case/Death
- Community Testing


Next we have to figure out how to properly take this data and upload it to google sheets for public consumption 
Here we have to put some thought into a data schema 

once these parts are finished, we then look at a proper system for setting these to timers.
