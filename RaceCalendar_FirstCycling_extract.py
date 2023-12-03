### Importing Packages ###

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
# drive.mount('drive')

### Men's Road Calendar ###

month = 0
# Change depending on Season
season = 2023

month_extract = 0

month_str = np.where(month < 10,'0'+str(month),str(month))

current_month = datetime.now().month

current_month_range_adj = np.where(current_month < 12,current_month,12)

mens_road_calendar_df = pd.DataFrame(columns=['season','gender','race_id','race_name','category','race_nationality','uci_race_classification','stage_race_boolean','start_date','end_date'])

for month_extract in tqdm(range(1,
                                # 3
                                12
                                )):
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
  month_str = np.where(month < 10,'0'+str(month),str(month))
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=2&m='+str(month_str)
  calendar_mens_road_df_meta = requests.get(url)
  calendar_mens_road_df_meta_soup = BeautifulSoup(calendar_mens_road_df_meta.content, "html.parser")
  calendar_mens_road_df_meta_soup_part2 = calendar_mens_road_df_meta_soup.find_all('tbody')[-1]

  for row in calendar_mens_road_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
        season = str(season)
        gender = 'Men'
        category = 'Road'
        race_id = str(columns[2].find_all('a')).split('r=')[1].split('&amp')[0]
        race_name = str(columns[2].find_all('a')).split('title="')[1].split('">')[0]
        race_nationality = str(columns[2].find_all("span")).split("flag-")[1].split('"><')[0].upper()
        uci_race_classification = columns[1].text
        stage_race_boolean = np.where(columns[1].text.startswith('2'),"Stage Race","One Day")
        start_date = str(season)+'/'+columns[0].text.split('-')[0].split('.')[-1]+'/'+columns[0].text.split('-')[0].split('.')[0]
        end_date = str(season)+'/'+columns[0].text.split('-')[-1].split('.')[-1]+'/'+columns[0].text.split('-')[-1].split('.')[0]
        # test5 = columns[5]

        mens_road_calendar_df = mens_road_calendar_df.append({
            'season':season
            ,'gender':gender
            ,'category':category
            ,'race_id':race_id
            ,'race_name':race_name
            ,'race_nationality':race_nationality
            ,'uci_race_classification':uci_race_classification
            ,'stage_race_boolean':stage_race_boolean
            ,'start_date':start_date
            ,'end_date':end_date
            # ,'test5':test5
            # ,'test0':test0
        }, ignore_index=True)

### Women's Road Calendar ###

month = 0

# Change depending on Season extracting
season = 2023

month_extract = 0

month_str = np.where(month < 10,'0'+str(month),str(month))

current_month = datetime.now().month

current_month_range_adj = np.where(current_month < 12,current_month,12)

womens_road_calendar_df = pd.DataFrame(columns=['season','gender','race_id','race_name','category','race_nationality','uci_race_classification','stage_race_boolean','start_date','end_date'])

for month_extract in tqdm(range(1,
                                # 3
                                10
                                )):
  # sleep_time = randrange(4.5,5.5)
  season = np.where(month == 12,int(season)+1,season)
  month = np.where(month < 12,month + 1,1)
  # month = 1
  month_str = np.where(month < 10,'0'+str(month),str(month))
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?y='+str(season)+'&t=6&m='+str(month_str)
  calendar_womens_road_df_meta = requests.get(url)
  calendar_womens_road_df_meta_soup = BeautifulSoup(calendar_womens_road_df_meta.content, "html.parser")
  calendar_womens_road_df_meta_soup_part2 = calendar_womens_road_df_meta_soup.find_all('tbody')[-1]

  for row in calendar_womens_road_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
        season = str(season)
        gender = 'Women'
        category = 'Road'
        first_cycling_race_id = str(columns[2].find_all('a')).split('r=')[1].split('&amp')[0]
        race_name = str(columns[2].find_all('a')).split('title="')[1].split('">')[0]
        race_nationality = str(columns[2].find_all("span")).split("flag-")[1].split('"><')[0].upper()
        uci_race_classification = columns[1].text
        stage_race_boolean = np.where(columns[1].text.startswith('2'),"Stage Race","One Day")
        start_date = str(season)+'/'+columns[0].text.split('-')[0].split('.')[-1]+'/'+columns[0].text.split('-')[0].split('.')[0]
        end_date = str(season)+'/'+columns[0].text.split('-')[-1].split('.')[-1]+'/'+columns[0].text.split('-')[-1].split('.')[0]
        # test5 = columns[5]

        womens_road_calendar_df = womens_road_calendar_df.append({
            'season':season
            ,'gender':gender
            ,'category':category
            ,'first_cycling_race_id':first_cycling_race_id
            ,'race_name':race_name
            ,'race_nationality':race_nationality
            ,'uci_race_classification':uci_race_classification
            ,'stage_race_boolean':stage_race_boolean
            ,'start_date':start_date
            ,'end_date':end_date
            # ,'test5':test5
            # ,'test0':test0
        }, ignore_index=True)

### Putting final steps of calendar together ###

calendar_df = pd.concat([mens_road_calendar_df,womens_road_calendar_df], ignore_index = True)

calendar_df = calendar_df.drop_duplicates(subset = 'first_cycling_race_id')

calendar_df['race_tag'] = np.where(calendar_df['first_cycling_race_id'].isin(['8','11','5','4','24','13853',]),'Monument',
                                   np.where(calendar_df['first_cycling_race_id'].isin(['13','17','23','15687','9058','9064']),'Grand Tour',
                                   np.where(calendar_df['first_cycling_race_id'].isin(['53','84','116','47','7','75','56','77']),'Cobbled Classic',
                                            '')))



