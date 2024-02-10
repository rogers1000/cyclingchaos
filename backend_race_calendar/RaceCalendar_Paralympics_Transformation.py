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

# create df idenitfying each paralympics and location of games

list_games_names = ['Toyko 2020','Rio 2016','London 2012','Beijing 2008','Athens 2004','Sydney 2000']

list_games_country_id = ['JP','BR','GB','CH','GR','AU']

list_games_unique_id = ['tokyo-2020','rio-2016','london-2012','beijing-2008','athens-2004','sydney-2000']

paralympics_games_df = pd.DataFrame({
    'games_name':list_games_names,
    'games_country':list_games_country_id,
    'games_id':list_games_unique_id
})

# load ingestion tracker, filter to startlists files and create list of file_names and count of file_names

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'calendar')]['file_name'].to_list()

paralympics_count_limit = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'calendar')]['file_name'].nunique()

# creating empty lists for dataframe

games_id = []
games_name = []
# year of start_date
season = []
# held within race_name
gender =[]
# held within race_name
category = []
# held within race_name
paralympics_race_id = []
paralympics_race_url = []
# first column of results base page
race_name = []
# location of games
country_id = []
# paralympics classification, held within race_name
uci_race_classification = []
# If it is an omnium or has qualifying event then 'Stage Race'
stage_race_boolean = []
# date of first race within detailed results page
start_date = []
# date of final race within detailed results page if multiple qualifying event
end_date = []
# Qualification name - ie First Round, Semi Final etc.
stage_number = []
distance = []
# '250m velodrome' for track races
route = []
# Not sure yet
stage_profile = []


games_calendar_count = 0

# transformation loop

for games_calendar_count in tqdm(range(0,
                                    #    1
                                       paralympics_count_limit
                                       )):
    # open html file using beautiful soup
    file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[games_calendar_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
# column 1 has both race_id and race_name.
            paralympics_race_id.append(str(columns[0].find_all('a')).split('href="/')[1].split('">')[0].replace('/results/cycling/','_'))
            paralympics_race_url.append(str(columns[0].find_all('a')).split('href="/')[1].split('">')[0])
            race_name.append(str(columns[0].find_all('a')).split('">')[1].split('\n ')[1].strip())
            if 'Road Race' in str(columns[0].find_all('a')).split('">')[1].split('\n ')[1].strip():
                category.append('Road')
                stage_profile.append('')
            else:
                category.append('Track')
                stage_profile.append('250m Velodrome')
            
# race_id contains other key details like gender, uci_classifcation
            gender.append(str(columns[0].find_all('a')).split('href="/')[1].split('">')[0].split('/')[3].split('-')[0])
# race_name contains other key details like uci_race_classification
            uci_race_classification.append(str(columns[0].find_all('a')).split('">')[1].split('\n ')[1].split(' ')[-1])
# adding in country_id, games_id and games_name from pre-built dataframe
            country_id.append(paralympics_games_df['games_country'][games_calendar_count])
            games_id.append(paralympics_games_df['games_id'][games_calendar_count])
            games_name.append(paralympics_games_df['games_name'][games_calendar_count])

            paralympics_calendar = pd.DataFrame({
                'gender':gender,
                'paralympics_race_id':paralympics_race_id,
                'paralympics_race_url':paralympics_race_url,
                'category':category,
                'race_name':race_name,
                'race_nationality':country_id,
                'uci_race_classification':uci_race_classification,
                'games_id':games_id,
                'games_name':games_name,
                'stage_profile':stage_profile
            })
    games_calendar_count = games_calendar_count + 1
        

paralympics_calendar.to_csv(setwd+'paralympics_calendar.csv',index=False)

paralympics_calendar

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'raceresults')]['file_name'].to_list()

paralympics_count_limit = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'raceresults')]['file_name'].nunique()

paralympics_race_id = []
# If it is an omnium or has qualifying event then 'Stage Race'
stage_race_boolean = []
# date of race stage_number
race_date = []
# Qualification name - ie First Round, Semi Final etc.
stage_number = []
distance = []
# '250m velodrome' for track races
route = []

games_results_count = 0

for games_results_count in tqdm(range(
                                      0,
                                      # 152,
                                      paralympics_count_limit
                                    )):
  file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[games_results_count], 'r')
  file_read = file.read()
  file_soup = BeautifulSoup(file_read, "html.parser")
  table_count_ingestion = 1
  table_count_limit = len(file_soup.find_all('tbody'))
