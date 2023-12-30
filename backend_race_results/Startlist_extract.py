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

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
# race_id_list = first_cycling_calendar_df['first_cycling_race_id']
race_id_list = first_cycling_calendar_df['first_cycling_race_id'].drop_duplicates().to_list()

race_id_list
race_count_limit = first_cycling_calendar_df['first_cycling_race_id'].nunique()

season = 2023
calendar_df_stage_races_race_id_extract = 0
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

race_id_extract_count = 0

for race_id_extract_count in tqdm(range(0,
                                        #   10
                                        race_count_limit
                                        )):
    time.sleep(5)
    url = 'https://firstcycling.com/race.php?r='+str(race_id_list[race_id_extract_count])+'&y='+str(season)+'&k=8'
    raceresults_gc_meta = requests.get(url)
    raceresults_gc_meta_soup = BeautifulSoup(raceresults_gc_meta.content, "html.parser")
    raceresults_gc_meta_soup_str = str(raceresults_gc_meta_soup)
    file_name = 'cycling_chaos_code'+'_'+'startlist'+'_'+'all'+'_'+str(season)+'_'+str(race_id_list[race_id_extract_count])+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(raceresults_gc_meta_soup_str)
        writefile.close()
    cci_output.append('startlist')
    cci_output_details.append('all')
    cci_file_name.append(file_name)

    print('Ingested #'+str(race_id_extract_count+1)+' '+file_name)

    race_id_extract_count = race_id_extract_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
