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

# read in calendar df

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

# ##### 2024 DATA INGEST BOTCH JOB

# set season that you want to ingest
season = 2024

# create new column to make start_date compatible for comparing to date fields
# if statement for if start_date is smaller than today's date then ingest file.
# filter calendar dataframe to only include 2024 data
# filter calendar dataframe to only include historic races

## Should look into ingestion field to work out if data has been ingested before.
## Probably need it for all code and do a complete re-design. 

first_cycling_calendar_df['today_date'] = datetime.today()

first_cycling_calendar_df['start_date_date'] = pd.to_datetime(first_cycling_calendar_df['start_date'],infer_datetime_format=True)

first_cycling_calendar_df['start_date_filter'] = np.where(first_cycling_calendar_df['start_date_date'] < first_cycling_calendar_df['today_date'],
                                                                   "Ingest","Wait")

first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['season'] == season]

first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['start_date_filter'] == 'Ingest']

##### END OF BOTCH JOB

# create unique list of race_id 
race_id_list = first_cycling_calendar_df['first_cycling_race_id'].drop_duplicates().to_list()

# count of unique race_id
race_count_limit = first_cycling_calendar_df['first_cycling_race_id'].nunique()

season = 2024
# ingestion count
calendar_df_stage_races_race_id_extract = 0

# create lists for ingestion tracker so it can be appended with new ingestions
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

race_id_extract_count = 0

# ingestion loop

for race_id_extract_count in tqdm(range(0,
                                        #   10
                                        race_count_limit
                                        )):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
# url = base website + race_id + season. 'K=8' is start lists
    url = 'https://firstcycling.com/race.php?r='+str(race_id_list[race_id_extract_count])+'&y='+str(season)+'&k=8'
# beautiful soup to ingest html file
    raceresults_gc_meta = requests.get(url)
    raceresults_gc_meta_soup = BeautifulSoup(raceresults_gc_meta.content, "html.parser")
    raceresults_gc_meta_soup_str = str(raceresults_gc_meta_soup)
# create file_name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'startlist'+'_'+'all'+'_'+str(season)+'_'+str(race_id_list[race_id_extract_count])+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(raceresults_gc_meta_soup_str)
        writefile.close()
# append ingestion tracker lists, convert to dataframe and write to disk
    cci_output.append('startlist')
    cci_output_details.append('all')
    cci_file_name.append(file_name)

    print('Ingested #'+str(race_id_extract_count+1)+' '+file_name)

    race_id_extract_count = race_id_extract_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