#   print(table_count_limit)

  for table_count_ingestion in range(1,
                                    #  2
                                     table_count_limit
                                     ):
    file_soup_part2 = file_soup.find_all('tbody')[table_count_ingestion]
    # print(cci_file_name_list[games_results_count])
    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
          paralympics_race_id.append(str(cci_file_name_list[games_results_count]).replace('cycling_chaos_code_results_paralympics_','').replace('.txt','').replace('_results_cycling_','_'))
          stage_number.append(table_count_ingestion)
          # race_date.append(columns[4].text)
          # find column name called 'Date' and take output of that for date column
          # print(columns[4])
          if str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count]  or str('2012') in cci_file_name_list[games_results_count]:
            if 'date' in str(columns[0]) and (str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count]  or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[0].text)
            elif 'date' in str(columns[1]) and (str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[1].text)
            elif 'date' in str(columns[2]) and (str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[2].text)
            elif 'date' in str(columns[3]) and (str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[3].text)
            elif 'date' in str(columns[4]) and (str('2020')in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[4].text)
            elif 'date' in str(columns[5]) and (str('2020')in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[5].text)
            elif 'date' in str(columns[6]) and (str('2020') in cci_file_name_list[games_results_count] or str('2016') in cci_file_name_list[games_results_count] or str('2012') in cci_file_name_list[games_results_count]):
              race_date.append(columns[6].text)
          else: race_date.append('Error')
          # print(paralympics_race_id)
          # if str('2020') in cci_file_name_list[games_results_count]:
          #   print(cci_file_name_list[games_results_count]+' happened in 2020')
          # else: print(cci_file_name_list[games_results_count]+' happened outside 2020')


          paralympics_calendar_results = pd.DataFrame({
            'paralympics_race_id':paralympics_race_id,
            'stage_number':stage_number,
            'race_date':race_date
          })
  table_count_ingestion = table_count_ingestion + 1
games_results_count = games_results_count + 1

paralympics_calendar_results = paralympics_calendar_results.drop_duplicates()

paralympics_calendar_results.to_csv(setwd+'paralympics_calendar_results.csv',index=False)
paralympics_calendar_results


# merge calendar details from base calendar transform and transform from results page

paralympics_calendar2 = paralympics_calendar.merge(paralympics_calendar_results, on = 'paralympics_race_id')
## asked SDV for feedback on errors encountered below
# paralympics_calendar3 = paralympics_calendar2.groupby(['paralympics_race_id'],group_keys=True).agg({'stage_number':['max']})
paralympics_calendar2["start_date"] = paralympics_calendar2.groupby("paralympics_race_id").race_date.transform("min")
paralympics_calendar2["end_date"] = paralympics_calendar2.groupby("paralympics_race_id").race_date.transform("max")
paralympics_calendar2["stage_race_boolean"] = paralympics_calendar2.groupby("paralympics_race_id").stage_number.transform("max")

paralympics_calendar2['season'] = 'To Do'
# paralympics_calendar2['stage_race_boolean'] = 'To Do'
# paralympics_calendar2['start_date'] = 'To Do'
# paralympics_calendar2['end_date'] = 'To Do'
paralympics_calendar2['distance'] = 'To Do'
paralympics_calendar2['route'] = 'To Do'
paralympics_calendar2['stage_profile'] = 'To Do'
paralympics_calendar2['first_cycling_race_id'] = None



paralympics_calendar2 = paralympics_calendar2[['season', 'gender', 'category','first_cycling_race_id','paralympics_race_id', 'race_name',
       'race_nationality', 'uci_race_classification', 'stage_race_boolean',
       'start_date', 'end_date', 'stage_number', 'distance', 'route',
       'stage_profile']]

paralympics_calendar2

paralympics_calendar2.to_csv(setwd+'paralympics_calendar_df_master.csv',index=False)

# create rest of fields that are needed to union to first cycling calendar
## season
### race_date or games_name
## stage_race_boolean
### if stage_number exceeds 1 then stage race
## distance
### not sure yet, might have to be manual
## route
### [n] laps of 250m velodrome for track
## stage_profile
### size of velodrome if track (250m), road races not sure yet.
