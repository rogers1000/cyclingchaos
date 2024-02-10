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
rank = []
nationality = []
test = []

games_results_count = 0

for games_results_count in tqdm(range(
                                      0,
                                      1
                                    #   paralympics_count_limit
                                    )):
  file = open(setwd+'souped_html_txt_files/'+cci_file_name_list[games_results_count], 'r')
  file_read = file.read()
  file_soup = BeautifulSoup(file_read, "html.parser")
  table_count_ingestion = 1
  table_count_limit = len(file_soup.find_all('tbody'))
#   print(table_count_limit)

  for table_count_ingestion in range(1,
                                     2
                                    #  table_count_limit
                                     ):
    file_soup_part2 = file_soup.find_all('tbody')[table_count_ingestion]
    # print(cci_file_name_list[games_results_count])
    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
          paralympics_race_id.append(str(cci_file_name_list[games_results_count]).replace('cycling_chaos_code_results_paralympics_','').replace('.txt','').replace('_results_cycling_','_'))
          stage_number.append(table_count_ingestion)
        #    rank
          if 'data-label="Rank"' in str(columns[0]):
            rank.append(columns[0].text)
          elif 'data-label="Rank"' in str(columns[1]):
            rank.append(columns[1].text)
          elif 'data-label="Rank"' in str(columns[2]):
            rank.append(columns[2].text)
          elif 'data-label="Rank"' in str(columns[3]):
            rank.append(columns[3].text)
          elif 'data-label="Rank"' in str(columns[4]):
            rank.append(columns[4].text)
          elif 'data-label="Rank"' in str(columns[5]):
            rank.append(columns[5].text)
          elif 'data-label="Rank"' in str(columns[6]):
            rank.append(columns[6].text)
          else: rank.append('Error')
          #    nationality
          if 'data-label="NPC"' in str(columns[0]):
            nationality.append(columns[0].text)
          elif 'data-label="NPC"' in str(columns[1]):
            nationality.append(columns[1].text)
          elif 'data-label="NPC"' in str(columns[2]):
            nationality.append(columns[2].text)
          elif 'data-label="NPC"' in str(columns[3]):
            nationality.append(columns[3].text)
          elif 'data-label="NPC"' in str(columns[4]):
            nationality.append(columns[4].text)
          elif 'data-label="NPC"' in str(columns[5]):
            nationality.append(columns[5].text)
          elif 'data-label="NPC"' in str(columns[6]):
            nationality.append(columns[6].text)
          else: nationality.append('Error')
          test.append(columns[2])
        #   test5.append(columns[5])
        #   test6.append(columns[6])
            
        paralympics_calendar_results = pd.DataFrame({
            'paralympics_race_id':paralympics_race_id,
            'stage_number':stage_number,
            'rank':rank,
            'nationality':nationality
            ,'test':test,
            # ,'test1':test1
            # 'test2':test2,
            # 'test3':test3,
            # 'test4':test4,
            # 'test5':test5,
            # 'test6':test6,
          })
        table_count_ingestion = table_count_ingestion + 1
games_results_count = games_results_count + 1

paralympics_calendar_results

# print(paralympics_calendar_results['test1'][0])
