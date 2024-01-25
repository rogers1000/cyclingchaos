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

# setwd = WorkingDirectory

##### Transforming Calendar Ingest #####

# Making a list of files needing to be transformed

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cycling_chaos_ingestion = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'men') | (cycling_chaos_ingestion['output_details'] == 'women')].reset_index()

cci_file_name_list = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'men') | (cycling_chaos_ingestion['output_details'] == 'women')]['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'men') | (cycling_chaos_ingestion['output_details'] == 'women')]['file_name'].nunique()


calendar_ingestion_count = 0

# making an empty lists for fields required for the dataframe

first_cycling_race_id_list = []
year = []
gender = []
category = []
calendar_ingestion_count_str = []
first_cycling_race_id = []
race_name = []
race_nationality = []
uci_race_classification = []
stage_race_boolean = []
start_date = []
end_date = []


# transformation loop


for calendar_ingestion_count in tqdm(range(0,
                                    #   2
                                      calendar_ingestion_count_limit
                                      )):
#  beautiful soup to open html file
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    # file_soup_part2 = file_soup.find_all('tbody')[-1]
# some errors occur so as a backup we force first race and then remove duplicates.
    try:
        file_soup_part2 = file_soup.find_all('tbody')[-1]
    except:
        file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[0], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        file_soup_part2 = file_soup.find_all('tbody')[-1]
        print(cci_file_name_list[calendar_ingestion_count]+' failed')
        

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
# use file_name to work out season of race
            year.append(str(cycling_chaos_ingestion['file_name'][calendar_ingestion_count].split('_')[5]))
# work out gender using file_name.
            try:
                gender.append(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['output_details'][calendar_ingestion_count])
            except:
                gender.append('Error')
# Only doing race races at this point
            category.append('Road')
# 3rd column of the data set is the first_cycling_race_id, first_cycling_race_name and race_nationality
# When looking at race_name, if the race contains an '&' sign, it needs additional transformation
# nationality is worked out by looking at the id of the flag shown
            first_cycling_race_id.append(str(columns[2].find_all('a')).split('r=')[1].split('&amp')[0])
            if '&amp;' in str(columns[2].find_all('a')).split('title="')[1].split('">')[0]:
                then: race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0].split('amp;')[0]+str(columns[2].find_all('a')).split('title="')[1].split('">')[0].split('amp;')[-1])
            else: race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0])
            race_nationality.append(str(columns[2].find_all("span")).split("flag-")[1].split('"><')[0].upper())
# UCI Race classification is the 2nd column of the table
# UCI Road races are split into 1. for One Day Races and 2. for Stage Races
            uci_race_classification.append(columns[1].text)
            stage_race_boolean.append(np.where(columns[1].text.startswith('2'),"Stage Race","One Day"))
# First column is the dates which we transform into start date and end date
            start_date.append(year[-1]+'/'+columns[0].text.split('-')[0].split('.')[-1]+'/'+columns[0].text.split('-')[0].split('.')[0])
            end_date.append(year[-1]+'/'+columns[0].text.split('-')[-1].split('.')[-1]+'/'+columns[0].text.split('-')[-1].split('.')[0])

# create dataframe from the data transformed
            road_calendar_df = pd.DataFrame({
                'season':year
                ,'gender':gender
                ,'category':category
                ,'first_cycling_race_id':first_cycling_race_id
                ,'race_name':race_name
                ,'race_nationality':race_nationality
                ,'uci_race_classification':uci_race_classification
                ,'stage_race_boolean':stage_race_boolean
                ,'start_date':start_date
                ,'end_date':end_date
                })
# to continue the transformation loop
            
    calendar_ingestion_count = calendar_ingestion_count + 1

# drop duplicates produced by errors in the raw data

road_calendar_df = road_calendar_df.drop_duplicates(subset=['season','first_cycling_race_id'])

# sort dataframe by season, gender, start_date and end_date

road_calendar_df = road_calendar_df.sort_values(by=['season','gender','start_date','end_date'])

# write dataframe to disk and show output

road_calendar_df.to_csv(setwd+'first_cycling_calendar_df_master.csv', index=False)
road_calendar_df            
# print(road_calendar_df['season'])
# print(calendar_ingestion_count)

##### Stage Race Stages Profiles #####

