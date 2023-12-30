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
cci_output = []
cci_output_details = []
cci_file_name = []

month = 0
month_str = np.where(month < 10,'0'+str(month),str(month))
season = 2023

month_extract = 0

for month_extract in tqdm(range(0,
                                #2
                                12
                                )):
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
  # month = 1
  month_str = np.where(month < 10,'0'+str(month),str(month))
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=2&m='+str(month_str)
  calendar_mens_road_df_meta = requests.get(url)
  calendar_mens_road_df_meta_soup = BeautifulSoup(calendar_mens_road_df_meta.content, "html.parser")
  calendar_mens_road_df_meta_soup_str = str(calendar_mens_road_df_meta_soup)
  file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'men'+'_'+str(season)+'_'+str(month_str)+'.txt
#   with open(r'/Users/zacrogers/Documents/cycling_chaos/python_code/calendar_ingestion_files/'+file_name, 'w') as writefile:
  with open(setwd+'calendar_ingestion_files/'+file_name, 'w') as writefile:
    writefile.write(calendar_mens_road_df_meta_soup_str)
    writefile.close()
  cci_output.append('calendar')
  cci_output_details.append('Men')
  cci_file_name.append(file_name)

  print('Ingested '+file_name)

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df.csv', index=False)

print(cycling_chaos_ingestion)

##### Women's Calendar Ingestion #####
cycling_chaos_ingestion = pd.read_csv('/Users/zacrogers/Documents/cycling_chaos/python_code/cycling_chaos_ingestion_df.csv')

month = 0
month_str = np.where(month < 10,'0'+str(month),str(month))
season = 2023

month_extract = 0

for month_extract in tqdm(range(0,
                                #2
                                12
                                )):
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
  # month = 1
  month_str = np.where(month < 10,'0'+str(month),str(month))
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=6&m='+str(month_str)
  calendar_womens_road_df_meta = requests.get(url)
  calendar_womens_road_df_meta_soup = BeautifulSoup(calendar_womens_road_df_meta.content, "html.parser")
  calendar_womens_road_df_meta_soup_str = str(calendar_womens_road_df_meta_soup)
  file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'women'+'_'+str(season)+'_'+str(month_str)+'.txt'
  # with open(r'/Users/zacrogers/Documents/cycling_chaos/python_code/calendar_ingestion_files/'+file_name, 'w') as writefile:
  with open(setwd+'calendar_ingestion_files/'+file_name, 'w') as writefile:
    writefile.write(calendar_womens_road_df_meta_soup_str)
    writefile.close()
    cci_output.append('calendar')
    cci_output_details.append('Women')
    cci_file_name.append(file_name)

  print('Ingested '+file_name)

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df.csv', index=False)

print(cycling_chaos_ingestion)
