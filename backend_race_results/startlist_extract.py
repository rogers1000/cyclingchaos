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

calendar_df = pd.read_csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/race_calendar/CyclingChaos_RaceCalendar.csv')

calendar_df['future_race'] = pd.to_datetime(calendar_df['end_date'], format='%Y/%m/%d') > pd.to_datetime('today', format='%Y/%m/%d')

calendar_df = calendar_df.loc[calendar_df['future_race'] == False]

calendar_df['first_cycling_race_id'] = calendar_df['first_cycling_race_id'].apply(str)
calendar_df['season'] = calendar_df['season'].apply(str)

### Get count of number of race extracts required
startlist_list_race_id = calendar_df['first_cycling_race_id'].tolist()
startlist_list_season = calendar_df['season'].tolist()
race_id_count_limit = calendar_df['first_cycling_race_id'].nunique()

### Startlist Dataframe creation ###
startlist_df_riders = pd.DataFrame(columns=['season','first_cycling_race_id','bib_number_order','bib_number','first_cycling_rider_id'])

startlist_df_teams = pd.DataFrame(columns=['season','first_cycling_race_id','bib_number_order','first_cycling_team_id'])

startlist_extract = -1

startlist_list_race_id_test = startlist_list_race_id[2:]

for race_id_count in tqdm(range(0,
                                # 10
                                race_id_count_limit
                                )):
  bib_number_order_teams = 0
  bib_number_order_riders = 0
  bib_number_order_riders_team_count = 0
  startlist_extract = startlist_extract + 1
  season = startlist_list_season[startlist_extract]
  first_cycling_race_id = startlist_list_race_id[startlist_extract]
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?r='+str(first_cycling_race_id)+'&y='+str(season)+'&k=8'
  startlist_df_meta = requests.get(url)
  startlist_df_meta_soup = BeautifulSoup(startlist_df_meta.content, "html.parser")

  for row in startlist_df_meta_soup.find_all('table')[2:]:
    columns = row.find_all('th')
    bib_number_order_teams = bib_number_order_teams + 1

    if(columns != []):
      season = str(season)
      # test0 = columns[0]
      # test1 = columns[1]
      # test2 = columns[2]
      # test3 = columns[3]
      # test4 = columns[4]
      # test5 = columns[5]
      # test6 = columns[6]
      first_cycling_team_id = np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                        #  str(columns[0]).split('l=')[-1].split('" ')[0].split('">')[-1].split('</th')[0]
                         None
                         ,str(columns[0]).split('l=')[-1].split('" ')[0])
      team_name_invitational = np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                         str(columns[0]).split('l=')[-1].split('" ')[0].split('">')[-1].split('</th')[0]
                        #  ,str(columns[0]).split('l=')[-1].split('" ')[0]
                                        , None)
      # team_name = columns[0].text

      startlist_df_teams = startlist_df_teams.append({
          'season':season
          ,'first_cycling_race_id':first_cycling_race_id
          ,'bib_number_order':bib_number_order_teams
          ,'first_cycling_team_id':first_cycling_team_id
          ,'team_name_invitational': team_name_invitational
          # ,'team_name':team_name
          # ,'test0':test0
          # ,'test1':test1
          # ,'test2':test2
          # ,'test3':test3
          # ,'test4':test4
          # ,'test5':test5
          # ,'test6':test6
      }, ignore_index=True)

  startlist_df_number_of_teams_in_race = int(startlist_df_teams['bib_number_order'][-1:])

  for bib_number_order_riders_team_count in range(0,startlist_df_number_of_teams_in_race):
    startlist_df_meta_soup_part2 = startlist_df_meta_soup.find_all('tbody')[bib_number_order_riders_team_count]

    for row in startlist_df_meta_soup_part2.find_all('tr'):
      columns = row.find_all('td')
      bib_number_order_riders = bib_number_order_riders + 1

      if(columns != []):
        season = str(season)
        # test0 = columns[0]
        # test1 = columns[1]
        # test2 = columns[2]
        # test3 = columns[3]
        # test4 = columns[4]
        # test5 = columns[5]
        # test6 = columns[6]
        bib_number = columns[0].text
        first_cycling_rider_id = str(columns[1].find_all('a')).split('r=')[1].split('&amp')[0]
        # rider_name = columns[1].text

        startlist_df_riders = startlist_df_riders.append({
              'season':season
              ,'first_cycling_race_id':first_cycling_race_id
              ,'bib_number_order':bib_number_order_riders_team_count+1
              ,'bib_number':bib_number
              ,'first_cycling_rider_id':first_cycling_rider_id
              # ,'rider_name':rider_name
              # ,'test0':test0
              # ,'test1':test1
              # ,'test2':test2
              # ,'test3':test3
              # ,'test4':test4
              # ,'test5':test5
              # ,'test6':test6
          }, ignore_index=True)

### Merge Startlist rider data with Startlist team data

startlist_df = startlist_df_riders.merge(startlist_df_teams,on = ['season','first_cycling_race_id','bib_number_order'])
startlist_df = startlist_df.drop(['bib_number_order'], axis = 1)