# Read ingestion tracker and create lists of stage races stages that need ingesting.

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')
cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profile']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'stage_profile']['file_name'].nunique()

calendar_stage_profiles_ingestion_count = 0

# create empty lists for dataframe. _stage standing for stage races.

season_stage = []
first_cycling_race_id_stage = []
stage_number_stage = []
stage_profile_category_first_cycling_stage = []
distance_stage = []
route_stage = []
stage_profile_category_eng_stage = []

# transformation loop

for calendar_stage_profiles_ingestion_count in tqdm(range(0,
                                                        #   10
                                                          calendar_ingestion_count_limit
                                                          )):
# beautiful soup to open html file
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_stage_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
# raw data isn't perfect so fallback is in place. Duplicates are then dropped later.
    try:
        file_soup_part2 = file_soup.find_all('tbody')[0]
    except:
        file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[0], 'r')
        file_read = file.read()
        file_soup = BeautifulSoup(file_read, "html.parser")
        file_soup_part2 = file_soup.find_all('tbody')[0]
        print(cci_file_name_list[calendar_stage_profiles_ingestion_count]+' failed')

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
# use file_name to get season of the race for stage races
# use file_name to get the first_cycling_race_id for stage races
            season_stage.append(str(cci_file_name_list[calendar_stage_profiles_ingestion_count]).split('_')[6])
            first_cycling_race_id_stage.append(str(cci_file_name_list[calendar_stage_profiles_ingestion_count]).split('_')[7].split('.')[0])
# the first column in the table is the stage number for stage races.
# prologues stage_number id in the url's are '00' so we are using those instead of 'Pl.'
            stage_number_stage.append(np.where(columns[0].text == 'Pl.','00',columns[0].text))
# use the second column to get the stage profile category for stage races
            stage_profile_category_first_cycling_stage.append(str(columns[1]).split('src="img/mini/')[-1].split('.svg')[0])
# use the 4th column to get the distance for stage races
            distance_stage.append(columns[3].text)
# attempt to ge the route from the 5th column, if not then put error for stage races.
            try:
                route_stage.append(columns[4].text)
            except:
                route_stage.append('Error')
# create dataframe focusing on stage races using data transformed

            road_calendar_stage_profiles = pd.DataFrame({
                'season':season_stage
                ,'first_cycling_race_id':first_cycling_race_id_stage
                ,'stage_number':stage_number_stage
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling_stage
                ,'distance':distance_stage
                ,'route':route_stage
            })
    
    calendar_stage_profiles_ingestion_count = calendar_stage_profiles_ingestion_count + 1

    road_calendar_stage_profiles

# road_calendar_stage_profiles

    road_calendar_stage_profiles.to_csv(setwd+'road_calendar_stage_profiles.csv',index=False)
    
# road_calendar_stage_profiles = pd.read_csv(setwd+'road_calendar_stage_profiles.csv')

# road_calendar_stage_profiles

# dropping duplicates in stage profiles

road_calendar_stage_profiles['concat'] = road_calendar_stage_profiles['season'].astype(str)+road_calendar_stage_profiles['first_cycling_race_id'].astype(str)+road_calendar_stage_profiles['stage_number'].astype(str)
road_calendar_stage_profiles = road_calendar_stage_profiles.drop_duplicates(subset=['concat'])
road_calendar_stage_profiles = road_calendar_stage_profiles.drop('concat',axis=1)
road_calendar_stage_profiles

##### Trying to get Route & Distance for One Day Races #####

# seeing what one day profiles need transforming from the ingestion tracker

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profile']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output_details'] == 'oneday_profile']['file_name'].nunique()

calendar_oneday_profiles_ingestion_count = 0

# creating empty lists for the dataframe

season_oneday = []
first_cycling_race_id_oneday = []
stage_number_oneday = []
stage_profile_category_first_cycling_oneday = []
distance_oneday = []
route_oneday = []
stage_profile_category_eng_oneday = []

# transformation loop

for calendar_oneday_profiles_ingestion_count in tqdm(range(0,
                                                          # 1
                                                          calendar_ingestion_count_limit
                                                          )):
# open html file using beautiful soup
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_oneday_profiles_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
# use file_name to work out season for one day races
# use file to work out first_cycling_race_id for one day races
    season_oneday.append(cci_file_name_list[calendar_oneday_profiles_ingestion_count].split('_')[6])
    first_cycling_race_id_oneday.append(cci_file_name_list[calendar_oneday_profiles_ingestion_count].split('_')[7].split('.')[0])
