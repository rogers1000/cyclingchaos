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

# creating dataframe with key information about each paralympics games

list_games_names = ['Toyko 2020','Rio 2016','London 2012','Beijing 2008','Athens 2004','Sydney 2000']

list_games_country_id = ['JP','BR','GB','CH','GR','AU']

list_games_unique_id = ['tokyo-2020','rio-2016','london-2012','beijing-2008','athens-2004','sydney-2000']

paralympics_games_df = pd.DataFrame({
    'games_name':list_games_names,
    'games_country':list_games_country_id,
    'games_id':list_games_unique_id
})

paralympics_games_df

ingestion_games_loop = paralympics_games_df['games_id'].nunique()

ingestion_games_loop

games_id_list = paralympics_games_df['games_id'].to_list()

games_id_list

##### Paralympics Calendar / Base Results

# make list of ingestion tracker to append during ingestions

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

games_id_list = paralympics_games_df['games_id'].to_list()

games_ingestion_count = 0

# ingestion loop

for games_ingestion_count in tqdm(range(0,6)):
# get code to sleep for 5 seconds to not overload website.
# probably should look at making this dynamic and more random
    time.sleep(5)
# url is base website + games_id + results
    url = 'https://www.paralympic.org/'+str(games_id_list[games_ingestion_count])+'/results/cycling'
    # url = 'https://www.paralympic.org/tokyo-2020/results/cycling'
    # print('test: '+url)
    # print('real: '+'https://www.paralympic.org/tokyo-2020/results/cycling')
# beautiful soup to open html file
    paralympics_calendar_meta = requests.get(url)
    paralympics_calendar_meta_soup = BeautifulSoup(paralympics_calendar_meta.content, "html.parser")
    paralympics_calendar_meta_soup_str = str(paralympics_calendar_meta_soup)
# write file name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'paralympics'+'_'+str(games_id_list[games_ingestion_count])+'.txt'
    with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(paralympics_calendar_meta_soup_str)
        writefile.close()
# append ingestion tracker list and write to disk
    cci_output.append('calendar')
    cci_output_details.append('paralympics')
    cci_file_name.append(file_name)

games_ingestion_count = games_ingestion_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
