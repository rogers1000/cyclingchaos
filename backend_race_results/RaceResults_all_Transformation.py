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
    file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[raceresults_stage_count], 'r')
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
    # print('calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count])
    try:
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        file_soup_part2 = file_soup.find_all('tbody')[1]
    except:
        raceresults_stage_gc_time_count = raceresults_stage_gc_time_count + 1
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[raceresults_stage_gc_time_count], 'r')
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

# cci_file_name_list = ['cycling_chaos_code_raceresults_gc_2023_53.txt',
#                       'cycling_chaos_code_raceresults_gc_2024_53.txt',
#                       'cycling_chaos_code_raceresults_gc_2023_9181.txt',
#                       'cycling_chaos_code_raceresults_gc_2024_9181.txt',
#                       'cycling_chaos_code_raceresults_gc_2023_84.txt',
#                       'cycling_chaos_code_raceresults_gc_2024_84.txt',
#                       'cycling_chaos_code_raceresults_gc_2023_9201.txt',
#                       'cycling_chaos_code_raceresults_gc_2024_9201.txt',]

raceresult_gc_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

# raceresult_gc_count_limit = 8

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
    file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[raceresult_gc_count], 'r')
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

##### Race Results Stages - Youth Standings #####

# read in ingestion tracker and create a list of stages where known errors don't occur

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']['file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()



cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# need to get a list of stage races

cci_file_name_list_stage_races = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].to_list()

raceresults_stagerace_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

print(raceresults_stagerace_count_limit)

raceresults_stagerace_count = 0

# adding empty lists for df fields
file_name = []
file_name_prefix = []
season = []
first_cycling_race_id = []
stage_number = []
first_cycling_rider_id = []
youth_position_overall = []
youth_time_raw_overall = []

# get youth standings results on an overall race standings level

# transformation loop

