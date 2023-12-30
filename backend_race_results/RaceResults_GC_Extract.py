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

##### Race Results GC #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df4.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'GC']['file_name'].to_list()

raceresult_gc_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'GC']['file_name'].nunique()

raceresult_gc_count = 0

season = []
first_cycling_race_id = []
gc_position = []
first_cycling_rider_id = []
gc_time = []

for raceresult_gc_count in tqdm(range(0,
                                    #   10
                                        raceresult_gc_count_limit
                                      )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresult_gc_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            season.append(str(cci_file_name_list[raceresult_gc_count]).split('_')[5].split('.')[0])
            try:
                first_cycling_race_id.append(str(cci_file_name_list[raceresult_gc_count]).split('_')[6].split('.')[0])
            except: first_cycling_race_id.append('Error')
            try:
                gc_position.append(columns[0].text)
            except: gc_position.append('Error')
            try:
                first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except: first_cycling_rider_id.append('Error')
            try:
                gc_time.append(columns[6].text)
            except: gc_time.append('Error')

            raceresults_gc_df = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'gc_position':gc_position
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'gc_time':gc_time
            })
    raceresult_gc_count = raceresult_gc_count + 1

raceresults_gc_df.to_csv(setwd+'raceresults_gc_df.csv',index=False)
