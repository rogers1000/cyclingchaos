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

#setwd = Working Directory

# Logically need to create basic calendar within this file otherwise its transforming calendar
# then transforming this file
# then re-transforming calendar

##### Stage Race Stages Profiles #####

# Select season that you want to extract

season = 2024

# Read calendar tracker and filter to just the season you want to ingest.
# Filter to stage races 
first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['season'] == season]
first_cycling_calendar_df_stages = first_cycling_calendar_df.loc[first_cycling_calendar_df['stage_race_boolean'] == 'Stage Race']

# create list of first_cycling_race_ids
first_cycling_stage_races_race_id_list = first_cycling_calendar_df_stages['first_cycling_race_id'].to_list()

# Botch job that is commented out if I want to just ingestion selected races
## first_cycling_stage_races_race_id_list = ['9080']

# Count number of stage_races that are currently ingested.
calendar_df_stage_races_race_id_count = first_cycling_calendar_df_stages['first_cycling_race_id'].nunique()

calendar_df_stage_races_race_id_extract = 0

# read ingestion file so I can add to the tracker once I have done the ingestions
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# ingestion loop

for calendar_df_stage_races_race_id_extract in tqdm(range(0,
                                                        #   1
                                                          calendar_df_stage_races_race_id_count
                                )):
# # get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
# url = base website + first_cycling_race_id. Set the season and 'K=2' means information page
    url = 'https://firstcycling.com/race.php?r='+str(first_cycling_stage_races_race_id_list[calendar_df_stage_races_race_id_extract])+'&y='+str(season)+'&k=2'
# beautiful soup to open html file
    calendar_stage_race_stages_df_meta = requests.get(url)
    calendar_stage_race_stages_df_meta_soup = BeautifulSoup(calendar_stage_race_stages_df_meta.content, "html.parser")
    calendar_stage_race_stages_df_meta_soup_str = str(calendar_stage_race_stages_df_meta_soup)
# create file name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'stage_profile'+'_'+str(season)+'_'+str(first_cycling_stage_races_race_id_list[calendar_df_stage_races_race_id_extract])+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(calendar_stage_race_stages_df_meta_soup_str)
        writefile.close()
# add new ingestion to ingestion tracker lists 
    cci_output.append('calendar')
    cci_output_details.append('stage_profile')
    cci_file_name.append(file_name)
# check ingestion is working

    print('Ingested '+file_name)

# re-make lists into dataframe, remove duplicates and write to disk

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})
cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()
cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)

##### One Day Profiles #####

# read calendar and filter to season and one day races
season = 2024
first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['season'] == season]
first_cycling_calendar_df_stages = first_cycling_calendar_df.loc[first_cycling_calendar_df['stage_race_boolean'] != 'Stage Race']

# create lists of the first_cycling_race_id for one day races within that season
first_cycling_oneday_races_race_id_list = first_cycling_calendar_df_stages['first_cycling_race_id'].to_list()

# count number of ingestions that need to happen
calendar_df_stage_races_race_id_count = first_cycling_calendar_df_stages['first_cycling_race_id'].nunique()
calendar_df_oneday_races_race_id_extract = 0

# make lists so I can append the ingestion tracker
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# ingestion loop

for calendar_df_oneday_races_race_id_extract in tqdm(range(0,
                                                        #   10
                                                          calendar_df_stage_races_race_id_count
                                )):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
# url = base website + first_cycling_race_id. Set the season and 'K=2' means information page
    url = 'https://firstcycling.com/race.php?r='+str(first_cycling_oneday_races_race_id_list[calendar_df_oneday_races_race_id_extract])+'&y='+str(season)+'&k=2'
# beautiful soup to open html file
    calendar_oneday_race_stages_df_meta = requests.get(url)
    calendar_oneday_race_stages_df_meta_soup = BeautifulSoup(calendar_oneday_race_stages_df_meta.content, "html.parser")
    calendar_oneday_race_stages_df_meta_soup_str = str(calendar_oneday_race_stages_df_meta_soup)
# create file_name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'oneday_profile'+'_'+str(season)+'_'+str(first_cycling_oneday_races_race_id_list[calendar_df_oneday_races_race_id_extract])+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
# with open(r'/Users/zacrogers/Documents/cycling_chaos/python_code/calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(calendar_oneday_race_stages_df_meta_soup_str)
        writefile.close()
# append the ingestion tracker lists and then re-make it a dataframe before writing to disk
    cci_output.append('calendar')
    cci_output_details.append('oneday_profiles')
    cci_file_name.append(file_name)

    print('Ingested '+file_name)

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