for raceresults_stagerace_count in tqdm(range(
                                              0,
                                            #   526,
                                            #   526
                                              raceresults_stagerace_count_limit
                                              )):
    # use try for the beautiful soup incase the table doesn't exist in the stage
    # examples of this are cancelled stages
    # tbody[1] means Youth standings when looking at overall standings
    try:
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list_stage_races[raceresults_stagerace_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        if '<div class="tab-content" id="youth">' in str(file_soup):
            #print('contains statement works')
            file_soup_part2 = file_soup.find_all('tbody')[1]

            for row in file_soup_part2.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    # create filename field for the transformation on a stage basis
                    file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                    file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                    # use filename to get season of race
                    season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                    # use filename to get race_id
                    first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                    # use file name to get the stage number in raw format before transforming into double digits
                    # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                    # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                    # use try and first column to get youth standings position
                    try:
                        youth_position_overall.append(columns[0].text)
                    except:
                        youth_position_overall.append('Error')
                    # not sure why yet but sometimes rider_id doesn't work at all.
                    try:
                        first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        try:
                            first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                        except:
                            first_cycling_rider_id.append('Error')
                    # should update this to include data-label instead of column number
                    try:
                        youth_time_raw_overall.append(columns[6].text)
                    except:
                        try:
                            youth_time_raw_overall.append(columns[5].text)
                        except: youth_time_raw_overall.append('Error')
        else: 'Error in contains'
        
    except:
        'Error'

        # create df and write to disk
        
    raceresults_df_youth_overall = pd.DataFrame({
                'file_name':file_name,
                'file_name_prefix':file_name_prefix,
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id,
                # ,'stage_number':stage_number,
                'youth_position':youth_position_overall
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'youth_time_raw':youth_time_raw_overall
    })

raceresults_stagerace_count = raceresults_stagerace_count + 1

raceresults_df_youth_overall.to_csv(setwd+'raceresults_df_youth_overall.csv',index=False)

raceresults_df_youth_overall

# trying to create list for youth stages racelist

# bring in ingestion tracker and remove stage results with known errors

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# bring in df with races that have a youth classification

raceresults_df_youth_overall = pd.read_csv(setwd+'raceresults_df_youth_overall.csv')

raceresults_df_youth_overall = raceresults_df_youth_overall.loc[raceresults_df_youth_overall['youth_time_raw'] != 'Error'].reset_index()

raceresults_df_youth_overall_list = raceresults_df_youth_overall['file_name_prefix'].drop_duplicates().to_list()


raceresults_df_youth_overall_count_limit = raceresults_df_youth_overall['file_name_prefix'].drop_duplicates().nunique()
# raceresults_df_youth_stage_racelist = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']

# create function which brings back all file names that have the file_name_prefix for races with youth standings

file_name_youth = []

raceresults_df_youth_overall_count = 0

for raceresults_df_youth_overall_count in range(0,raceresults_df_youth_overall_count_limit):
    if raceresults_df_youth_overall_list[raceresults_df_youth_overall_count] in str(raceresults_df_youth_overall['file_name'])+'*':
        file_name_youth.append(raceresults_df_youth_overall['file_name_prefix'])
        # print('Works')
    else: 'Error'

raceresults_df_youth_overall_count = raceresults_df_youth_overall_count + 1

raceresults_df_youth_overall

# take youth overall standings and create list of races where there are youth standings tracked in race

raceresults_df_youth_overall = raceresults_df_youth_overall.loc[raceresults_df_youth_overall['youth_time_raw'] != 'Error'].reset_index()

raceresults_df_youth_overall_racelist = raceresults_df_youth_overall

raceresults_df_youth_overall_racelist['season_race_id'] = raceresults_df_youth_overall_racelist['season'].astype(str)+'_'+raceresults_df_youth_overall_racelist['first_cycling_race_id'].astype(str)

raceresults_df_youth_overall_racelist = raceresults_df_youth_overall_racelist['season_race_id'].drop_duplicates().to_list()

raceresults_df_youth_overall_racelist

calendar_df = pd.read_csv(setwd+'frontend_csv/calendar.csv')

calendar_df['race_id_nan'] = np.isnan(calendar_df.first_cycling_race_id.values)

calendar_df = calendar_df.loc[calendar_df['race_id_nan'] == False]

calendar_df['season_race_id'] = calendar_df['season'].astype(str)+'_'+(calendar_df['first_cycling_race_id'].astype(int)).astype(str)

raceresults_df_youth_stage_racelist_df = calendar_df[calendar_df['season_race_id'].isin(raceresults_df_youth_overall_racelist)]

calendar_df

raceresults_df_youth_stage_racelist_df

raceresults_df_youth_stage_racelist_df['stg_number_float'] = raceresults_df_youth_stage_racelist_df['stage_number'].astype(int)

raceresults_df_youth_stage_racelist_df['file_name'] = 'cycling_chaos_code_raceresults_stages_'+raceresults_df_youth_stage_racelist_df['season_race_id']+'_'+raceresults_df_youth_stage_racelist_df['stg_number_float'].astype(str)+'.txt'

raceresults_df_youth_stage_racelist_df = raceresults_df_youth_stage_racelist_df[~raceresults_df_youth_stage_racelist_df['file_name'].isin(known_errors_list)]

raceresults_df_youth_stage_racelist_list = raceresults_df_youth_stage_racelist_df['file_name'].to_list()

# raceresults_df_youth_stage_racelist

raceresults_df_youth_stage_racelist_count_limit = raceresults_df_youth_stage_racelist_df['file_name'].drop_duplicates().nunique()

raceresults_df_youth_stage_racelist_count_limit

# create empty lists for df fields

season = []
first_cycling_race_id = []
stage_number = []
youth_position_stage = []
first_cycling_rider_id_stage = []
youth_time_raw_stage = []

raceresults_stage_count = 0

# transformation loop

for raceresults_stage_count in tqdm(range(0,
                                # 1
                                raceresults_df_youth_stage_racelist_count_limit
                                )):
    try:
        # print(raceresults_df_youth_stage_racelist_list[raceresults_stage_count])
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_youth_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = Youth
        file_soup_part2 = file_soup.find_all('tbody')[2]
    except:
        print('Error in '+raceresults_df_youth_stage_racelist_list[raceresults_stage_count])
        raceresults_stage_count = raceresults_stage_count + 1
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_youth_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = Youth
        file_soup_part2 = file_soup.find_all('tbody')[2]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            # use racelist with youth standings in overall to get season
            season.append(str(raceresults_df_youth_stage_racelist_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            # use racelist with youth standings in overall to get race_id
            first_cycling_race_id.append(str(raceresults_df_youth_stage_racelist_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            # use racelist with youth standings in overall to get stage_number
            stage_number_raw = int((raceresults_df_youth_stage_racelist_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            # use try and first column to get youth standings position
            try:
                youth_position_stage.append(columns[0].text)
            except:
                youth_position_stage.append('Error')
            # not sure why yet but sometimes rider_id doesn't work at all.
            try:
                first_cycling_rider_id_stage.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id_stage.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id_stage.append('Error')
            # should update this to include data-label instead of column number
            try:
                youth_time_raw_stage.append(columns[6].text)
            except:
                try:
                    youth_time_raw_stage.append(columns[5].text)
                except: youth_time_raw_stage.append('Error')
            
    raceresults_stage_df_youth = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'youth_position':youth_position_stage
                ,'first_cycling_rider_id':first_cycling_rider_id_stage
                ,'youth_time_raw':youth_time_raw_stage
    })
raceresults_stage_count = raceresults_stage_count + 1

# raceresult_stage_count_limit

raceresults_stage_df_youth.to_csv(setwd+'raceresults_df_youth_stage.csv',index=False)
# file_soup_tbody_count

raceresults_stage_df_youth

##### Race Results Stages - points Standings #####

# read in ingestion tracker and create a list of stages where known errors don't occur

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']['file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()



cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# need to get a list of stage races

cci_file_name_list_stage_races = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].to_list()

raceresults_stagerace_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

raceresults_stagerace_count = 0

# adding empty lists for df fields
file_name = []
file_name_prefix = []
season = []
first_cycling_race_id = []
stage_number = []
first_cycling_rider_id = []
points_position_overall = []
points_score_raw_overall = []

# get points standings results on an overall race standings level

# transformation loop

for raceresults_stagerace_count in tqdm(range(0,
                                            #   1
                                              raceresults_stagerace_count_limit
                                              )):
    # use try for the beautiful soup incase the table doesn't exist in the stage
    # examples of this are cancelled stages
    # tbody[1] means points standings when looking at overall standings
    try:
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list_stage_races[raceresults_stagerace_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        if '<div class="tab-content" id="youth">' in str(file_soup):
            #print('contains statement works')
            file_soup_part2 = file_soup.find_all('tbody')[2]

            for row in file_soup_part2.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    # create filename field for the transformation on a stage basis
                    file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                    file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                    # use filename to get season of race
                    season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                    # use filename to get race_id
                    first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                    # use file name to get the stage number in raw format before transforming into double digits
                    # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                    # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                    # use try and first column to get points standings position
                    try:
                        points_position_overall.append(columns[0].text)
                    except:
                        points_position_overall.append('Error')
                    # not sure why yet but sometimes rider_id doesn't work at all.
                    try:
                        first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        try:
                            first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                        except:
                            first_cycling_rider_id.append('Error')
                    # should update this to include data-label instead of column number
                    try:
                        points_score_raw_overall.append(columns[6].text)
                    except:
                        try:
                            points_score_raw_overall.append(columns[5].text)
                        except: points_score_raw_overall.append('Error')
        else:
            file_soup_part2 = file_soup.find_all('tbody')[1]

            for row in file_soup_part2.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    # create filename field for the transformation on a stage basis
                    file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                    file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                    # use filename to get season of race
                    season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                    # use filename to get race_id
                    first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                    # use file name to get the stage number in raw format before transforming into double digits
                    # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                    # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                    # use try and first column to get points standings position
                    try:
                        points_position_overall.append(columns[0].text)
                    except:
                        points_position_overall.append('Error')
                    # not sure why yet but sometimes rider_id doesn't work at all.
                    try:
                        first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        try:
                            first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                        except:
                            first_cycling_rider_id.append('Error')
                    # should update this to include data-label instead of column number
                    try:
                        points_score_raw_overall.append(columns[6].text)
                    except:
                        try:
                            points_score_raw_overall.append(columns[5].text)
                        except: points_score_raw_overall.append('Error')
    except:
        'Error'

        # create df and write to disk
        
    raceresults_df_points_overall = pd.DataFrame({
                'file_name':file_name,
                'file_name_prefix':file_name_prefix,
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id,
                # ,'stage_number':stage_number,
                'points_position':points_position_overall
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'points_score_raw':points_score_raw_overall
    })

raceresults_stagerace_count = raceresults_stagerace_count + 1

raceresults_df_points_overall.to_csv(setwd+'raceresults_df_points_overall.csv',index=False)

raceresults_df_points_overall

# trying to create list for points stages racelist

# bring in ingestion tracker and remove stage results with known errors

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# bring in df with races that have a points classification

raceresults_df_points_overall = pd.read_csv(setwd+'raceresults_df_points_overall.csv')

raceresults_df_points_overall = raceresults_df_points_overall.loc[raceresults_df_points_overall['points_score_raw'] != 'Error'].reset_index()

raceresults_df_points_overall_list = raceresults_df_points_overall['file_name_prefix'].drop_duplicates().to_list()


raceresults_df_points_overall_count_limit = raceresults_df_points_overall['file_name_prefix'].drop_duplicates().nunique()
# raceresults_df_points_stage_racelist = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']

# create function which brings back all file names that have the file_name_prefix for races with points standings

file_name_points = []

raceresults_df_points_overall_count = 0

for raceresults_df_points_overall_count in range(0,raceresults_df_points_overall_count_limit):
    if raceresults_df_points_overall_list[raceresults_df_points_overall_count] in str(raceresults_df_points_overall['file_name'])+'*':
        file_name_points.append(raceresults_df_points_overall['file_name_prefix'])
        # print('Works')
    else: 'Error'

raceresults_df_points_overall_count = raceresults_df_points_overall_count + 1
    
raceresults_df_points_overall_count = raceresults_df_points_overall_count + 1

raceresults_df_points_overall

# take points overall standings and create list of races where there are points standings tracked in race

raceresults_df_points_overall = raceresults_df_points_overall.loc[raceresults_df_points_overall['points_score_raw'] != 'Error'].reset_index()

raceresults_df_points_overall_racelist = raceresults_df_points_overall

raceresults_df_points_overall_racelist['season_race_id'] = raceresults_df_points_overall_racelist['season'].astype(str)+'_'+raceresults_df_points_overall_racelist['first_cycling_race_id'].astype(str)

raceresults_df_points_overall_racelist = raceresults_df_points_overall_racelist['season_race_id'].drop_duplicates().to_list()

raceresults_df_points_overall_racelist

calendar_df = pd.read_csv(setwd+'frontend_csv/calendar.csv')

calendar_df['season_race_id'] = calendar_df['season'].astype(str)+'_'+calendar_df['first_cycling_race_id'].astype(str)

raceresults_df_points_stage_racelist_df = calendar_df[calendar_df['season_race_id'].isin(raceresults_df_points_overall_racelist)]

raceresults_df_points_stage_racelist_df['stg_number_float'] = raceresults_df_points_stage_racelist_df['stage_number'].astype(int)

raceresults_df_points_stage_racelist_df['file_name'] = 'cycling_chaos_code_raceresults_stages_'+raceresults_df_points_stage_racelist_df['season_race_id']+'_'+raceresults_df_points_stage_racelist_df['stg_number_float'].astype(str)+'.txt'

raceresults_df_points_stage_racelist_df = raceresults_df_points_stage_racelist_df[~raceresults_df_points_stage_racelist_df['file_name'].isin(known_errors_list)]

raceresults_df_points_stage_racelist_list = raceresults_df_points_stage_racelist_df['file_name'].to_list()

# raceresults_df_points_stage_racelist

raceresults_df_points_stage_racelist_count_limit = raceresults_df_points_stage_racelist_df['file_name'].drop_duplicates().nunique()

raceresults_df_points_stage_racelist_count_limit

# create empty lists for df fields

season = []
first_cycling_race_id = []
stage_number = []
points_position_stage = []
first_cycling_rider_id_stage = []
points_score_raw_stage = []

raceresults_stage_count = 0

# transformation loop

for raceresults_stage_count in tqdm(range(
                                          0,
                                # 984,
                                raceresults_df_points_stage_racelist_count_limit
                                )):
    try:
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_points_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = points
        file_soup_part2 = file_soup.find_all('tbody')[3]
    except:
        print('Error in '+raceresults_df_points_stage_racelist_list[raceresults_stage_count])
        raceresults_stage_count = raceresults_stage_count + 1
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_points_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = points
        file_soup_part2 = file_soup.find_all('tbody')[2]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            # use racelist with points standings in overall to get season
            season.append(str(raceresults_df_points_stage_racelist_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            # use racelist with points standings in overall to get race_id
            first_cycling_race_id.append(str(raceresults_df_points_stage_racelist_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            # use racelist with points standings in overall to get stage_number
            stage_number_raw = int((raceresults_df_points_stage_racelist_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            # use try and first column to get points standings position
            try:
                points_position_stage.append(columns[0].text)
            except:
                points_position_stage.append('Error')
            # not sure why yet but sometimes rider_id doesn't work at all.
            try:
                first_cycling_rider_id_stage.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id_stage.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id_stage.append('Error')
            # should update this to include data-label instead of column number
            try:
                points_score_raw_stage.append(columns[6].text)
            except:
                try:
                    points_score_raw_stage.append(columns[5].text)
                except: points_score_raw_stage.append('Error')
            
            raceresults_stage_df_points = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'points_position':points_position_stage
                ,'first_cycling_rider_id':first_cycling_rider_id_stage
                ,'points_score_raw':points_score_raw_stage
            })
raceresults_stage_count = raceresults_stage_count + 1

# raceresult_stage_count_limit

raceresults_stage_df_points.to_csv(setwd+'raceresults_df_points_stage.csv',index=False)
# file_soup_tbody_count

raceresults_stage_df_points

##### Race Results Stages - kom Standings #####

# read in ingestion tracker and create a list of stages where known errors don't occur

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']['file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()



cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# need to get a list of stage races

cci_file_name_list_stage_races = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].to_list()

raceresults_stagerace_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

raceresults_stagerace_count = 0

# adding empty lists for df fields
file_name = []
file_name_prefix = []
season = []
first_cycling_race_id = []
stage_number = []
first_cycling_rider_id = []
kom_position_overall = []
kom_score_raw_overall = []

# get kom standings results on an overall race standings level

# transformation loop

for raceresults_stagerace_count in tqdm(range(0,
                                            #   1
                                              raceresults_stagerace_count_limit
                                              )):
    # use try for the beautiful soup incase the table doesn't exist in the stage
    # examples of this are cancelled stages
    # tbody[1] means kom standings when looking at overall standings
    try:
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list_stage_races[raceresults_stagerace_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        if '<div class="tab-content" id="youth">' in str(file_soup):
            file_soup_part2 = file_soup.find_all('tbody')[3]

            for row in file_soup_part2.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    # create filename field for the transformation on a stage basis
                    file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                    file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                    # use filename to get season of race
                    season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                    # use filename to get race_id
                    first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                    # use file name to get the stage number in raw format before transforming into double digits
                    # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                    # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                    # use try and first column to get kom standings position
                    try:
                        kom_position_overall.append(columns[0].text)
                    except:
                        kom_position_overall.append('Error')
                    # not sure why yet but sometimes rider_id doesn't work at all.
                    try:
                        first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        try:
                            first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                        except:
                            first_cycling_rider_id.append('Error')
                    # should update this to include data-label instead of column number
                    try:
                        kom_score_raw_overall.append(columns[6].text)
                    except:
                        try:
                            kom_score_raw_overall.append(columns[5].text)
                        except: kom_score_raw_overall.append('Error')
        else:
            file_soup_part2 = file_soup.find_all('tbody')[2]

            for row in file_soup_part2.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    # create filename field for the transformation on a stage basis
                    file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                    file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                    # use filename to get season of race
                    season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                    # use filename to get race_id
                    first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                    # use file name to get the stage number in raw format before transforming into double digits
                    # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                    # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                    # use try and first column to get kom standings position
                    try:
                        kom_position_overall.append(columns[0].text)
                    except:
                        kom_position_overall.append('Error')
                    # not sure why yet but sometimes rider_id doesn't work at all.
                    try:
                        first_cycling_rider_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        try:
                            first_cycling_rider_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                        except:
                            first_cycling_rider_id.append('Error')
                    # should update this to include data-label instead of column number
                    try:
                        kom_score_raw_overall.append(columns[6].text)
                    except:
                        try:
                            kom_score_raw_overall.append(columns[5].text)
                        except: kom_score_raw_overall.append('Error')
    except:
        'Error'

        # create df and write to disk
        
        raceresults_df_kom_overall = pd.DataFrame({
                'file_name':file_name,
                'file_name_prefix':file_name_prefix,
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id,
                # ,'stage_number':stage_number,
                'kom_position':kom_position_overall
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'kom_score_raw':kom_score_raw_overall
            })

raceresults_stagerace_count = raceresults_stagerace_count + 1

raceresults_df_kom_overall.to_csv(setwd+'raceresults_df_kom_overall.csv',index=False)

raceresults_df_kom_overall

# trying to create list for kom stages racelist

# bring in ingestion tracker and remove stage results with known errors

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# bring in df with races that have a kom classification

raceresults_df_kom_overall = pd.read_csv(setwd+'raceresults_df_kom_overall.csv')

raceresults_df_kom_overall = raceresults_df_kom_overall.loc[raceresults_df_kom_overall['kom_score_raw'] != 'Error'].reset_index()

raceresults_df_kom_overall_list = raceresults_df_kom_overall['file_name_prefix'].drop_duplicates().to_list()


raceresults_df_kom_overall_count_limit = raceresults_df_kom_overall['file_name_prefix'].drop_duplicates().nunique()
# raceresults_df_kom_stage_racelist = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']

# create function which brings back all file names that have the file_name_prefix for races with kom standings

file_name_kom = []

raceresults_df_kom_overall_count = 0

for raceresults_df_kom_overall_count in range(0,raceresults_df_kom_overall_count_limit):
    if raceresults_df_kom_overall_list[raceresults_df_kom_overall_count] in str(raceresults_df_kom_overall['file_name'])+'*':
        file_name_kom.append(raceresults_df_kom_overall['file_name_prefix'])
        # print('Works')
    else: 'Error'

raceresults_df_kom_overall_count = raceresults_df_kom_overall_count + 1
    
raceresults_df_kom_overall_count = raceresults_df_kom_overall_count + 1

raceresults_df_kom_overall

# take kom overall standings and create list of races where there are kom standings tracked in race

raceresults_df_kom_overall = raceresults_df_kom_overall.loc[raceresults_df_kom_overall['kom_score_raw'] != 'Error'].reset_index()

raceresults_df_kom_overall_racelist = raceresults_df_kom_overall

raceresults_df_kom_overall_racelist['season_race_id'] = raceresults_df_kom_overall_racelist['season'].astype(str)+'_'+raceresults_df_kom_overall_racelist['first_cycling_race_id'].astype(str)

raceresults_df_kom_overall_racelist = raceresults_df_kom_overall_racelist['season_race_id'].drop_duplicates().to_list()

raceresults_df_kom_overall_racelist

calendar_df = pd.read_csv(setwd+'frontend_csv/calendar.csv')

calendar_df['season_race_id'] = calendar_df['season'].astype(str)+'_'+calendar_df['first_cycling_race_id'].astype(str)

raceresults_df_kom_stage_racelist_df = calendar_df[calendar_df['season_race_id'].isin(raceresults_df_kom_overall_racelist)]

raceresults_df_kom_stage_racelist_df['stg_number_float'] = raceresults_df_kom_stage_racelist_df['stage_number'].astype(int)

raceresults_df_kom_stage_racelist_df['file_name'] = 'cycling_chaos_code_raceresults_stages_'+raceresults_df_kom_stage_racelist_df['season_race_id']+'_'+raceresults_df_kom_stage_racelist_df['stg_number_float'].astype(str)+'.txt'

raceresults_df_kom_stage_racelist_df = raceresults_df_kom_stage_racelist_df[~raceresults_df_kom_stage_racelist_df['file_name'].isin(known_errors_list)]

raceresults_df_kom_stage_racelist_list = raceresults_df_kom_stage_racelist_df['file_name'].to_list()

# raceresults_df_kom_stage_racelist

raceresults_df_kom_stage_racelist_count_limit = raceresults_df_kom_stage_racelist_df['file_name'].drop_duplicates().nunique()

raceresults_df_kom_stage_racelist_count_limit

# create empty lists for df fields

season = []
first_cycling_race_id = []
stage_number = []
kom_position_stage = []
first_cycling_rider_id_stage = []
kom_score_raw_stage = []

raceresults_stage_count = 0

# transformation loop

for raceresults_stage_count in tqdm(range(0,
                                # 1
                                raceresults_df_kom_stage_racelist_count_limit
                                )):
    try:
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_kom_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = kom
        file_soup_part2 = file_soup.find_all('tbody')[4]
    except:
        print('Error in '+raceresults_df_kom_stage_racelist_list[raceresults_stage_count])
        raceresults_stage_count = raceresults_stage_count + 1
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_kom_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = kom
        file_soup_part2 = file_soup.find_all('tbody')[3]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            # use racelist with kom standings in overall to get season
            season.append(str(raceresults_df_kom_stage_racelist_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            # use racelist with kom standings in overall to get race_id
            first_cycling_race_id.append(str(raceresults_df_kom_stage_racelist_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            # use racelist with kom standings in overall to get stage_number
            stage_number_raw = int((raceresults_df_kom_stage_racelist_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            # use try and first column to get kom standings position
            try:
                kom_position_stage.append(columns[0].text)
            except:
                kom_position_stage.append('Error')
            # not sure why yet but sometimes rider_id doesn't work at all.
            try:
                first_cycling_rider_id_stage.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_rider_id_stage.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_rider_id_stage.append('Error')
            # should update this to include data-label instead of column number
            try:
                kom_score_raw_stage.append(columns[6].text)
            except:
                try:
                    kom_score_raw_stage.append(columns[5].text)
                except: kom_score_raw_stage.append('Error')
            
            raceresults_stage_df_kom = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'kom_position':kom_position_stage
                ,'first_cycling_rider_id':first_cycling_rider_id_stage
                ,'kom_score_raw':kom_score_raw_stage
            })
raceresults_stage_count = raceresults_stage_count + 1

# raceresult_stage_count_limit

raceresults_stage_df_kom.to_csv(setwd+'raceresults_df_kom_stage.csv',index=False)
# file_soup_tbody_count

raceresults_stage_df_kom

##### Race Results Stages - team Standings #####

# read in ingestion tracker and create a list of stages where known errors don't occur

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']['file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()



cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# need to get a list of stage races

cci_file_name_list_stage_races = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].to_list()

raceresults_stagerace_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'gc']['file_name'].nunique()

raceresults_stagerace_count = 0

# adding empty lists for df fields
file_name = []
file_name_prefix = []
season = []
first_cycling_race_id = []
stage_number = []
first_cycling_team_id = []
team_position_overall = []
team_time_raw_overall = []

# get team standings results on an overall race standings level

# transformation loop

for raceresults_stagerace_count in tqdm(range(0,
                                            #   1
                                              raceresults_stagerace_count_limit
                                              )):
    # use try for the beautiful soup incase the table doesn't exist in the stage
    # examples of this are cancelled stages
    # tbody[1] means team standings when looking at overall standings
    try:
        file = open(setwd+'souped_html_txt_files/'+cci_file_name_list_stage_races[raceresults_stagerace_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # file_soup_tbody_count = file_soup.count('tbody')
        file_soup_part2 = file_soup.find_all('tbody')[1]

        for row in file_soup_part2.find_all('tr'):
            columns = row.find_all('td')

            if(columns != []):
                # create filename field for the transformation on a stage basis
                file_name.append(cci_file_name_list_stage_races[raceresults_stagerace_count])
                file_name_prefix.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('.')[0])
                # use filename to get season of race
                season.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[5].split('.')[0])
                # use filename to get race_id
                first_cycling_race_id.append(str(cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[6].split('.')[0])
                # use file name to get the stage number in raw format before transforming into double digits
                # stage_number_raw = int((cci_file_name_list_stage_races[raceresults_stagerace_count]).split('_')[7].split('.')[0])
                # stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
                # use try and first column to get team standings position
                try:
                    team_position_overall.append(columns[0].text)
                except:
                    team_position_overall.append('Error')
                # not sure why yet but sometimes team_id doesn't work at all.
                try:
                    first_cycling_team_id.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    try:
                        first_cycling_team_id.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                    except:
                        first_cycling_team_id.append('Error')
                # should update this to include data-label instead of column number
                try:
                    team_time_raw_overall.append(columns[6].text)
                except:
                    try:
                        team_time_raw_overall.append(columns[5].text)
                    except: team_time_raw_overall.append('Error')
    except:
        'Error'

        # create df and write to disk
        
        raceresults_df_team_overall = pd.DataFrame({
                'file_name':file_name,
                'file_name_prefix':file_name_prefix,
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id,
                # ,'stage_number':stage_number,
                'team_position':team_position_overall
                ,'first_cycling_team_id':first_cycling_team_id
                ,'team_time_raw':team_time_raw_overall
            })

raceresults_stagerace_count = raceresults_stagerace_count + 1

raceresults_df_team_overall.to_csv(setwd+'raceresults_df_team_overall.csv',index=False)

raceresults_df_team_overall

# trying to create list for team stages racelist

# bring in ingestion tracker and remove stage results with known errors

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

known_errors_list = pd.read_csv(setwd+'cyclingchaos_raceresults_df_master_errors.csv')
known_errors_list = known_errors_list.loc[known_errors_list['stage_number']!='GC']
known_errors_list['ingest_file_name'] = 'cycling_chaos_code_raceresults_stages_'+known_errors_list['season'].astype(str)+'_'+known_errors_list['first_cycling_race_id'].astype(str)+'_'+(known_errors_list['stage_number'].astype(int)).astype(str)+'.txt'
known_errors_list = known_errors_list['ingest_file_name'].to_list()

cycling_chaos_ingestion = cycling_chaos_ingestion[~cycling_chaos_ingestion['file_name'].isin(known_errors_list)]

# bring in df with races that have a team classification

raceresults_df_team_overall = pd.read_csv(setwd+'raceresults_df_team_overall.csv')

raceresults_df_team_overall = raceresults_df_team_overall.loc[raceresults_df_team_overall['team_time_raw'] != 'Error'].reset_index()

raceresults_df_team_overall_list = raceresults_df_team_overall['file_name_prefix'].drop_duplicates().to_list()


raceresults_df_team_overall_count_limit = raceresults_df_team_overall['file_name_prefix'].drop_duplicates().nunique()
# raceresults_df_team_stage_racelist = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stages']

# create function which brings back all file names that have the file_name_prefix for races with team standings

file_name_team = []

raceresults_df_team_overall_count = 0

for raceresults_df_team_overall_count in range(0,raceresults_df_team_overall_count_limit):
    if raceresults_df_team_overall_list[raceresults_df_team_overall_count] in str(raceresults_df_team_overall['file_name'])+'*':
        file_name_team.append(raceresults_df_team_overall['file_name_prefix'])
        # print('Works')
    else: 'Error'

raceresults_df_team_overall_count = raceresults_df_team_overall_count + 1
    
raceresults_df_team_overall_count = raceresults_df_team_overall_count + 1

raceresults_df_team_overall

# take team overall standings and create list of races where there are team standings tracked in race

raceresults_df_team_overall = raceresults_df_team_overall.loc[raceresults_df_team_overall['team_time_raw'] != 'Error'].reset_index()

raceresults_df_team_overall_racelist = raceresults_df_team_overall

raceresults_df_team_overall_racelist['season_race_id'] = raceresults_df_team_overall_racelist['season'].astype(str)+'_'+raceresults_df_team_overall_racelist['first_cycling_race_id'].astype(str)

raceresults_df_team_overall_racelist = raceresults_df_team_overall_racelist['season_race_id'].drop_duplicates().to_list()

raceresults_df_team_overall_racelist

calendar_df = pd.read_csv(setwd+'frontend_csv/calendar.csv')

calendar_df['season_race_id'] = calendar_df['season'].astype(str)+'_'+calendar_df['first_cycling_race_id'].astype(str)

raceresults_df_team_stage_racelist_df = calendar_df[calendar_df['season_race_id'].isin(raceresults_df_team_overall_racelist)]

raceresults_df_team_stage_racelist_df['stg_number_float'] = raceresults_df_team_stage_racelist_df['stage_number'].astype(int)

raceresults_df_team_stage_racelist_df['file_name'] = 'cycling_chaos_code_raceresults_stages_'+raceresults_df_team_stage_racelist_df['season_race_id']+'_'+raceresults_df_team_stage_racelist_df['stg_number_float'].astype(str)+'.txt'

raceresults_df_team_stage_racelist_df = raceresults_df_team_stage_racelist_df[~raceresults_df_team_stage_racelist_df['file_name'].isin(known_errors_list)]

raceresults_df_team_stage_racelist_list = raceresults_df_team_stage_racelist_df['file_name'].to_list()

# raceresults_df_team_stage_racelist

raceresults_df_team_stage_racelist_count_limit = raceresults_df_team_stage_racelist_df['file_name'].drop_duplicates().nunique()

raceresults_df_team_stage_racelist_count_limit

# create empty lists for df fields

season = []
first_cycling_race_id = []
stage_number = []
team_position_stage = []
first_cycling_team_id_stage = []
team_time_raw_stage = []

raceresults_stage_count = 0

# transformation loop

for raceresults_stage_count in tqdm(range(0,
                                # 1
                                raceresults_df_team_stage_racelist_count_limit
                                )):
    try:
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_team_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = team
        file_soup_part2 = file_soup.find_all('tbody')[2]
    except:
        print('Error in '+raceresults_df_team_stage_racelist_list[raceresults_stage_count])
        raceresults_stage_count = raceresults_stage_count + 1
        file = open(setwd+'souped_html_txt_files/'+raceresults_df_team_stage_racelist_list[raceresults_stage_count], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        # tbody[2] = team
        file_soup_part2 = file_soup.find_all('tbody')[2]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            # use racelist with team standings in overall to get season
            season.append(str(raceresults_df_team_stage_racelist_list[raceresults_stage_count]).split('_')[5].split('.')[0])
            # use racelist with team standings in overall to get race_id
            first_cycling_race_id.append(str(raceresults_df_team_stage_racelist_list[raceresults_stage_count]).split('_')[6].split('.')[0])
            # use racelist with team standings in overall to get stage_number
            stage_number_raw = int((raceresults_df_team_stage_racelist_list[raceresults_stage_count]).split('_')[7].split('.')[0])
            stage_number.append(np.where(stage_number_raw < 10,'0'+str(stage_number_raw),str(stage_number_raw)))
            # use try and first column to get team standings position
            try:
                team_position_stage.append(columns[0].text)
            except:
                team_position_stage.append('Error')
            # not sure why yet but sometimes team_id doesn't work at all.
            try:
                first_cycling_team_id_stage.append(str(columns[4].find_all('a')).split('php?r=')[1].split('&amp')[0])
            except:
                try:
                    first_cycling_team_id_stage.append(str(columns[3].find_all('a')).split('php?r=')[1].split('&amp')[0])
                except:
                    first_cycling_team_id_stage.append('Error')
            # should update this to include data-label instead of column number
            try:
                team_time_raw_stage.append(columns[6].text)
            except:
                try:
                    team_time_raw_stage.append(columns[5].text)
                except: team_time_raw_stage.append('Error')
            
            raceresults_stage_df_team = pd.DataFrame({
                'season':season
                ,'first_cycling_race_id':first_cycling_race_id
                ,'stage_number':stage_number
                ,'team_position':team_position_stage
                ,'first_cycling_team_id':first_cycling_team_id_stage
                ,'team_time_raw':team_time_raw_stage
            })
raceresults_stage_count = raceresults_stage_count + 1

# raceresult_stage_count_limit

raceresults_stage_df_team.to_csv(setwd+'raceresults_df_team_stage.csv',index=False)
# file_soup_tbody_count

raceresults_stage_df_team

##### Unioning RaceResults_Stage_df and RaceResults_GC_df #####

# reading stage time on stage races data and transforming fields to correct type 

raceresults_stage_df = pd.read_csv(setwd+'raceresults_stage_df.csv')
raceresults_stage_df['season'] = raceresults_stage_df['season'].astype(str)
raceresults_stage_df['first_cycling_race_id'] = raceresults_stage_df['first_cycling_race_id'].astype(str)
raceresults_stage_df['stage_number'] = np.where(raceresults_stage_df['stage_number'] < 10,'0'+raceresults_stage_df['stage_number'].astype(str),raceresults_stage_df['stage_number'].astype(str))
raceresults_stage_df['first_cycling_rider_id'] = raceresults_stage_df['first_cycling_rider_id'].astype(str)
# raceresults_stage_df['first_cycling_team_id'] = raceresults_stage_df['first_cycling_team_id'].astype(str)

# meant to be looking at stage race gc time, but currently reads one day gc time

raceresults_stage_df_gc = pd.read_csv(setwd+'raceresults_stage_gc_df.csv')
raceresults_stage_df_gc['season'] = raceresults_stage_df_gc['season'].astype(str)
raceresults_stage_df_gc['first_cycling_race_id'] = raceresults_stage_df_gc['first_cycling_race_id'].astype(str)
raceresults_stage_df_gc['stage_number'] = np.where(raceresults_stage_df_gc['stage_number'] < 10,'0'+raceresults_stage_df_gc['stage_number'].astype(str),raceresults_stage_df_gc['stage_number'].astype(str))
raceresults_stage_df_gc['first_cycling_rider_id'] = raceresults_stage_df_gc['first_cycling_rider_id'].astype(str)
raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_gc, on = ['season','first_cycling_race_id','stage_number','first_cycling_rider_id'])


raceresults_stage_df_youth = pd.read_csv(setwd+'raceresults_df_youth_stage.csv')
raceresults_stage_df_youth['season'] = raceresults_stage_df_youth['season'].astype(str)
raceresults_stage_df_youth['first_cycling_race_id'] = raceresults_stage_df_youth['first_cycling_race_id'].astype(str)
raceresults_stage_df_youth['stage_number'] = np.where(raceresults_stage_df_youth['stage_number'] < 10,'0'+raceresults_stage_df_youth['stage_number'].astype(str),raceresults_stage_df_youth['stage_number'].astype(str))
raceresults_stage_df_youth['first_cycling_rider_id'] = raceresults_stage_df_youth['first_cycling_rider_id'].astype(str)
raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_youth, on = ['season','first_cycling_race_id','stage_number','first_cycling_rider_id'])

raceresults_stage_df_points = pd.read_csv(setwd+'raceresults_df_points_stage.csv')
raceresults_stage_df_points['season'] = raceresults_stage_df_points['season'].astype(str)
raceresults_stage_df_points['first_cycling_race_id'] = raceresults_stage_df_points['first_cycling_race_id'].astype(str)
raceresults_stage_df_points['stage_number'] = np.where(raceresults_stage_df_points['stage_number'] < 10,'0'+raceresults_stage_df_points['stage_number'].astype(str),raceresults_stage_df_points['stage_number'].astype(str))
raceresults_stage_df_points['first_cycling_rider_id'] = raceresults_stage_df_points['first_cycling_rider_id'].astype(str)
raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_points, on = ['season','first_cycling_race_id','stage_number','first_cycling_rider_id'])

raceresults_stage_df_kom = pd.read_csv(setwd+'raceresults_df_kom_stage.csv')
raceresults_stage_df_kom['season'] = raceresults_stage_df_kom['season'].astype(str)
raceresults_stage_df_kom['first_cycling_race_id'] = raceresults_stage_df_kom['first_cycling_race_id'].astype(str)
raceresults_stage_df_kom['stage_number'] = np.where(raceresults_stage_df_kom['stage_number'] < 10,'0'+raceresults_stage_df_kom['stage_number'].astype(str),raceresults_stage_df_kom['stage_number'].astype(str))
raceresults_stage_df_kom['first_cycling_rider_id'] = raceresults_stage_df_kom['first_cycling_rider_id'].astype(str)
raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_kom, on = ['season','first_cycling_race_id','stage_number','first_cycling_rider_id'])

# raceresults_stage_df_team = pd.read_csv(setwd+'raceresults_df_team_stage.csv')
# raceresults_stage_df_team['season'] = raceresults_stage_df_team['season'].astype(str)
# raceresults_stage_df_team['first_cycling_race_id'] = raceresults_stage_df_team['first_cycling_race_id'].astype(str)
# raceresults_stage_df_team['stage_number'] = np.where(raceresults_stage_df_team['stage_number'] < 10,'0'+raceresults_stage_df_team['stage_number'].astype(str),raceresults_stage_df_team['stage_number'].astype(str))
# raceresults_stage_df_team['first_cycling_team_id'] = raceresults_stage_df_team['first_cycling_team_id'].astype(str)
# raceresults_stage_df = raceresults_stage_df.merge(raceresults_stage_df_team, on = ['season','first_cycling_race_id','stage_number','first_cycling_team_id'])


# creating fields for jersey data that is yet to be transformed
# raceresults_stage_df['gc_position'] = 'to do'
# raceresults_stage_df['gc_time_raw'] = 'to do'
# raceresults_stage_df['youth_position'] = 'to do'
# raceresults_stage_df['youth_time_raw'] = 'to do'
# raceresults_stage_df['points_position'] = 'to do'
# raceresults_stage_df['points_score_raw'] = 'to do'
# raceresults_stage_df['kom_position'] = 'to do'
# raceresults_stage_df['kom_score_raw'] = 'to do'
raceresults_stage_df['team_position'] = pd.NA
raceresults_stage_df['team_time_raw'] = pd.NA

# aligning columns for stage races

raceresults_stage_df = raceresults_stage_df[['season','first_cycling_race_id','stage_number','first_cycling_rider_id','gc_position','gc_time_raw','stage_position','stage_time_raw','youth_position','youth_time_raw','points_position','points_score_raw','kom_position','kom_score_raw','team_position','team_time_raw']]

# reading file in for one day races and adds additional columns ahead of unioning tables. 

raceresults_gc_df = pd.read_csv(setwd+'raceresults_gc_df.csv')
raceresults_gc_df['stage_position'] = raceresults_gc_df['gc_position']
raceresults_gc_df['stage_time_raw'] = raceresults_gc_df['gc_time_raw']
raceresults_gc_df['youth_position'] = pd.NA
raceresults_gc_df['youth_time_raw'] = pd.NA
raceresults_gc_df['points_position'] = pd.NA
raceresults_gc_df['points_score_raw'] = pd.NA
raceresults_gc_df['kom_position'] = pd.NA
raceresults_gc_df['kom_score_raw'] = pd.NA
raceresults_gc_df['team_position'] = pd.NA
raceresults_gc_df['team_time_raw'] = pd.NA

raceresults_stage_df = raceresults_stage_df[['season','first_cycling_race_id','stage_number','first_cycling_rider_id','gc_position','gc_time_raw','stage_position','stage_time_raw','youth_position','youth_time_raw','points_position','points_score_raw','kom_position','kom_score_raw','team_position','team_time_raw']]

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
