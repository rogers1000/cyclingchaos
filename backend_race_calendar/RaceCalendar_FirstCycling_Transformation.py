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

# setwd = WorkingDirectory

##### Transforming Calendar Ingest #####

# Making a list of files needing to be transformed

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name'].nunique()

calendar_ingestion_count = 0

# print(cci_file_name_list[calendar_ingestion_count])

first_cycling_race_id_list = []
year = []
gender = []
category = []
calendar_ingestion_count_str = []
first_cycling_race_id = []
race_name = []
race_nationality = []
uci_race_classification = []
stage_race_boolean = []
start_date = []
end_date = []




for calendar_ingestion_count in range(0,22):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[-1]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            year.append(str(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name']).split('_')[5])
            gender.append(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['output_details'][calendar_ingestion_count])
            category.append('Road')
            calendar_ingestion_count_str.append(str(calendar_ingestion_count))
            first_cycling_race_id.append(str(columns[2].find_all('a')).split('r=')[1].split('&amp')[0])
            # race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0])
            try:
                race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0].split('amp;')[0]+str(columns[2].find_all('a')).split('title="')[1].split('">')[0].split('amp;')[-1])
            except:
                race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0])
            race_nationality.append(str(columns[2].find_all("span")).split("flag-")[1].split('"><')[0].upper())
            uci_race_classification.append(columns[1].text)
            stage_race_boolean.append(np.where(columns[1].text.startswith('2'),"Stage Race","One Day"))
            # start_date.append(year[-1])
            start_date.append(year[-1]+'/'+columns[0].text.split('-')[0].split('.')[-1]+'/'+columns[0].text.split('-')[0].split('.')[0])
            end_date.append(year[-1]+'/'+columns[0].text.split('-')[-1].split('.')[-1]+'/'+columns[0].text.split('-')[-1].split('.')[0])
            # test.append(calendar_ingestion_count)

            road_calendar_df = pd.DataFrame({
                'season':year
                ,'gender':gender
                ,'category':category
                ,'first_cycling_race_id':first_cycling_race_id
                ,'race_name':race_name
                ,'race_nationality':race_nationality
                ,'uci_race_classification':uci_race_classification
                ,'stage_race_boolean':stage_race_boolean
                ,'start_date':start_date
                ,'end_date':end_date
                })
            
    calendar_ingestion_count = calendar_ingestion_count + 1

road_calendar_df = road_calendar_df.drop_duplicates(subset=['season','first_cycling_race_id'])

road_calendar_df.to_csv(setwd+'first_cycling_calendar_df_master.csv', index=False)
road_calendar_df            
# print(road_calendar_df['season'])
# print(calendar_ingestion_count)

##### Stage Race Stages Profiles #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profiles']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profiles']['file_name'].nunique()

calendar_stage_profiles_ingestion_count = 0

# print(cci_file_name_list)

season = []
first_cycling_race_id = []
stage_number = []
stage_profile_category_first_cycling = []
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
            stage_profile_category_first_cycling.append(str(columns[1]).split('src="img/mini/')[-1].split('.svg')[0])
            distance.append(columns[3].text)
            route.append(columns[4].text)

            road_calendar_stage_profiles = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling
                ,'distance':distance
                ,'route':route
            })
    
    calendar_stage_profiles_ingestion_count = calendar_stage_profiles_ingestion_count + 1

road_calendar_stage_profiles.to_csv(setwd+'road_calendar_stage_profiles.csv',index=False)

##### Trying to get Route & Distance for One Day Races #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profiles']['file_name'].nunique()

calendar_oneday_profiles_ingestion_count = 0

for calendar_oneday_profiles_ingestion_count in tqdm(range(0,
                                                          # 1
                                                          calendar_ingestion_count_limit
                                                          )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_oneday_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    season.append(cci_file_name_list[calendar_stage_profiles_ingestion_count].split('_')[6])
    first_cycling_race_id.append(cci_file_name_list[calendar_oneday_profiles_ingestion_count].split('_')[7].split('.')[0])
    stage_number.append('GC')
    try:
        stage_profile_category_first_cycling.append(file_soup.find(title='Race profile icon').get('src').split('mini/')[-1].split('.')[0])
    except:
        stage_profile_category_first_cycling.append('Error')
    distance.append('')
    route.append('')

    road_calendar_stage_profiles = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling
                ,'distance':distance
                ,'route':route
            })

    calendar_oneday_profiles_ingestion_count = calendar_oneday_profiles_ingestion_count + 1

road_calendar_stage_profiles = road_calendar_stage_profiles.drop_duplicates(subset=['first_cycling_race_id'])

# cci_file_name_list

stage_profile_category_first_cycling = ['Flatt','Tempo','Bakketempo','Fjell-MF','Fjell','Smaakupert-MF',
                                               'Smaakupert','Brosten','Lagtempo','Ukjent','<td></td>']

stage_profile_category_mapping_eng = ['Flat','Flat ITT','Mountain ITT','Mountain MTF','Mountain','Hilly MTF',
                                      'Hilly','Cobbles','TTT','Unknown','Unknown']

stage_profile_category_mapping = pd.DataFrame({'stage_profile_category_first_cycling':stage_profile_category_first_cycling,
                                               'stage_profile_category_mapping_eng':stage_profile_category_mapping_eng})

# stage_profile_category_mapping

road_calendar_stage_profiles = road_calendar_stage_profiles.merge(stage_profile_category_mapping, on = 'stage_profile_category_first_cycling')

road_calendar_stage_profiles = road_calendar_stage_profiles.drop(['stage_profile_category_first_cycling'],axis=1)  

road_calendar_stage_profiles 

# road_calendar_oneday_profiles2 = pd.read_csv(setwd+'road_calendar_oneday_profiles.csv')
road_calendar_stage_profiles['season'] = road_calendar_stage_profiles['season'].astype(str)
road_calendar_stage_profiles['first_cycling_race_id'] = road_calendar_stage_profiles['first_cycling_race_id'].astype(str)

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
first_cycling_calendar_df['season'] = first_cycling_calendar_df['season'].astype(str)
first_cycling_calendar_df['first_cycling_race_id'] = first_cycling_calendar_df['first_cycling_race_id'].astype(str)

first_cycling_calendar_df = first_cycling_calendar_df.merge(road_calendar_stage_profiles, on = ['season','first_cycling_race_id'])

first_cycling_calendar_df.to_csv(setwd+'first_cycling_calendar_df_master.csv',index=False)

first_cycling_calendar_df
