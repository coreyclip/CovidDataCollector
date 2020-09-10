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

## Data Section
**data/scraped_data** - raw data scraped from the LA County Public Health Dashboard organized by date scraped
**data/parsed_data** - data reorganized by community, reindexed by  

## Community Whitelisting 
in the script `transform_upload_to_gsheets.py` set the variable city_whitelist to include communities that the
script will specifcally seek out to process for google sheet uploads

## Helpful Docs 
https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/

accessing external APIs with google sheets:
https://developers.google.com/apps-script/guides/services/external
