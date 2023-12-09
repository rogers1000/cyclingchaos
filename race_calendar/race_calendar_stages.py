### Import Modules
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
from random import randrange
# data_table.enable_dataframe_formatter()

### Bring in Stages Races
calendar_df = pd.read_csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_RaceCalendar.csv')

calendar_df_stage_races = calendar_df.loc[calendar_df['stage_race_boolean'] == 'Stage Race']

calendar_df_stage_races_race_id = calendar_df_stage_races['race_id'].to_list()

calendar_df_stage_races_race_id_count = calendar_df_stage_races['race_id'].nunique()

### Extract Stage Race Details

race_results_df_stages = pd.DataFrame(columns=['season','first_cycling_race_id','stage'])

calendar_df_stage_races_race_id_extract = -1

for calendar_df_stage_races_race_id_extract in tqdm(range(0,
                                # 2
                                calendar_df_stage_season_race_id_stage_count
                                )):
  calendar_df_stage_races_race_id_extract = calendar_df_stage_races_race_id_extract+1
  time.sleep(5)
  try:
    url = 'https://firstcycling.com/race.php?r='+str(calendar_df_stage_race_id[calendar_df_stage_races_race_id_extract])+'&y='+str(calendar_df_stage_season[calendar_df_stage_races_race_id_extract])+'&e='+str(calendar_df_stage_stage_number[calendar_df_stage_races_race_id_extract])
  except:
    url = 'https://firstcycling.com/race.php?r=17&y=2023&e=1'
  # url = 'https://firstcycling.com/race.php?r=5247&y=2023&e=1'
  # url = 'https://firstcycling.com/race.php?r='+str(calendar_df_stage_races_race_id[calendar_df_stage_races_race_id_count])+'&y='+str(season)+'&k=2'
  # url = 'https://firstcycling.com/race.php?r=17&y=2023&k=2'
  season = calendar_df_stage_season[calendar_df_stage_races_race_id_extract]
  race_id = calendar_df_stage_race_id[calendar_df_stage_races_race_id_extract]
  stage_number = calendar_df_stage_stage_number[calendar_df_stage_races_race_id_extract]
  calendar_stage_race_stages_df_meta = requests.get(url)
  calendar_stage_race_stages_df_meta_soup = BeautifulSoup(calendar_stage_race_stages_df_meta.content, "html.parser")
  calendar_stage_race_stages_df_meta_soup_part2 = calendar_stage_race_stages_df_meta_soup.find_all('tbody')[0]

  for row in calendar_stage_race_stages_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
      season = str(season)
      first_cycling_race_id = str(race_id)
      stage_number = str(stage_number)
      try:
        position = columns[0].text
        first_cycling_rider_id = str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0]
        gc_time_leader = columns[6].text
      except:
        position = 'Error'
        first_cycling_rider_id = 'Error'
        gc_time_leader = 'Error'
      # test0 = columns[0]
      # test1 = columns[1]
      # test2 = columns[2]
      # test3 = columns[3]
      # test4 = columns[4]
      # test5 = columns[5]
      # test6 = columns[6]

      race_results_df_stages = race_results_df_stages.append({
        'season':season
        ,'first_cycling_race_id':first_cycling_race_id
        ,'stage':stage_number
        ,'position':position
        # ,'race_id':race_id
        ,'first_cycling_rider_id':first_cycling_rider_id
        # ,'team_id':team_id
        ,'gc_time_leader':gc_time_leader
        # ,'gc_time':gc_time
        # ,'rider_name':rider_name
        # ,'test0':test0
        # ,'test1':test1
        # ,'test2':test2
        # ,'test3':test3
        # ,'test4':test4
        # ,'test5':test5
        # ,'test6':test6
          }, ignore_index=True)

calendar_df_stage_races_stages_df = calendar_df_stage_races_stages_df.loc[calendar_df_stage_races_stages_df['stage_number']!= '']
# calendar_df_stage_races_stages_df
