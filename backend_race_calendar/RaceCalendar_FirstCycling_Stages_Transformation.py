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

#setwd = WorkingDirectory

##### Stage Race Stages Profiles #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df4.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profiles']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profiles']['file_name'].nunique()

calendar_stage_profiles_ingestion_count = 0

# print(cci_file_name_list)

season = []
first_cycling_race_id = []
stage_number = []
stage_profile_category = []
distance = []
route = []
stage_profile_category_eng = []


for calendar_stage_profiles_ingestion_count in tqdm(range(0,
                                                        #   10
                                                          calendar_ingestion_count_limit
                                                          )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_stage_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            season.append(str(cci_file_name_list[calendar_stage_profiles_ingestion_count]).split('_')[6])
            first_cycling_race_id.append(str(cci_file_name_list[calendar_stage_profiles_ingestion_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(columns[0].text == 'Pl.','00',columns[0].text))
            stage_profile_category.append(str(columns[1]).split('src="img/mini/')[-1].split('.svg')[0])
            distance.append(columns[3].text)
            route.append(columns[4].text)

            road_calendar_stage_profiles = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category
                ,'distance':distance
                ,'route':route
            })
    
    calendar_stage_profiles_ingestion_count = calendar_stage_profiles_ingestion_count + 1

stage_profile_category_first_cycling = ['Flatt','Tempo','Bakketempo','Fjell-MF','Fjell','Smaakupert-MF',
                                               'Smaakupert','Brosten','Lagtempo','Ukjent','<td></td>']

stage_profile_category_mapping_eng = ['Flat','Flat ITT','Mountain ITT','Mountain MTF','Mountain','Hilly MTF',
                                      'Hilly','Cobbles','TTT','Unknown','Unknown']

stage_profile_category_mapping = pd.DataFrame({'stage_profile_category_first_cycling':stage_profile_category_first_cycling,
                                               'stage_profile_category_mapping_eng':stage_profile_category_mapping_eng})

# stage_profile_category_mapping

road_calendar_stage_profiles = road_calendar_stage_profiles.merge(stage_profile_category_mapping, on = 'stage_profile_category_first_cycling')

# road_calendar_stage_profiles = road_calendar_stage_profiles.drop(['stage_profile_category_first_cycling'],axis=1)  


road_calendar_stage_profiles

first_cycling_calendar_df = pd.read_csv(setwd+'calendar_ingestion_files/first_cycling_calendar_version_control/first_cycling_calendar_df.csv')

first_cycling_calendar_df['season'] = first_cycling_calendar_df['season'].astype(str)
first_cycling_calendar_df['first_cycling_race_id'] = first_cycling_calendar_df['first_cycling_race_id'].astype(str)

first_cycling_calendar_df2 = first_cycling_calendar_df.merge(road_calendar_stage_profiles, on = ['season','first_cycling_race_id'])

first_cycling_calendar_df2 = first_cycling_calendar_df2.loc[first_cycling_calendar_df2['stage_number']!= '']

# first_cycling_calendar_df2 = first_cycling_calendar_df2.drop_duplicates()

first_cycling_calendar_df2.to_csv(setwd+'first_cycling_calendar_df2.csv',index=False)

# first_cycling_calendar_df2

##### Trying to get Route & Distance for One Day Races #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df4.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].nunique()

calendar_stage_profiles_ingestion_count = 0

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df2.csv')

# print(cci_file_name_list)

season = first_cycling_calendar_df['season'].to_list()
first_cycling_race_id = first_cycling_calendar_df['first_cycling_race_id'].to_list()
stage_number = first_cycling_calendar_df['stage_number'].to_list()
stage_profile_category_first_cycling = first_cycling_calendar_df['stage_profile_category_first_cycling'].to_list()
distance = first_cycling_calendar_df['distance'].to_list()
route = first_cycling_calendar_df['route'].to_list()
# stage_profile_category_eng = first_cycling_calendar_df['stage_profile_category_eng'].to_list()

for calendar_stage_profiles_ingestion_count in tqdm(range(0,
                                                          1
                                                        #   calendar_ingestion_count_limit
                                                          )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[0], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    season.append(cci_file_name_list[calendar_stage_profiles_ingestion_count].split('_')[6])
    first_cycling_race_id.append(cci_file_name_list[calendar_stage_profiles_ingestion_count].split('_')[7].split('.')[0])
    stage_number.append(1)
    try:
        stage_profile_category_first_cycling.append(file_soup.find(title='Race profile icon').get('src').split('mini/')[-1].split('.')[0])
    except:
        stage_profile_category_first_cycling.append('Error')
    distance.append('')
    route.append('')

    calendar_stage_profiles_ingestion_count = calendar_stage_profiles_ingestion_count + 1

##### One Day Race Profiles ######

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df4.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].nunique()

calendar_stage_profiles_ingestion_count = 0

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df2.csv')

# print(cci_file_name_list)

season = first_cycling_calendar_df['season'].to_list()
first_cycling_race_id = first_cycling_calendar_df['first_cycling_race_id'].to_list()
stage_number = first_cycling_calendar_df['stage_number'].to_list()
stage_profile_category_first_cycling = first_cycling_calendar_df['stage_profile_category_first_cycling'].to_list()
distance = first_cycling_calendar_df['distance'].to_list()
route = first_cycling_calendar_df['route'].to_list()
# stage_profile_category_eng = first_cycling_calendar_df['stage_profile_category_eng'].to_list()

for calendar_stage_profiles_ingestion_count in tqdm(range(0,
                                                          1
                                                        #   calendar_ingestion_count_limit
                                                          )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_stage_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    season.append(cci_file_name_list[calendar_stage_profiles_ingestion_count].split('_')[6])
    first_cycling_race_id.append(cci_file_name_list[calendar_stage_profiles_ingestion_count].split('_')[7].split('.')[0])
    stage_number.append(1)
    try:
        stage_profile_category_first_cycling.append(file_soup.find(title='Race profile icon').get('src').split('mini/')[-1].split('.')[0])
    except:
        stage_profile_category_first_cycling.append('Error')
    distance.append('')
    route.append('')

    calendar_stage_profiles_ingestion_count = calendar_stage_profiles_ingestion_count + 1


file_soup
stage_profile_category_first_cycling

road_calendar_oneday_profiles = pd.DataFrame({
    'season':season
    ,'first_cycling_race_id':first_cycling_race_id
    ,'stage_number':stage_number
#     # ,'date':date
    ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling
    ,'distance':distance
    ,'route':route
    })

stage_profile_category_first_cycling = ['Flatt','Tempo','Bakketempo','Fjell-MF','Fjell','Smaakupert-MF',
                                               'Smaakupert','Brosten','Lagtempo','Ukjent','<td></td>']

stage_profile_category_mapping_eng = ['Flat','Flat ITT','Mountain ITT','Mountain MTF','Mountain','Hilly MTF',
                                      'Hilly','Cobbles','TTT','Unknown','Unknown']

stage_profile_category_mapping = pd.DataFrame({'stage_profile_category_first_cycling':stage_profile_category_first_cycling,
                                               'stage_profile_category_mapping_eng':stage_profile_category_mapping_eng})

# # stage_profile_category_mapping

road_calendar_oneday_profiles = road_calendar_oneday_profiles.merge(stage_profile_category_mapping, on = 'stage_profile_category_first_cycling')

road_calendar_oneday_profiles = road_calendar_oneday_profiles.drop(['stage_profile_category_first_cycling'],axis=1)  

road_calendar_oneday_profiles

stage_profile_category_first_cycling

# road_calendar_oneday_profiles2 = pd.read_csv(setwd+'road_calendar_oneday_profiles.csv')
road_calendar_oneday_profiles2 = road_calendar_oneday_profiles
road_calendar_oneday_profiles2['season'] = road_calendar_oneday_profiles2['season'].astype(str)
road_calendar_oneday_profiles2['first_cycling_race_id'] = road_calendar_oneday_profiles2['first_cycling_race_id'].astype(str)

first_cycling_calendar_df2 = pd.read_csv(setwd+'calendar_ingestion_files/first_cycling_calendar_version_control/first_cycling_calendar_df.csv')
first_cycling_calendar_df2['season'] = first_cycling_calendar_df2['season'].astype(str)
first_cycling_calendar_df2['first_cycling_race_id'] = first_cycling_calendar_df2['first_cycling_race_id'].astype(str)

first_cycling_calendar_df2

road_calendar_oneday_profiles.dtypes

first_cycling_calendar_df3 = first_cycling_calendar_df2.merge(road_calendar_oneday_profiles2, on = ['season','first_cycling_race_id'])

# # first_cycling_calendar_df2 = first_cycling_calendar_df2.loc[first_cycling_calendar_df2['stage_number']!= '']

# # first_cycling_calendar_df2 = first_cycling_calendar_df2.drop_duplicates()

first_cycling_calendar_df3.to_csv(setwd+'first_cycling_calendar_df3.csv',index=False)

first_cycling_calendar_df3

