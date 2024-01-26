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

# load ingestion tracker, filter to startlists files and create list of file_names and count of file_names

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'startlist']['file_name'].to_list()

startlist_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'startlist']['file_name'].nunique()

startlist_count = 0

# create empty lists for fields within dataframe output

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

# transformation loop

for startlist_count in tqdm(range(0,
                                    #   2
                                      startlist_count_limit
                                      )):
# each loop needs following reset
    bib_number_order = 0
    bib_number_order_teams = -1
    bib_number_order_riders = 0
    bib_number_order_riders_team_count = 0
# open html file using beautiful soup
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[startlist_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")

    for row in file_soup.find_all('table')[2:]:
        columns = row.find_all('th')
        bib_number_order_teams = bib_number_order_teams + 1

        if(columns != []):
# use file_name to work out the season for teams data
            season_teams.append(str(cci_file_name_list[startlist_count]).split('_')[5].split('.')[0])
# use file_name to work out the race_id for teams data
            first_cycling_race_id_teams.append(str(cci_file_name_list[startlist_count]).split('_')[6].split('.')[0])
# create bib_number_order column which will be used to merge team and rider data
            bib_number_order_teams_str.append(str(bib_number_order_teams))
# column 1 of the table has team_id if it is a UCI team and None if it is invitational
            first_cycling_team_id.append(np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                         None
                         ,str(columns[0]).split('l=')[-1].split('" ')[0]))
# column 1 of the table has team_name if it is a UCI team and None if it is invitational
            team_name_invitational.append(np.where(str(columns[0]).split('l=')[-1].split('" ')[0].startswith('<th'),
                         str(columns[0]).split('l=')[-1].split('" ')[0].split('">')[-1].split('</th')[0]
                                        , None))
        
# create dataframe for startlist data on team level
            startlist_df_teams = pd.DataFrame({
                'season':season_teams
                ,'first_cycling_race_id':first_cycling_race_id_teams
                ,'bib_number_order':bib_number_order_teams_str
                ,'first_cycling_team_id':first_cycling_team_id
                ,'team_name_invitational':team_name_invitational
            })

# count of teams within the race
    startlist_df_teams['bib_number_order']
# use count of teams within race + 1 for table_count for ingestion
    startlist_df_number_of_teams_in_race = int(startlist_df_teams['bib_number_order'][-1:])+1


    for bib_number_order_riders_team_count in range(0,startlist_df_number_of_teams_in_race):
# each team is own table so needs to be split by team count to get just riders within one team for each loop
        file_soup_part2 = file_soup.find_all('tbody')[bib_number_order_riders_team_count]

        for row in file_soup_part2.find_all('tr'):
            columns = row.find_all('td')
            bib_number_order_riders = bib_number_order_riders + 1

            if(columns != []):
# use file_name to work out the season for rider data. If not possible, error.
                try:
                    season_riders.append(str(cci_file_name_list[startlist_count]).split('_')[5].split('.')[0])
                except: season_riders.append('Error')
# use file_name to work out the race_id for rider data. If not possible, error.
                try:
                    first_cycling_race_id_riders.append(str(cci_file_name_list[startlist_count]).split('_')[6].split('.')[0])
                except: first_cycling_race_id_riders.append('Error')
# create bib_number_order column which will be used to merge team and rider data
                bib_number_order_riders_team_count_str.append(str(bib_number_order_riders_team_count))
# rider bib_number is first columnn in the table
                bib_number.append(columns[0].text)
# rider_id and rider_name is the second column in the table
                first_cycling_rider_id.append(str(columns[1].find_all('a')).split('r=')[1].split('&amp')[0])
                first_cycling_rider_name.append(str(columns[1].find_all('a')).split('title="')[1].split('"><')[0])

# create dataframe for rider data
                startlist_df_riders = pd.DataFrame({
                'season':season_riders,
                'first_cycling_race_id':first_cycling_race_id_riders,
                'bib_number_order':bib_number_order_riders_team_count_str
                ,'bib_number':bib_number
                ,'first_cycling_rider_id':first_cycling_rider_id
                ,'first_cycling_rider_name':first_cycling_rider_name
                })
    startlist_count = startlist_count + 1

# merge rider and team data using season, race_id, bib_number_order

startlist_df = startlist_df_riders.merge(startlist_df_teams,on = ['season','first_cycling_race_id','bib_number_order'])

# drop bib_number_order as not relevant now its use is been done
startlist_df = startlist_df.drop(['bib_number_order'],axis=1)

startlist_df

# write startlist df to disk

startlist_df.to_csv(setwd+'startlist_df.csv',index=False)
