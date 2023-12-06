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

season = 2023

calendar_df_stage_races_race_id_extract = -1

calendar_df_stage_races_stages_df = pd.DataFrame(columns=['season','first_cycling_race_id','stage_number','distance','stage_profile_category','route'])

for calendar_df_stage_races_race_id_extract in tqdm(range(0,
                                # 10
                                calendar_df_stage_races_race_id_count
                                )):
  calendar_df_stage_races_race_id_extract = calendar_df_stage_races_race_id_extract+1
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?r='+str(calendar_df_stage_races_race_id[calendar_df_stage_races_race_id_extract])+'&y='+str(2023)+'&k=2'
  # url = 'https://firstcycling.com/race.php?r='+str(calendar_df_stage_races_race_id[calendar_df_stage_races_race_id_count])+'&y='+str(season)+'&k=2'
  # url = 'https://firstcycling.com/race.php?r=17&y=2023&k=2'
  calendar_stage_race_stages_df_meta = requests.get(url)
  calendar_stage_race_stages_df_meta_soup = BeautifulSoup(calendar_stage_race_stages_df_meta.content, "html.parser")
  calendar_stage_race_stages_df_meta_soup_part2 = calendar_stage_race_stages_df_meta_soup.find_all('tbody')[0]

  for row in calendar_stage_race_stages_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
        season = str(season)
        first_cycling_race_id = calendar_df_stage_races_race_id[calendar_df_stage_races_race_id_extract]
        stage_number = np.where(columns[0].text == 'Pl.','00',columns[0].text)
        stage_profile_category = str(columns[1]).split('src="img/mini/')[-1].split('.svg')[0]
        # date_month_test = str(columns[2])
        # date_month_test = np.where(str(columns[2].text).find('Jan'),'Found','Not Found')
        # date_month = np.where(str(columns[2].text).find('Jan'),'01',
                              # np.where(str(columns[2].text).find('Feb'),'02',
                              #          np.where(str(columns[2].text).find('Mar'),'03',
                              #                   np.where(str(columns[2].text).find('Apr'),'04',
                              #                            np.where(str(columns[2].text).find('May'),'05',
                              #                                     np.where(str(columns[2].text).find('Jun'),'06',
                              #                                              np.where(str(columns[2].text).find('Jul'),'07',
                              #                                                       np.where(str(columns[2].text).find('Aug'),'08',
                              #                                                                np.where(str(columns[2].text).find('Sep'),'09',
                              #                                                                         np.where(str(columns[2].text).find('Oct'),'10',
                              #                                                                                  np.where(str(columns[2].text).find('Nov'),'11',np.where(str(columns[2].text).find('Dec'),'12',
                              #                                                                                                                                          ""))))))))))))



        # date = str(season)+'/'+str(date_month)+'/'+str(np.where(int(str(columns[2].text).split('.')[0]) < 10,'0'+str(columns[2].text).split('.')[0],str(columns[2].text).split('.')[0]))
        distance = columns[3].text
        route = columns[4].text
        # start_town = columns[4].text
        # finish_town = columns[4].text
        # stage_winner = columns[5]
        # test0 = columns[0]
        # test1 = columns[1]
        # test2 = columns[2]
        # test3 = columns[3]
        # test4 = columns[4]
        # test5 = columns[5]
        # test6 = columns[6]
        # test7 = columns[7]

        calendar_df_stage_races_stages_df = calendar_df_stage_races_stages_df.append({
            'season':season
            ,'first_cycling_race_id':first_cycling_race_id
            ,'stage_number':stage_number
            # ,'date':date
            ,'stage_profile_category':stage_profile_category
            ,'distance':distance
            ,'route':route
            # ,'date_month':date_month
            # ,'date_month_test':date_month_test
            # ,'test0':test0
            # ,'test1':test1
            # ,'test2':test2
            # ,'test3':test3
            # ,'test4':test4
            # ,'test5':test5
            # ,'test6':test6
            # ,'test7':test7
        }, ignore_index=True)

calendar_df_stage_races_stages_df = calendar_df_stage_races_stages_df.loc[calendar_df_stage_races_stages_df['stage_number']!= '']
# calendar_df_stage_races_stages_df
