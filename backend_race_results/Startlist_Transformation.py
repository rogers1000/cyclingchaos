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

##### Startlist Transformation #####

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'startlist']['file_name'].to_list()

startlist_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'startlist']['file_name'].nunique()

startlist_count = 0

cci_file_name_list

bib_number = []
first_cycling_rider_id = []
first_cycling_rider_name = []
first_cycling_team_id = []
team_name_invitational = []
season_teams = []
season_riders = []
first_cycling_race_id_teams = []
first_cycling_race_id_riders = []
bib_number_order_teams_str = []
bib_number_order_riders_team_count_str = []

for startlist_count in tqdm(range(0,
                                    #   2
                                      startlist_count_limit
                                      )):
    ib_number_order = 0
    bib_number_order_teams = -1
    bib_number_order_riders = 0
    bib_number_order_riders_team_count = 0
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[startlist_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    
    for row in file_soup.find_all('table')[2:]:
        columns = row.find_all('th')
        bib_number_order_teams = bib_number_order_teams + 1

        if(columns != []):
            season_teams.append(str(cci_file_name_list[startlist_count]).split('_')[5].split('.')[0])
            first_cycling_race_id_teams.append(str(cci_file_name_list[startlist_count]).split('_')[6].split('.')[0])
            bib_number_order_teams_str.append(str(bib_number_order_teams))
            first_cycling_team_id.append(np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                        #  str(columns[0]).split('l=')[-1].split('" ')[0].split('">')[-1].split('</th')[0]
                         None
                         ,str(columns[0]).split('l=')[-1].split('" ')[0]))
            team_name_invitational.append(np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                         str(columns[0]).split('l=')[-1].split('" ')[0].split('">')[-1].split('</th')[0]
                        #  ,str(columns[0]).split('l=')[-1].split('" ')[0]
                                        , None))
        
            startlist_df_teams = pd.DataFrame({
                'season':season_teams
                ,'first_cycling_race_id':first_cycling_race_id_teams
                ,'bib_number_order':bib_number_order_teams_str
                ,'first_cycling_team_id':first_cycling_team_id
                ,'team_name_invitational':team_name_invitational
            })

    # startlist_count = startlist_count + 1

    startlist_df_teams['bib_number_order']

    startlist_df_number_of_teams_in_race = int(startlist_df_teams['bib_number_order'][-1:])+1

    # startlist_count = -1

    for bib_number_order_riders_team_count in range(0,startlist_df_number_of_teams_in_race):
        file_soup_part2 = file_soup.find_all('tbody')[bib_number_order_riders_team_count]

        for row in file_soup_part2.find_all('tr'):
            columns = row.find_all('td')
            bib_number_order_riders = bib_number_order_riders + 1

            if(columns != []):
                try:
                    season_riders.append(str(cci_file_name_list[startlist_count]).split('_')[5].split('.')[0])
                except: season_riders.append('Error')
                try:
                    first_cycling_race_id_riders.append(str(cci_file_name_list[startlist_count]).split('_')[6].split('.')[0])
                except: first_cycling_race_id_riders.append('Error')
                bib_number_order_riders_team_count_str.append(str(bib_number_order_riders_team_count))
                bib_number.append(columns[0].text)
                first_cycling_rider_id.append(str(columns[1].find_all('a')).split('r=')[1].split('&amp')[0])
                first_cycling_rider_name.append(str(columns[1].find_all('a')).split('title="')[1].split('"><')[0])

                startlist_df_riders = pd.DataFrame({
                'season':season_riders,
                'first_cycling_race_id':first_cycling_race_id_riders,
                'bib_number_order':bib_number_order_riders_team_count_str
                ,'bib_number':bib_number
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'first_cycling_rider_name':first_cycling_rider_name
                })
    startlist_count = startlist_count + 1

startlist_df = startlist_df_riders.merge(startlist_df_teams,on = ['season','first_cycling_race_id','bib_number_order'])

startlist_df = startlist_df.drop(['bib_number_order'],axis=1)

startlist_df

startlist_df.to_csv('startlist_df.csv',index=False)