# all one day races are 'GC' results
    stage_number_oneday.append('GC')
# find the image for the race profile to work out the first cycling profile category for one day races
# sometimes the races won't be classifed yet
    try:
        stage_profile_category_first_cycling_oneday.append(file_soup.find(title='Race profile icon').get('src').split('mini/')[-1].split('.')[0])
    except:
        stage_profile_category_first_cycling_oneday.append('Error')
# append distance and route for one day races to show blank cells.
# this is as I've not worked out how to transform distance and route yet for one day races.
    distance_oneday.append('')
    route_oneday.append('')

# create dataframe with transformed data

    road_calendar_oneday_profiles = pd.DataFrame({
                'season':season_oneday
                ,'first_cycling_race_id':first_cycling_race_id_oneday
                ,'stage_number':stage_number_oneday
                # ,'date':date
                ,'stage_profile_category_first_cycling':stage_profile_category_first_cycling_oneday
                ,'distance':distance_oneday
                ,'route':route_oneday
            })

# continue transform loop and write to disk

    calendar_oneday_profiles_ingestion_count = calendar_oneday_profiles_ingestion_count + 1

    road_calendar_oneday_profiles.to_csv(setwd+'road_calendar_oneday_profiles.csv',index=False)

# transform stage profiles for stage races to match field type for one day races

# road_calendar_stage_profiles = pd.read_csv(setwd+'road_calendar_stage_profiles.csv')
road_calendar_stage_profiles['season'] = road_calendar_stage_profiles['season'].astype(str)
road_calendar_stage_profiles['first_cycling_race_id'] = road_calendar_stage_profiles['first_cycling_race_id'].astype(str)

# road_calendar_stage_profiles = road_calendar_stage_profiles.drop_duplicates(subset=['season','first_cycling_race_id','stage_number'])


# road_calendar_oneday_profiles

# cci_file_name_list

# read stage profiles for one day races and union to stage profiles for stage races

road_calendar_oneday_profiles = pd.read_csv(setwd+'road_calendar_oneday_profiles.csv')

road_calendar_oneday_profiles

road_calendar_profiles = pd.concat([road_calendar_stage_profiles,road_calendar_oneday_profiles])
road_calendar_profiles

# create mapping dataframe for first_cycling category name to English
# then join to main dataframe and write to disk

stage_profile_category_first_cycling = ['Flatt','Tempo','Bakketempo','Fjell-MF','Fjell','Smaakupert-MF',
                                               'Smaakupert','Brosten','Lagtempo','Ukjent','<td></td>']

stage_profile_category_mapping_eng = ['Flat','Flat ITT','Mountain ITT','Mountain MTF','Mountain','Hilly MTF',
                                      'Hilly','Cobbles','TTT','Unknown','Unknown']

stage_profile_category_mapping = pd.DataFrame({'stage_profile_category_first_cycling':stage_profile_category_first_cycling,
                                               'stage_profile_category_mapping_eng':stage_profile_category_mapping_eng})

road_calendar_profiles = road_calendar_profiles.merge(stage_profile_category_mapping, on = 'stage_profile_category_first_cycling')
road_calendar_profiles = road_calendar_profiles.drop(['stage_profile_category_first_cycling'],axis=1)
# stage_profile_category_mapping

road_calendar_profiles.to_csv(setwd+'road_calendar_profiles.csv',index=False)

road_calendar_profiles.dtypes

# road_calendar_stage_profiles

# read calendar_df and stage_profiles files from disk and then merge
# then write to disk

first_cycling_calendar_df = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')
# first_cycling_calendar_df['season'] = first_cycling_calendar_df['season'].astype(str)
# first_cycling_calendar_df['first_cycling_race_id'] = first_cycling_calendar_df['first_cycling_race_id'].astype(str)

road_calendar_profiles = pd.read_csv(setwd+'road_calendar_profiles.csv'))

first_cycling_calendar_df = first_cycling_calendar_df.merge(road_calendar_profiles, on = ['season','first_cycling_race_id'])

first_cycling_calendar_df.to_csv(setwd+'first_cycling_calendar_df_master.csv',index=False)

first_cycling_calendar_df
