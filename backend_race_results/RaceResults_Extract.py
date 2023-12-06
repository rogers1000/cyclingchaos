### Import Modules ###
import pandas as pd
import numpy as np
import requests
# from google.colab import data_table
from datetime import datetime
import time
from datetime import timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup
# from google.colab import files
import os
import re
from time import sleep
# from google.colab import drive
from random import randrange
# data_table.enable_dataframe_formatter()

### Get data from Calendar_df

calendar_df = pd.read_csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/race_calendar/CyclingChaos_RaceCalendar.csv')

### Check if race happens in future or not

calendar_df['future_race'] = pd.to_datetime(calendar_df['end_date'], format='%Y/%m/%d') > pd.to_datetime('today', format='%Y/%m/%d')

calendar_df = calendar_df.loc[calendar_df['future_race'] == False]

### Change data from numeric to varchar

calendar_df['first_cycling_race_id'] = calendar_df['first_cycling_race_id'].apply(str)
calendar_df['season'] = calendar_df['season'].apply(str)

### Filter out TTTs from race results scrape

calendar_df = calendar_df[~calendar_df['first_cycling_race_id'].isin(['462','9338','15151','9049','647','21369','21139','12533','12532'])]

### Get count of number of race extracts required
startlist_list_race_id = calendar_df['first_cycling_race_id'].tolist()
startlist_list_season = calendar_df['season'].tolist()
race_id_count_limit = calendar_df['first_cycling_race_id'].nunique()

### Scrape Results

race_results_df = pd.DataFrame(columns=['season','first_cycling_race_id','position','first_cycling_rider_id','gc_time'])

results_extract = -1

for race_id_count in tqdm(range(0,
                                # 10
                                race_id_count_limit
                                )):
  results_extract = results_extract + 1
  season = startlist_list_season[results_extract]
  first_cycling_race_id = startlist_list_race_id[results_extract]
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?r='+str(first_cycling_race_id)+'&y='+str(season)
  results_df_meta = requests.get(url)
  results_df_meta_soup = BeautifulSoup(results_df_meta.content, "html.parser")
  results_df_meta_soup_part2 = results_df_meta_soup.find_all('tbody')[0]

  for row in results_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
      season = str(season)
      stage = 'GC'
      position = columns[0].text
      # gc_time = columns[6].text
      gc_time_leader = (columns[6].text)
      # gc_seconds = str(columns[6].text).split(':')
      # gc_mins = str(columns[6].text)
      # gc_hours = str(columns[6].text).split(':')[0]
      first_cycling_rider_id = str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0]
      # team_id = str(columns[4].find_all('a')).split('?l=')[-1].split('" title=')[0]
      # year_of_birth = columns[1].text
      # uci_points = columns[5].text
      # rider_nationality = columns[2].find_all('span')
      # test0 = columns[0]
      # test1 = columns[1]
      # test2 = columns[2]
      # test3 = columns[3]
      # test4 = columns[4]
      # test5 = columns[5]
      # test6 = columns[6]

      race_results_df = race_results_df.append({
        'season':season
        ,'stage':stage
        ,'position':position
        ,'first_cycling_race_id':first_cycling_race_id
        ,'first_cycling_rider_id':first_cycling_rider_id
        # ,'team_id':team_id
        ,'gc_time_leader':gc_time_leader
        # ,'rider_name':rider_name
        # ,'test0':test0
        # ,'test1':test1
        # ,'test2':test2
        # ,'test3':test3
        # ,'test4':test4
        # ,'test5':test5
        # ,'test6':test6
          }, ignore_index=True)

### Bring in Startlist data
startlist_df = pd.read_csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_results/CyclingChaos_startlists.csv')

startlist_df['first_cycling_race_id'] = startlist_df['first_cycling_race_id'].apply(str)
startlist_df['first_cycling_rider_id'] = startlist_df['first_cycling_rider_id'].apply(str)
startlist_df['season'] = startlist_df['season'].apply(str)

### Merge data to get everything required

race_results_startlist_df = race_results_df.merge(startlist_df,on = ['season','first_cycling_race_id','first_cycling_rider_id']).merge(calendar_df, on = ['season','first_cycling_race_id'])


