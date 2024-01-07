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

##### Race Results Stages #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'Stages']['file_name'].to_list()

raceresults_stage_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'Stages']['file_name'].nunique()

raceresults_stage_count = 0

season = []
first_cycling_race_id = []
stage_number = []
stage_position = []
first_cycling_rider_id = []
stage_time_raw = []


for raceresults_stage_count in tqdm(range(0,
                                # 10
                                raceresults_stage_count_limit
                                )):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            season.append(str(cci_file_name_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            first_cycling_race_id.append(str(cci_file_name_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            stage_number_raw = int((cci_file_name_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            # stage_number.append(str(cci_file_name_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            try:
                stage_position.append(columns[0].text)
            except:
                stage_position.append('Error')
            try:
                first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                first_cycling_rider_id.append('error')
            try:
                stage_time_raw.append(columns[6].text)
            except:
                stage_time_raw.append('error')
            
            raceresults_stage_df = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'stage_position':stage_position
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'stage_time_raw':stage_time_raw
            })
raceresults_stage_count = raceresults_stage_count + 1

# raceresult_stage_count_limit

raceresults_stage_df.to_csv(setwd+'raceresults_stage_df.csv',index=False)
raceresults_stage_df

##### Race Results GC #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'GC']['file_name'].to_list()

raceresult_gc_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'GC']['file_name'].nunique()

raceresult_gc_count = 0

season = []
first_cycling_race_id = []
gc_position = []
first_cycling_rider_id = []
gc_time_raw = []
stage_number = []

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
                gc_time_raw.append(columns[6].text)
            except: gc_time_raw.append('Error')
            stage_number.append('GC')

            raceresults_gc_df = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'gc_position':gc_position
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'gc_time_raw':gc_time_raw
            })
    raceresult_gc_count = raceresult_gc_count + 1

raceresults_gc_df.to_csv(setwd+'raceresults_gc_df.csv',index=False)

##### Unioning RaceResults_Stage_df and RaceResults_GC_df #####

# raceresults_stage_df = pd.read_csv(setwd+'raceresults_stage_df.csv')
raceresults_stage_df['stage_number'] = np.where(raceresults_stage_df['stage_number'] < 10,'0'+(raceresults_stage_df['stage_number']).astype(str),raceresults_stage_df['stage_number'].astype(str))
raceresults_stage_df['gc_position'] = 'to do'
raceresults_stage_df['gc_time_raw'] = 'to do'

raceresults_stage_df = raceresults_stage_df[['season','first_cycling_race_id','stage_number','gc_position','first_cycling_rider_id','gc_time_raw','stage_position','stage_time_raw']]

# raceresults_gc_df = pd.read_csv(setwd+'raceresults_gc_df.csv')
raceresults_gc_df['stage_position'] = raceresults_gc_df['gc_position']
raceresults_gc_df['stage_time_raw'] = raceresults_gc_df['gc_time_raw']

raceresults_gc_df = raceresults_gc_df[['season','first_cycling_race_id','stage_number','gc_position','first_cycling_rider_id','gc_time_raw','stage_position','stage_time_raw']]

raceresults_all_df = pd.concat([raceresults_gc_df,raceresults_stage_df])

raceresults_all_df.to_csv(setwd+'raceresults_all_df.csv',index=False)


# raceresults_stage_df
# raceresults_gc_df
# raceresults_all_df

raceresults_all_df['season'] = raceresults_all_df['season'].astype(str)
raceresults_all_df['first_cycling_race_id'] = raceresults_all_df['first_cycling_race_id'].astype(str)
raceresults_all_df['first_cycling_rider_id'] = raceresults_all_df['first_cycling_rider_id'].astype(str)
raceresults_all_df['stage_number'] = raceresults_all_df['stage_number'].astype(str)
# raceresults_all_df['concat'] = raceresults_all_df['season'].astype(str)+raceresults_all_df['first_cycling_race_id'].astype(str)+raceresults_all_df['stage_number'].astype(str)

startlists_df = pd.read_csv(setwd+'startlist_df.csv')
startlists_df['season'] = startlists_df['season'].astype(str)
startlists_df['first_cycling_race_id'] = startlists_df['first_cycling_race_id'].astype(str)
startlists_df['first_cycling_rider_id'] = startlists_df['first_cycling_rider_id'].astype(str)
startlists_df['first_cycling_team_id'] = startlists_df['first_cycling_team_id'].astype(str)

calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
calendar_df['season'] = calendar_df['season'].astype(str)
calendar_df['first_cycling_race_id'] = calendar_df['first_cycling_race_id'].astype(str)
# calendar_df['concat'] = calendar_df['season'].astype(str)+calendar_df['first_cycling_race_id'].astype(str)+calendar_df['stage_number'].astype(str)

raceresults_df = raceresults_all_df.merge(startlists_df, on = ['season','first_cycling_race_id','first_cycling_rider_id'])
raceresults_df = raceresults_all_df.merge(calendar_df, on = ['season','first_cycling_race_id','stage_number'])
raceresults_df.to_csv(setwd+'cyclingchaos_raceresults_df_master_test.csv',index=False)

raceresults_df
# raceresults_all_df
# calendar_df
