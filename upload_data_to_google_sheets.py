import sys
import os
from datetime import datetime as dt
import pygsheets
import pandas as pd

#authorization
credential_file=''

gc = pygsheets.authorize(service_file=credential_file)

print("Argument List: ", str(sys.argv))
data_limit=str(sys.argv[0])
print("data_limit: ", data_limit)

today = dt.now().strftime("%m-%d-%Y")
dfs = {}
if data_limit == "today":
    print("uploading today's data: ", today)
    if os.path.isdir(today):
        for file in os.listdir(today):
            dfs[file] = pd.read_csv(os.path.join(today, file))
    else:
        raise Exception(f"Cannot Locate directory: {today} has it been downloaded?")
elif data_limit == "all":
    print("uploading all data: currently not available")

else:
    if os.path.isdir(data_limit):
        print(f"uploading {data_limit} data")
        for file in os.listdir(data_limit):
            dfs[file] = pd.read_csv(os.path.join(data_limit, file))
    else:
        raise Exception(f"Cannot Locate directory: {today} has it been downloaded?")

for key, df in dfs.items():
    sh = gc.open(file.rstrip())
    sh[0].set_dataframe(df, (1,1))