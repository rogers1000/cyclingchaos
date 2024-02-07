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

# load ingestion tracker, filter to team_details files and create list of file_names and count of file_names

cycling_chaos_ingestion = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')

cci_file_name_list = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'team_details']['file_name'].to_list()

team_details_count_limit = cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'team_details']['file_name'].nunique()

team_details_count = 1

cci_file_name_list

# create empty lists for fields within dataframe output

season = []
first_cycling_team_id = []
team_name = []
uci_division_id = []
team_logo = []

# transformation loop

for team_details_count in range(0,team_details_count_limit):
#  beautiful soup to open html file
    file = open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+cci_file_name_list[team_details_count], 'r')
    file_read = file.read()
    file_soup = BeautifulSoup(file_read, "html.parser")
    file_soup_part2 = file_soup.find_all('tbody')[0]

    for row in file_soup_part2.find_all('tr'):
        columns = row.find_all('td')

        if(columns != []):
        # use file_name to work out season of data
            season.append(str(cycling_chaos_ingestion.loc[cycling_chaos_ingestion['output'] == 'team_details']['file_name']).split('_')[5])
            # 1st column is the logo
            team_logo.append(str(columns[0].find_all('span')))
            # 2nd column is the team_id and team_name
            first_cycling_team_id.append(str(columns[1].find_all('a')).split('?l=')[1].split('" style=')[0])
            team_name.append(str(columns[1].find_all('a')).split('title="')[1].split('">')[0])
            # loop count is the associated division ID
            uci_division_id.append(team_details_count)
        
        # create base df
        first_cycling_team_details_df = pd.DataFrame({
            'season':season
            ,'first_cycling_team_id':first_cycling_team_id
            ,'team_name':team_name
            ,'uci_division_id':uci_division_id
        })

# to continue the transformation loop

    team_details_count = team_details_count+1
    
first_cycling_team_details_df

# create mapping division id df

first_cycling_team_details_mapping_id_df = [1,2,3,4,5,6,7,8,9]

first_cycling_team_details_mapping_name_df = ["UCI Men's World Tour","UCI Men's Pro Conti","Men's Conti",
                                              "Men's Junior","Men's Amateur","Women's World Tour","Women's Conti",
                                              "Women's Other","Women's Junior"]

first_cycling_team_details_mapping_df = pd.DataFrame({'uci_division_id':first_cycling_team_details_mapping_id_df,
                                               'uci_division_name':first_cycling_team_details_mapping_name_df})

# join mapping df to main df and drop mapping field. Write to disk.

first_cycling_team_details_df = first_cycling_team_details_df.merge(first_cycling_team_details_mapping_df, on = 'uci_division_id')

first_cycling_team_details_df = first_cycling_team_details_df.drop('uci_division_id',axis=1)

first_cycling_team_details_df.to_csv(setwd+'first_cycling_team_details.csv',index=False)

first_cycling_team_details_df
