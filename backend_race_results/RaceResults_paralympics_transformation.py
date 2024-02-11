##### work in progress #####

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

# load ingestion tracker, filter to startlists files and create list of file_names and count of file_names

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'raceresults')]['file_name'].to_list()

paralympics_count_limit = cycling_chaos_ingestion.loc[(cycling_chaos_ingestion['output_details'] == 'paralympics') & (cycling_chaos_ingestion['output'] == 'raceresults')]['file_name'].nunique()

# creating empty lists for dataframe

paralympics_race_id = []
stage_number = []
# Rank
rank = []
# NPC
nationality = []
# Athlete
rider_name = []
rider_id = []
# Time1 and Time
race_time = []
# date
race_date = []
# irm and IRM
race_irm = []
# combo of info and note
race_results_info = []
test = []

games_results_count = 0

for games_results_count in tqdm(range(
                                      0,
                                      # 1
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
        #    rank
          rank_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="Rank"' in str(columns[rank_column_count]):
              rank_column = rank_column_count
              # rank.append(columns[rank_column_count].text)
            else: 
              'Not in column '+str(rank_column_count)
            rank_column_count = rank_column_count + 1
          rank.append(str(columns[rank_column]))

        #    nationality
          nationality_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="NPC"' in str(columns[nationality_column_count]):
              nationality_column = nationality_column_count
              # nationality.append(columns[nationality_column_count].text)
            else:
              'Not in column '+str(nationality_column_count)
            nationality_column_count = nationality_column_count + 1
          try:
            nationality.append(str(columns[nationality_column].find_all('a')).split('title="')[1].split('">')[0])
          except: nationality.append('')
        #    rider_id
          rider_id_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="Athlete"' in str(columns[rider_id_column_count]):
              rider_id_column = rider_id_column_count
              # rider_name.append(columns[rider_name_column_count].text)
            else:
              'Not in column '+str(rider_id_column_count)
            rider_id_column_count = rider_id_column_count + 1
          try: rider_id.append(str(columns[rider_id_column]).split('href="/')[1].split('">\n')[0])
          except: rider_id.append('')
        #    rider_name
          rider_name_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="Athlete"' in str(columns[rider_name_column_count]):
              rider_name_column = rider_name_column_count
              # rider_name.append(columns[rider_name_column_count].text)
            else:
              'Not in column '+str(rider_name_column_count)
            rider_name_column_count = rider_name_column_count + 1
          try: rider_name.append(str(columns[rider_name_column]).split('class="athlete">')[1].split('</span')[0])
          except: rider_name.append('')
        #    race_time
          race_time_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="Time1"' in str(columns[race_time_column_count]):
              race_time_column = race_time_column_count
              # race_time.append(columns[race_time_column_count].text)
            else:
              'Not in column '+str(race_time_column_count)
            # elif 'data-label="Time"' in str(columns[race_time_column_count]):
            #   race_time.append(columns[race_time_column_count].text)
            race_time_column_count = race_time_column_count + 1
          race_time.append(columns[race_time_column].text)
        #    race_results_info
          race_results_info_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="note"' in str(columns[race_results_info_column_count]):
              race_info_column = race_results_info_column_count
            elif 'data-label="Info"' in str(columns[race_results_info_column_count]):
              race_info_column = race_results_info_column_count
            else:
              'Not in column '+str(race_results_info_column_count)
              race_info_column = 'error' 
              # race_results_info.append(columns[race_results_info_column_count].text)
            # elif 'data-label="note"' in str(columns[race_results_info_column_count]):
            #   race_results_info.append(columns[race_results_info_column_count].text)
            race_results_info_column_count = race_results_info_column_count + 1
          if race_info_column == 'error':
            race_results_info.append('Error')
          else: race_results_info.append(columns[race_info_column].text)
        #    irm
          irm_column_count = 0
          for column_count in range(0,
                                    # 7
                                    len(columns)
                                    ):
            if 'data-label="IRM"' in str(columns[irm_column_count]):
              race_irm_column = irm_column_count
              # race_irm.append(columns[irm_column_count].text)
            elif 'data-label="irm"' in str(columns[irm_column_count]):
              race_irm_column = irm_column_count
            else:
              race_irm_column = 'error'
              # race_irm.append(columns[irm_column_count].text)
            irm_column_count = irm_column_count + 1
          if race_irm_column == 'error':
            race_irm.append('Error')
          else: race_irm.append(columns[race_irm_column].text)
            
        paralympics_calendar_results = pd.DataFrame({
            'paralympics_race_id':paralympics_race_id,
            'stage_number':stage_number,
            'rank':rank,
            'nationality':nationality,
            'rider_id':rider_id,
            'rider_name':rider_name,
            'race_time':race_time,
            'race_results_info':race_results_info,
            'race_irm':race_irm
          })
        table_count_ingestion = table_count_ingestion + 1
games_results_count = games_results_count + 1

paralympics_calendar_results.to_csv(setwd+'test_csv.csv')

paralympics_calendar_results

# print(rider_name)
