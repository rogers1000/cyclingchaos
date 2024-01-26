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

##### Trying to create a list of races that needs to be ingested


# set season that you want to ingest
season = 2024

# load calendar data

first_cycling_calendar_stages_list = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

# filter to only show stages within stage races

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['stage_race_boolean'] == 'Stage Race']

##### 2024 DATA INGEST BOTCH JOB

# create column for today's date

first_cycling_calendar_stages_list['today_date'] = datetime.today()

# create new column to make start_date compatible for comparing to date fields
# if statement for if start_date is smaller than today's date then ingest file.
# filter calendar dataframe to only include 2024 data
# filter calendar dataframe to only include historic races

## Should look into ingestion field to work out if data has been ingested before.
## Probably need it for all code and do a complete re-design. 



first_cycling_calendar_stages_list['start_date_date'] = pd.to_datetime(first_cycling_calendar_stages_list['start_date'],infer_datetime_format=True)

first_cycling_calendar_stages_list['start_date_filter'] = np.where(first_cycling_calendar_stages_list['start_date_date'] < first_cycling_calendar_stages_list['today_date'],
                                                                   "Ingest","Wait")

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['season'] == season]

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['start_date_filter'] == 'Ingest']

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.drop(['start_date_date','today_date'],axis=1)

##### END OF BOTCH JOB

# read in results file
# create unique ID for season+race_id
# create list of unique season+race_id as a list

race_results_df_master = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master.csv')

race_results_df_master['concat'] = race_results_df_master['season'].astype(str)+'_'+race_results_df_master['first_cycling_race_id'].astype(str)

race_results_df_master_list = race_results_df_master['concat'].drop_duplicates().to_list()

# first_cycling_calendar_stages_list 

# race_results_df_master_list

# read in calendar data
# filter to just Stage Races
# create colum for unique ID for season+race_id+stage_number

first_cycling_calendar_stages_list = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['stage_race_boolean'] == 'Stage Race']

first_cycling_calendar_stages_list['season_race_id_stagenumber'] = first_cycling_calendar_stages_list['season'].astype(str)+first_cycling_calendar_stages_list['first_cycling_race_id'].astype(str)+first_cycling_calendar_stages_list['stage_number'].astype(str)

##### 2024 DATA INGEST BOTCH JOB


# create new column to make start_date compatible for comparing to date fields
# if statement for if start_date is smaller than today's date then ingest file.
# filter calendar dataframe to only include 2024 data
# filter calendar dataframe to only include historic races

## Should look into ingestion field to work out if data has been ingested before.
## Probably need it for all code and do a complete re-design. 

first_cycling_calendar_stages_list['today_date'] = datetime.today()

first_cycling_calendar_stages_list['start_date_date'] = pd.to_datetime(first_cycling_calendar_stages_list['start_date'],infer_datetime_format=True)

first_cycling_calendar_stages_list['start_date_filter'] = np.where(first_cycling_calendar_stages_list['start_date_date'] < first_cycling_calendar_stages_list['today_date'],
                                                                   "Ingest","Wait")

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['season'] == 2024]

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['start_date_filter'] == 'Ingest']

##### END OF 2024 BOTCH JOB

first_cycling_calendar_stages_list['stage_number'] = first_cycling_calendar_stages_list['stage_number'].astype(int)

first_cycling_calendar_stages_list

# read in calendar data
# filter to Stage Races
# create colum for unique ID for season+race_id+stage_number

first_cycling_calendar_stages_list = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['stage_race_boolean'] == 'Stage Race']

first_cycling_calendar_stages_list['season_race_id_stagenumber'] = first_cycling_calendar_stages_list['season'].astype(str)+first_cycling_calendar_stages_list['first_cycling_race_id'].astype(str)+first_cycling_calendar_stages_list['stage_number'].astype(str)

##### 2024 DATA INGEST BOTCH JOB

# create new column to make start_date compatible for comparing to date fields
# if statement for if start_date is smaller than today's date then ingest file.
# filter calendar dataframe to only include 2024 data
# filter calendar dataframe to only include historic races

## Should look into ingestion field to work out if data has been ingested before.
## Probably need it for all code and do a complete re-design. 

first_cycling_calendar_stages_list['today_date'] = datetime.today()

first_cycling_calendar_stages_list['start_date_date'] = pd.to_datetime(first_cycling_calendar_stages_list['start_date'],infer_datetime_format=True)

first_cycling_calendar_stages_list['start_date_filter'] = np.where(first_cycling_calendar_stages_list['start_date_date'] < first_cycling_calendar_stages_list['today_date'],
                                                                   "Ingest","Wait")

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['season'] == 2024]

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['start_date_filter'] == 'Ingest']

##### END OF BOTCH JOB

# change stage_number type `int`

first_cycling_calendar_stages_list['stage_number'] = first_cycling_calendar_stages_list['stage_number'].astype(int)

# count of unique season,race_id, stage_number

first_cycling_calendar_stages_count_limit = first_cycling_calendar_stages_list['season_race_id_stagenumber'].nunique()

# create lists for the dataframe transform for season, race_id, stage_number

first_cycling_calendar_stages_count_season = first_cycling_calendar_stages_list['season'].to_list()
first_cycling_calendar_stages_count_race_id = first_cycling_calendar_stages_list['first_cycling_race_id'].to_list()
first_cycling_calendar_stages_count_stagenumber = first_cycling_calendar_stages_list['stage_number'].to_list()

# create empty lists for fields required for dataframes

season = []
first_cycling_race_id = []
stage = []

# ingestion count
calendar_df_stage_races_race_id_extract = 0

# create lists of ingestion master to append with new ingestions

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# ingestion loop

for calendar_df_stage_races_race_id_extract in tqdm(range(0,
                                # 1
                                first_cycling_calendar_stages_count_limit
                                )):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
  time.sleep(5)
# base website + race_id + season + stage_number. 'e=' means stage number for race
  url = 'https://firstcycling.com/race.php?r='+str(first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract])+'&y='+str(first_cycling_calendar_stages_count_season[calendar_df_stage_races_race_id_extract])+'&e='+str(first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract])
# list for season
# list for race_id
# list for stage_nnumber
  season = first_cycling_calendar_stages_count_season[calendar_df_stage_races_race_id_extract]
  race_id = first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract]
  stage_number = first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract]
# beautiful soup to ingest html file
  calendar_stage_race_stages_df_meta = requests.get(url)
  raceresults_stages_meta = requests.get(url)
  raceresults_stages_meta_soup = BeautifulSoup(raceresults_stages_meta.content, "html.parser")
  raceresults_stages_meta_soup_str = str(raceresults_stages_meta_soup)
# create file_name and write to disk
  file_name = 'cycling_chaos_code'+'_'+'raceresults'+'_'+'stages'+'_'+str(season)+'_'+str(first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract])+'_'+str(first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract])+'.txt'
  with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
    writefile.write(raceresults_stages_meta_soup_str)
    writefile.close()
# add ingestions to ingestion tracker and write to disk
    cci_output.append('raceresults')
    cci_output_details.append('Stages')
    cci_file_name.append(file_name)

    print('Ingested #'+str(calendar_df_stage_races_race_id_extract+1)+' '+file_name)

calendar_df_stage_races_race_id_extract = calendar_df_stage_races_race_id_extract + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
