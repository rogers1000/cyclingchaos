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

first_cycling_calendar_stages_list = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

first_cycling_calendar_stages_list = first_cycling_calendar_stages_list.loc[first_cycling_calendar_stages_list['stage_race_boolean'] == 'Stage Race']

first_cycling_calendar_stages_list['season_race_id_stagenumber'] = first_cycling_calendar_stages_list['season'].astype(str)+first_cycling_calendar_stages_list['first_cycling_race_id'].astype(str)+first_cycling_calendar_stages_list['stage_number'].astype(str)

# first_cycling_calendar_stages

first_cycling_calendar_stages_count_limit = first_cycling_calendar_stages_list['season_race_id_stagenumber'].nunique()

first_cycling_calendar_stages_count_season = first_cycling_calendar_stages_list['season'].to_list()
first_cycling_calendar_stages_count_race_id = first_cycling_calendar_stages_list['first_cycling_race_id'].to_list()
first_cycling_calendar_stages_count_stagenumber = first_cycling_calendar_stages_list['stage_number'].to_list()

season = []
first_cycling_race_id = []
stage = []
calendar_df_stage_races_race_id_extract = 0

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

for calendar_df_stage_races_race_id_extract in tqdm(range(0,
                                # 10
                                first_cycling_calendar_stages_count_limit
                                )):
  time.sleep(5)
  url = 'https://firstcycling.com/race.php?r='+str(first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract])+'&y='+str(first_cycling_calendar_stages_count_season[calendar_df_stage_races_race_id_extract])+'&e='+str(first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract])
  season = first_cycling_calendar_stages_count_season[calendar_df_stage_races_race_id_extract]
  race_id = first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract]
  stage_number = first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract]
  calendar_stage_race_stages_df_meta = requests.get(url)
  raceresults_stages_meta = requests.get(url)
  raceresults_stages_meta_soup = BeautifulSoup(raceresults_stages_meta.content, "html.parser")
  raceresults_stages_meta_soup_str = str(raceresults_stages_meta_soup)
  file_name = 'cycling_chaos_code'+'_'+'raceresults'+'_'+'stages'+'_'+str(season)+'_'+str(first_cycling_calendar_stages_count_race_id[calendar_df_stage_races_race_id_extract])+'_'+str(first_cycling_calendar_stages_count_stagenumber[calendar_df_stage_races_race_id_extract])+'.txt'
  with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
    # with open(r'/Users/zacrogers/Documents/cycling_chaos/python_code/calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
    writefile.write(raceresults_stages_meta_soup_str)
    writefile.close()
    cci_output.append('raceresults')
    cci_output_details.append('Stages')
    cci_file_name.append(file_name)

    print('Ingested #'+str(calendar_df_stage_races_race_id_extract+1)+' '+file_name)

calendar_df_stage_races_race_id_extract = calendar_df_stage_races_race_id_extract + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
