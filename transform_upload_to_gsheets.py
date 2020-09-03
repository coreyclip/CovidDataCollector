import os
from datetime import datetime as dt
import pandas as pd
import pygsheets

df = pd.read_csv('data/scraped_data/08-27-2020/LA_County_Covid19_CSA_case_death_table.csv').drop('Unnamed: 0',1).set_index('City/Community')
tdf = pd.read_csv('data/scraped_data/08-27-2020/LA_County_Covid19_CSA_testing_table.csv').drop('Unnamed: 0',1)

cities = df.index
dates = os.listdir('data/scraped_data')
columns = list(df.columns.append(tdf.columns))
columns.remove("timestamp")
case_columns = df.columns
testing_columns = tdf.columns
cdf = df.join(tdf)

def set_index_to_geo(df):
    if 'geo_merge' in df.columns:
        df.set_index('geo_merge', inplace=True)
        df.index.rename('City/Community', inplace=True)
    elif 'City/Community' in df.columns:
        df.set_index('City/Community', inplace=True)
    else:
        raise Exception(f"missing geo column: {df.info()}")
    return df

dfs = {}
for d in os.listdir('data/scraped_data'):
    if os.path.isdir(os.path.join('data/scraped_data', d)):
        date = d
        dfs[date] = {}
        
        case_death_path = os.path.join(os.path.join('data/scraped_data', d),'LA_County_Covid19_CSA_case_death_table.csv')
        if os.path.exists(case_death_path):
            dfs[date]['case_death'] = set_index_to_geo(pd.read_csv(case_death_path).drop('Unnamed: 0',1))
        else:
            dfs[date]['case_death'] = pd.DataFrame(index=[cities], data=[], columns=case_columns)
            
        testing_path = os.path.join(os.path.join('data/scraped_data', d),'LA_County_Covid19_CSA_testing_table.csv')
        if os.path.exists(testing_path):
            dfs[date]['testing'] = set_index_to_geo(pd.read_csv(testing_path).drop('Unnamed: 0',1))
        else:
            dfs[date]['testing'] = pd.DataFrame(index=[cities], data=[], columns=testing_columns)
                
cities_dfs = {}
for city in cities:
    city_df = pd.DataFrame(index=dates, data=[], columns=columns)
    for date in dates:
        if 'case_death' in dfs[date].keys():
            if city in dfs[date]['case_death'].index:
                cdf = dfs[date]['case_death'].loc[city]
            else:
                cdf = pd.DataFrame(index=[city], data=[], columns=case_columns)
        else:
            cdf = pd.DataFrame(index=[city], data=[], columns=case_columns)
        if 'testing' in dfs[date].keys():
            if city in dfs[date]['testing'].index:
                tdf = dfs[date]['testing'].loc[city]
            else:
                tdf = pd.DataFrame(index=[city], data=[], columns=testing_columns)
        else:
            tdf = pd.DataFrame(index=[city], data=[], columns=testing_columns)
        row = cdf.append(tdf).to_dict()
        city_df.loc[date] = row
    city_df.index = pd.Series(city_df.index).apply(lambda x: dt.strptime(x,"%m-%d-%Y"))
    city_df.sort_index(inplace=True)
    city_df.index.rename('Date', inplace=True)
    city_df.drop(columns=['geo_merge'], inplace=True)
    cities_dfs[city] = city_df
    
for key, df in cities_dfs.items():
    city = key.replace('/', '-')
    path = os.path.join('data/parsed_data', f"{city}.csv")
    df.to_csv(path)
    
gc = pygsheets.authorize(service_file='metal-density-185407-715708b8cad6.json')
# gc.create('LA County Covid-19 Community Level Data')
sh = gc.open('LA Covid-19 Community Level Data')

zorgi_wants = [
"City of Industry",
"Los Angeles - Wholesale District",
"City of Vernon",
"Los Angeles - Central",
"Los Angeles - South Park",
"Los Angeles - Florence-Firestone",
"Los Angeles - Little Armenia",
"Los Angeles - Boyle Heights",
"City of Maywood",
"East LA",
"West LA",
"City of Huntington Park",
"City of Irwindale",
"Los Angeles - Westlake",
"Los Angeles - Downtown",
"Unincorporated - Athens Village",
"City of Lynwood"
]

for city, i in zip(zorgi_wants, range(0, len(zorgi_wants))):
    try:
        sh.add_worksheet(city)
    except Exception as e:
        pass
#         print(str(e))
    if city in cities:
        try:
            assert sh[i].title == city
            sh[i].set_dataframe(cities_dfs[city].reset_index(), (1,1))
        except:
            print(f"{i} {city} {sh[i].title}")
        