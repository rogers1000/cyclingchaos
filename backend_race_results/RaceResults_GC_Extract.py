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

latest_ingest_date = '18/02/2024'

##### One Day / GC Results #####


# set season that you want to ingest
season = 2024

# load calendar data

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

##### 2024 DATA INGEST BOTCH JOB

# create column for today's date

first_cycling_calendar_df['today_date'] = datetime.today()

# create new column to make start_date compatible for comparing to date fields
# if statement for if start_date is smaller than today's date then ingest file.
# filter calendar dataframe to only include 2024 data
# filter calendar dataframe to only include historic races

## Should look into ingestion field to work out if data has been ingested before.
## Probably need it for all code and do a complete re-design. 

first_cycling_calendar_df['last_ingest_date'] = pd.to_datetime(latest_ingest_date, infer_datetime_format=True)

first_cycling_calendar_df['end_date_date'] = pd.to_datetime(first_cycling_calendar_df['end_date'],infer_datetime_format=True)

first_cycling_calendar_df['end_date_filter'] = np.where(first_cycling_calendar_df['end_date_date'] < first_cycling_calendar_df['today_date'],
                                                                   "Ingest","Wait")

first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['season'] == season]

first_cycling_calendar_df = first_cycling_calendar_df.loc[first_cycling_calendar_df['end_date_filter'] == 'Ingest']

first_cycling_calendar_df['end_date_filter_ingested'] = np.where(latest_ingest_date < first_cycling_calendar_df['end_date_date'],
                                                                   "Ingest","Ingested")

first_cycling_calendar_df

##### END OF BOTCH JOB

# create list of first_cycling_race_id that need to be ingested
# count how many races need to be ingested

race_id_list = first_cycling_calendar_df['first_cycling_race_id'].drop_duplicates().to_list()
# race_id_list = ['1172']
race_count_limit = first_cycling_calendar_df['first_cycling_race_id'].nunique()
calendar_df_stage_races_race_id_extract = 0
race_id_extract_count = 0

# make list of ingestion tracker to append during ingestions

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# ingestion loop

for race_id_extract_count in tqdm(range(0,
                                        #   1
                                        race_count_limit
                                        )):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
# base website + race_id and season to get gc results
    url = 'https://firstcycling.com/race.php?r='+str(race_id_list[race_id_extract_count])+'&y='+str(season)
# beautiful soup to open html file
    raceresults_gc_meta = requests.get(url)
    raceresults_gc_meta_soup = BeautifulSoup(raceresults_gc_meta.content, "html.parser")
    raceresults_gc_meta_soup_str = str(raceresults_gc_meta_soup)
# write file name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'raceresults'+'_'+'gc'+'_'+str(season)+'_'+str(race_id_list[race_id_extract_count])+'.txt'
    with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(raceresults_gc_meta_soup_str)
        writefile.close()
# append ingestion tracker list and write to disk
    cci_output.append('raceresults')
    cci_output_details.append('gc')
    cci_file_name.append(file_name)

    print('Ingested #'+str(race_id_extract_count+1)+' '+file_name)

    race_id_extract_count = race_id_extract_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
