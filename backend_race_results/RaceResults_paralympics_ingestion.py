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

# setwd = Working Directory

# make list of ingestion tracker to append during ingestions

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# bringing in list of urls to ingest

paralympics_calendar = pd.read_csv(setwd+'paralympics_calendar.csv')

paralympics_calendar_race_id_list = paralympics_calendar['paralympics_race_id'].to_list()

paralympics_calendar_race_id_list_limit = paralympics_calendar['paralympics_race_id'].nunique()

paralympics_calendar_race_id_list

ingestion_results_count = 0

# ingestion loop

for ingestion_results_count in tqdm(range(0,
                                        # 1
                                        paralympics_calendar_race_id_list_limit
                                        )):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
    url = 'https://www.paralympic.org/'+str(paralympics_calendar_race_id_list[ingestion_results_count])
# beautiful soup to open html file
    paralympics_results_meta = requests.get(url)
    paralympics_results_meta_soup = BeautifulSoup(paralympics_results_meta.content, "html.parser")
    paralympics_results_meta_soup_str = str(paralympics_results_meta_soup)
# write file name and write to disk
    race_id_file = paralympics_calendar_race_id_list[ingestion_results_count].replace('/','_')
    file_name = 'cycling_chaos_code'+'_'+'results'+'_'+'paralympics'+'_'+race_id_file+'.txt'
    with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(paralympics_results_meta_soup_str)
        writefile.close()
# append ingestion tracker list and write to disk
    cci_output.append('raceresults')
    cci_output_details.append('paralympics')
    cci_file_name.append(file_name)

ingestion_results_count = ingestion_results_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
