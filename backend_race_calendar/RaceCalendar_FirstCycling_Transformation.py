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

##### Transforming Calendar Ingest #####

# Making a list of files needing to be transformed

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name'].to_list()

calendar_ingestion_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name'].nunique()

calendar_ingestion_count = 0

# print(cci_file_name_list[calendar_ingestion_count])

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




for calendar_ingestion_count in range(0,22):
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[calendar_ingestion_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[-1]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
            year.append(str(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['file_name']).split('_')[5])
            gender.append(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'calendar']['output_details'][calendar_ingestion_count])
            category.append('Road')
            calendar_ingestion_count_str.append(str(calendar_ingestion_count))
            first_cycling_race_id.append(str(columns[2].find_all('a')).split('r=')[1].split('&amp')[0])
            race_name.append(str(columns[2].find_all('a')).split('title="')[1].split('">')[0])
            race_nationality.append(str(columns[2].find_all("span")).split("flag-")[1].split('"><')[0].upper())
            uci_race_classification.append(columns[1].text)
            stage_race_boolean.append(np.where(columns[1].text.startswith('2'),"Stage Race","One Day"))
            # start_date.append(year[-1])
            start_date.append(year[-1]+'/'+columns[0].text.split('-')[0].split('.')[-1]+'/'+columns[0].text.split('-')[0].split('.')[0])
            end_date.append(year[-1]+'/'+columns[0].text.split('-')[-1].split('.')[-1]+'/'+columns[0].text.split('-')[-1].split('.')[0])
            # test.append(calendar_ingestion_count)

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
            
    calendar_ingestion_count = calendar_ingestion_count + 1

road_calendar_df = road_calendar_df.drop_duplicates(subset=['season','first_cycling_race_id'])

road_calendar_df.to_csv(setwd+'first_cycling_calendar_df.csv', index=False)
road_calendar_df            
# print(road_calendar_df['season'])
# print(calendar_ingestion_count)
