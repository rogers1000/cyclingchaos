# Importing Modules required for code to work
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import time
from datetime import timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup
import os
import re
from time import sleep
from random import randrange

##### Making Code Possible to Put onto Github #####

#setwd = #Your Working Directory

##### Men's Calendar Ingestion #####

# Bring in ingestion master as lists, so you can track what you have ingested in this code

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# Create month as a string where numbers are all double digits

month = 0
month_str = np.where(month < 10,'0'+str(month),str(month))

# Select what season you want to ingest
season = 2024

# Count how many months you have ingested

month_extract = 0

# ingestion loop

for month_extract in tqdm(range(0,
                                #2
                                12
                                )):
# In theory this menas you can do multiple seasons at once, but not been tested.
# month counter is what we use within url for ingestion
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
# month needs to be double digits as a string
  month_str = np.where(month < 10,'0'+str(month),str(month))
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
  time.sleep(5)
# url is base calendar website with season and then month_str. 't=2' means Men's UCI
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=2&m='+str(month_str)
# beautiful soup usage to get html code
  calendar_mens_road_df_meta = requests.get(url)
  calendar_mens_road_df_meta_soup = BeautifulSoup(calendar_mens_road_df_meta.content, "html.parser")
  calendar_mens_road_df_meta_soup_str = str(calendar_mens_road_df_meta_soup)
  file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'men'+'_'+str(season)+'_'+str(month_str)+'.txt'
# write file to disk
  with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
    writefile.write(calendar_mens_road_df_meta_soup_str)
    writefile.close()
# add ingest details to ingestion master tracker
  cci_output.append('calendar')
  cci_output_details.append('Men')
  cci_file_name.append(file_name)
# ensures that code is working and ingesting properly.
  print('Ingested '+file_name)

# make ingestion master lists back into a dataframe and save the new csv
cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})
cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df.csv', index=False)

# check ingestion master is working
print(cycling_chaos_ingestion)

##### Women's Calendar Ingestion #####

# Bring in ingestion master as lists, so you can track what you have ingested in this code
cycling_chaos_ingestion = pd.read_csv('/Users/zacrogers/Documents/cycling_chaos/python_code/cycling_chaos_ingestion_df.csv')

# Create month as a string where numbers are all double digits

month = 0
month_str = np.where(month < 10,'0'+str(month),str(month))

# Select what season you want to ingest
season = 2024

# Count how many months you have ingested
month_extract = 0

# ingestion loop

for month_extract in tqdm(range(0,
                                #2
                                12
                                )):
# In theory this menas you can do multiple seasons at once, but not been tested.
# month counter is what we use within url for ingestion
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
  month_str = np.where(month < 10,'0'+str(month),str(month))
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
  time.sleep(5)
# url is base calendar website with season and then month_str. 't=6' = Women's UCI
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=6&m='+str(month_str)
# beautiful soup usage to get html code
  calendar_womens_road_df_meta = requests.get(url)
  calendar_womens_road_df_meta_soup = BeautifulSoup(calendar_womens_road_df_meta.content, "html.parser")
  calendar_womens_road_df_meta_soup_str = str(calendar_womens_road_df_meta_soup)
  file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'women'+'_'+str(season)+'_'+str(month_str)+'.txt'
# write to disk
  with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
    writefile.write(calendar_womens_road_df_meta_soup_str)
    writefile.close()
# add ingest details to ingestion master tracker
    cci_output.append('calendar')
    cci_output_details.append('Women')
    cci_file_name.append(file_name)

# ensures that code is working and ingesting properly.
  print('Ingested '+file_name)

# make ingestion master lists back into a dataframe and save the new csv
cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df.csv', index=False)

# check ingestion master is working
print(cycling_chaos_ingestion)
