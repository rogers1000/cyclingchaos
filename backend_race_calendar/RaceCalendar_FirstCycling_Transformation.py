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

##### Trying to get Route & Distance for One Day Races #####

# seeing what one day profiles need transforming from the ingestion tracker

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profile']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profile']['file_name'].nunique()

calendar_oneday_profiles_ingestion_count = 0

# creating empty lists for the dataframe

season_oneday = []
first_cycling_race_id_oneday = []
stage_number_oneday = []
stage_profile_category_first_cycling_oneday = []
distance_oneday = []
route_oneday = []
stage_profile_category_eng_oneday = []

# transformation loop

for calendar_oneday_profiles_ingestion_count in tqdm(range(0,
                                                          # 1
                                                          calendar_ingestion_count_limit
                                                          )):
# open html file using beautiful soup
    file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[calendar_oneday_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
# use file_name to work out season for one day races
# use file to work out first_cycling_race_id for one day races
    season_oneday.append(cci_file_name_list[calendar_oneday_profiles_ingestion_count].split('_')[6])
    first_cycling_race_id_oneday.append(cci_file_name_list[calendar_oneday_profiles_ingestion_count].split('_')[7].split('.')[0])
# all one day races are 'GC' results
    stage_number_oneday.append('GC')
# find the image for the race profile to work out the first cycling profile category for one day races
# sometimes the races won't be classifed yet
    try:
        stage_profile_category_first_cycling_oneday.append(file_soup.find(title='Race profile icon').get('src').split('mini/')[-1].split('.')[0])
    except:
        stage_profile_category_first_cycling_oneday.append('Error')
# append distance and route for one day races to show blank cells.
# this is as I've not worked out how to transform distance and route yet for one day races.
    distance_oneday.append('')
    route_oneday.append('')

# create dataframe with transformed data

    road_calendar_oneday_profiles = pd.DataFrame({
                'season':season_oneday
                ,'first_cycling_race_id':first_cycling_race_id_oneday
                ,'stage_number':stage_number_oneday
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling_oneday
                ,'distance':distance_oneday
                ,'route':route_oneday
            })

# continue transform loop and write to disk

    calendar_oneday_profiles_ingestion_count = calendar_oneday_profiles_ingestion_count + 1

    road_calendar_oneday_profiles.to_csv(setwd+'road_calendar_oneday_profiles.csv',index=False)

# transform stage profiles for stage races to match field type for one day races

# road_calendar_stage_profiles = pd.read_csv(setwd+'road_calendar_stage_profiles.csv')
road_calendar_stage_profiles['season'] = road_calendar_stage_profiles['season'].astype(str)
road_calendar_stage_profiles['first_cycling_race_id'] = road_calendar_stage_profiles['first_cycling_race_id'].astype(str)

# road_calendar_stage_profiles = road_calendar_stage_profiles.drop_duplicates(subset=['season','first_cycling_race_id','stage_number'])


# road_calendar_oneday_profiles

# cci_file_name_list

# read stage profiles for one day races and union to stage profiles for stage races

road_calendar_oneday_profiles = pd.read_csv(setwd+'road_calendar_oneday_profiles.csv')

road_calendar_oneday_profiles

road_calendar_profiles = pd.concat([road_calendar_stage_profiles,road_calendar_oneday_profiles])
road_calendar_profiles

# create mapping dataframe for first_cycling category name to English
# then join to main dataframe and write to disk

stage_profile_category_first_cycling = ['Flatt','Tempo','Bakketempo','Fjell-MF','Fjell','Smaakupert-MF',
                                               'Smaakupert','Brosten','Lagtempo','Ukjent','<td></td>']

stage_profile_category_mapping_eng = ['Flat','Flat ITT','Mountain ITT','Mountain MTF','Mountain','Hilly MTF',
                                      'Hilly','Cobbles','TTT','Unknown','Unknown']

stage_profile_category_mapping = pd.DataFrame({'stage_profile_category_first_cycling':stage_profile_category_first_cycling,
                                               'stage_profile':stage_profile_category_mapping_eng})

road_calendar_profiles = road_calendar_profiles.merge(stage_profile_category_mapping, on = 'stage_profile_category_first_cycling')
road_calendar_profiles = road_calendar_profiles.drop(['stage_profile_category_first_cycling'],axis=1)
# stage_profile_category_mapping

road_calendar_profiles.to_csv(setwd+'road_calendar_profiles.csv',index=False)

road_calendar_profiles.dtypes

# road_calendar_stage_profiles

# read calendar_df and stage_profiles files from disk and then merge
# then write to disk

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
# first_cycling_calendar_df['season'] = first_cycling_calendar_df['season'].astype(str)
# first_cycling_calendar_df['first_cycling_race_id'] = first_cycling_calendar_df['first_cycling_race_id'].astype(str)

road_calendar_profiles = pd.read_csv(setwd+'road_calendar_profiles.csv')

first_cycling_calendar_df = first_cycling_calendar_df.merge(road_calendar_profiles, on = ['season','first_cycling_race_id'])

first_cycling_calendar_df.to_csv(setwd+'first_cycling_calendar_df_master.csv',index=False)

first_cycling_calendar_df
