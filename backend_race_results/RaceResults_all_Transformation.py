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

##### Race Results Stages #####

# Reading in ingestion tracker master and creating lists to work out which files need to be transformed and the number of those files.

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'stages')] ['file_name'].to_list()
raceresults_stage_count_limit = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'stages')]['file_name'].nunique()

# file count

raceresults_stage_count = 0

# empty list which will form the dataframe

season = []
first_cycling_race_id =[]
stage_number = []
stage_position = []
first_cycling_rider_id = []
stage_time_raw = []

# transformation loop

for raceresults_stage_count in tqdm(range(0,
                                # 2
                                raceresults_stage_count_limit
                                )):
# open file from ingestion tracker and use beautiful soup to get html code.
# tbody[0] = Stage time data
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')
# get season data from the file name
# get first_cycling_race_id from the file name
# get the stage number from the file and transform to double digits
# get stage_position from column 1 of the table
# get first_cycling_rider_id from column 4 of the table. Could be column 3 if no uci date age on table
# get stage_time_raw from column 7 of the table, could be column 6 if no uci date age on table
        if(columns != []):
            season.append(str(cci_file_name_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            first_cycling_race_id.append(str(cci_file_name_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            stage_number_raw = int((cci_file_name_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            try:
                stage_position.append(columns[0].text)
            except:
                stage_position.append('Error')
            try:
                first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id.append(str(columns[2].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id.append('Error')
            try:
                stage_time_raw.append(columns[6].text)
            except:
                try:
                    stage_time_raw.append(columns[5].text)
                except:
                    stage_time_raw.append('Error')

# create dataframe and write file to disk
# restart loop
            
            raceresults_stage_df = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'stage_position':stage_position
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'stage_time_raw':stage_time_raw
            })
    raceresults_stage_df.to_csv(setwd+'raceresults_stage_df.csv',index=False)

raceresults_stage_count = raceresults_stage_count + 1



# raceresult_stage_count_limit

# raceresults_stage_df.to_csv(setwd+'raceresults_stage_df.csv',index=False)
# raceresults_stage_df


##### Race Results Stages - GC Time #####

# Reading in ingestion tracker master and creating lists to work out which files need to be transformed and the number of those files.

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_names_stages = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'stages')]

cci_file_names_stages = cci_file_names_stages.loc[~(cci_file_names_stages['file_name'] == 'cycling_chaos_code_raceresults_stages_2023_16_6.txt')]

# 'cycling_chaos_code_raceresults_stages_2023_16_6.txt'

cci_file_name_list = cci_file_names_stages['file_name'].to_list()
raceresults_stage_count_limit = cci_file_names_stages['file_name'].nunique()

# file count

raceresults_stage_gc_time_count = 0

# empty list which will form the dataframe

season = []
first_cycling_race_id =[]
stage_number = []
gc_position = []
first_cycling_rider_id = []
gc_time_raw = []

# transformation loop

for raceresults_stage_gc_time_count in tqdm(range(0,
                                # 2
                                raceresults_stage_count_limit
                                )):
# open file from ingestion tracker and use beautiful soup to get html code.
# tbody[1] = gc time data
# if no data, then it will skip the stage.
    print('calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count])
    try:
        file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        file_soup_part2 = file_soup.find_all('tbody')[1]
    except:
        raceresults_stage_gc_time_count = raceresults_stage_gc_time_count + 1
        file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        file_soup_part2 = file_soup.find_all('tbody')[1]
    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')
# get season data from the file name
# get first_cycling_race_id from the file name
# get the stage number from the file and transform to double digits
# get stage_position from column 1 of the table
# get first_cycling_rider_id from column 6 of the table. Could be column 5 if no uci date age on table
# get stage_time_raw from column 7 of the table, could be column 6 if no uci date age on table
        if(columns != []):
            season.append(str(cci_file_name_list[raceresults_stage_gc_time_count]).split('_')[5].split('.')[0])
            first_cycling_race_id.append(str(cci_file_name_list[raceresults_stage_gc_time_count]).split('_')[6].split('.')[0])
            stage_number_raw = int((cci_file_name_list[raceresults_stage_gc_time_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            try:
                gc_position.append(columns[0].text)
            except:
                gc_position.append('Error')
            try:
                first_cycling_rider_id.append(str(columns[5].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id.append('Error')
            try:
                gc_time_raw.append(columns[6].text)
            except:
                try:
                    gc_time_raw.append(columns[5].text)
                except:
                    gc_time_raw.append('Error')

# create dataframe and write file to disk
# restart loop
            
            raceresults_stage_df = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'gc_position':gc_position
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'gc_time_raw':gc_time_raw
            })
raceresults_stage_df.to_csv(setwd+'raceresults_stage_gc_df.csv',index=False)

raceresults_stage_gc_time_count = raceresults_stage_gc_time_count + 1

##### Race Results GC #####

# Get file name and transform loop count from the ingestion tracker master

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')



cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].to_list()

raceresult_gc_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

raceresult_gc_count = 0

# Create list for fields that dataframe will use.

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
# open file from ingestion tracker and use beautiful soup to get html code.
# tbody[0] = GC time data
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresult_gc_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]
# get season data from the file name
# get first_cycling_race_id from the file name
# create stage_number field which is called 'GC'
# get gc_position from column 1 of the table
# get first_cycling_rider_id from column 4 of the table. Could be column 3 if no uci date age on table
# get stage_time_raw from column 7 of the table, could be column 6 if no uci date age on table
    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            season.append(str(cci_file_name_list[raceresult_gc_count]).split('_')[5].split('.')[0])
            try:
                first_cycling_race_id.append(str(cci_file_name_list[raceresult_gc_count]).split('_')[6].split('.')[0])
            except:
                first_cycling_race_id.append('Error')
            try:
                gc_position.append(columns[0].text)
            except: gc_position.append('Error')
            try:
                first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id.append(str(columns[2].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id.append('Error')
            try:
                gc_time_raw.append(columns[6].text)
            except:
                try:
                    gc_time_raw.append(columns[5].text)
                except:
                    gc_time_raw.append('Error')
            stage_number.append('GC')
# Create Dataframe and restart the loop before writing to disk at the end.
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

# reading stage time on stage races data and transforming fields to correct type 

raceresults_stage_df = pd.read_csv(setwd+'raceresults_stage_df.csv')
raceresults_stage_df['season'] = raceresults_stage_df['season'].astype(str)
raceresults_stage_df['first_cycling_race_id'] = raceresults_stage_df['first_cycling_race_id'].astype(str)
# raceresults_stage_df['stage_number'] = raceresults_stage_df['stage_number'].astype(str)
raceresults_stage_df['stage_number'] = np.where(raceresults_stage_df['stage_number'] < 10,'0'+raceresults_stage_df['stage_number'].astype(str),raceresults_stage_df['stage_number'].astype(str))
raceresults_stage_df['first_cycling_rider_id'] = raceresults_stage_df['first_cycling_rider_id'].astype(str)

# meant to be looking at stage race gc time, but currently reads one day gc time

raceresults_stage_df_gc = pd.read_csv(setwd+'raceresults_stage_gc_df.csv')
raceresults_stage_df_gc['season'] = raceresults_stage_df_gc['season'].astype(str)
raceresults_stage_df_gc['first_cycling_race_id'] = raceresults_stage_df_gc['first_cycling_race_id'].astype(str)
# raceresults_stage_df_gc['stage_number'] = raceresults_stage_df_gc['stage_number'].astype(str)
raceresults_stage_df_gc['stage_number'] = np.where(raceresults_stage_df_gc['stage_number'] < 10,'0'+raceresults_stage_df_gc['stage_number'].astype(str),raceresults_stage_df_gc['stage_number'].astype(str))
raceresults_stage_df_gc['first_cycling_rider_id'] = raceresults_stage_df_gc['first_cycling_rider_id'].astype(str)
raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_gc, on = ['season','first_cycling_race_id','stage_number','first_cycling_rider_id'])


# creating fields for jersey data that is yet to be transformed
# raceresults_stage_df['gc_position'] = 'to do'
# raceresults_stage_df['gc_time_raw'] = 'to do'
raceresults_stage_df['youth_position'] = 'to do'
raceresults_stage_df['youth_time_raw'] = 'to do'
raceresults_stage_df['points_position'] = 'to do'
raceresults_stage_df['points_score_raw'] = 'to do'
raceresults_stage_df['kom_position'] = 'to do'
raceresults_stage_df['kom_score_raw'] = 'to do'
raceresults_stage_df['team_position'] = 'to do'
raceresults_stage_df['team_time_raw'] = 'to do'

# aligning columns for stage races

raceresults_stage_df = raceresults_stage_df[['season','first_cycling_race_id','stage_number','first_cycling_rider_id','gc_position','gc_time_raw','stage_position','stage_time_raw','youth_position','youth_time_raw','kom_position','kom_score_raw','team_position','team_time_raw']]

# reading file in for one day races and adds additional columns ahead of unioning tables. 

raceresults_gc_df = pd.read_csv(setwd+'raceresults_gc_df.csv')
raceresults_gc_df['stage_position'] = raceresults_gc_df['gc_position']
raceresults_gc_df['stage_time_raw'] = raceresults_gc_df['gc_time_raw']
raceresults_gc_df['youth_position'] = 'to do'
raceresults_gc_df['youth_time_raw'] = 'to do'
raceresults_gc_df['team_position'] = 'to do'
raceresults_gc_df['team_time_raw'] = 'to do'
raceresults_gc_df['kom_position'] = 'to do'
raceresults_gc_df['kom_score_raw'] = 'to do'
raceresults_gc_df['team_position'] = 'to do'
raceresults_gc_df['team_time_raw'] = 'to do'

raceresults_gc_df = raceresults_gc_df[['season','first_cycling_race_id','stage_number','first_cycling_rider_id','gc_position','gc_time_raw','stage_position','stage_time_raw','youth_position','youth_time_raw','kom_position','kom_score_raw','team_position','team_time_raw']]


# raceresults_gc_df = raceresults_gc_df.loc[raceresults_gc_df['gc_time_raw'] != 'Error']

# unions stage race and one day race data

raceresults_all_df = pd.concat([raceresults_gc_df,raceresults_stage_df])

# raceresults_all_df.to_csv(setwd+'raceresults_all_df.csv',index=False)


# raceresults_stage_df
# raceresults_stage_df_gc
# raceresults_gc_df
raceresults_all_df

# raceresults_stage_df.to_csv(setwd+'results_test.csv',index=False)

# converts fields to correct type

raceresults_all_df['season'] = raceresults_all_df['season'].astype(str)
raceresults_all_df['first_cycling_race_id'] = raceresults_all_df['first_cycling_race_id'].astype(str)
raceresults_all_df['first_cycling_rider_id'] = raceresults_all_df['first_cycling_rider_id'].astype(str)
raceresults_all_df['stage_number'] = raceresults_all_df['stage_number'].astype(str)

# reading in start list data
startlists_df = pd.read_csv(setwd+'startlist_df.csv')
startlists_df['season'] = startlists_df['season'].astype(str)
startlists_df['first_cycling_race_id'] = startlists_df['first_cycling_race_id'].astype(str)
startlists_df['first_cycling_rider_id'] = startlists_df['first_cycling_rider_id'].astype(str)
startlists_df['first_cycling_team_id'] = startlists_df['first_cycling_team_id'].astype(str)

# reading in calendar data
calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
calendar_df['season'] = calendar_df['season'].astype(str)
calendar_df['first_cycling_race_id'] = calendar_df['first_cycling_race_id'].astype(str)
calendar_df['stage_number'] = calendar_df['stage_number'].astype(str)


raceresults_df = raceresults_all_df

# merging in startlist data

raceresults_all_df = raceresults_all_df.merge(startlists_df, on = ['season','first_cycling_race_id','first_cycling_rider_id'])

raceresults_df = raceresults_all_df

# merging in calendar data

raceresults_df = raceresults_all_df.merge(calendar_df, on = ['season','first_cycling_race_id','stage_number'])

# creating errors dataframe and writing to disk option (normally commented out)
# raceresults_df_errors = raceresults_df.loc[raceresults_df['first_cycling_rider_id'] == 'Error']
# raceresults_df_errors.to_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv',index=False)

# removing errors and writing to disk
raceresults_df = raceresults_df.loc[raceresults_df['first_cycling_rider_id'] != 'Error']
raceresults_df.to_csv(setwd+'cyclingchaos_raceresults_df_master.csv',index=False)

raceresults_df
# startlists_df
# raceresults_all_df
# calendar_df
