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

setwd = '/Users/zacrogers/Documents/cycling_chaos/python_code/'

season = 2023
fc_division_count = 1
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

for fc_division_count in tqdm(range(1,
                                          10
                                        )):
    time.sleep(5)
    url = 'https://firstcycling.com/team.php?y='+str(season)+'&d='+str(fc_division_count)
    teamdetails_meta = requests.get(url)
    teamdetails_meta_soup = BeautifulSoup(teamdetails_meta.content, "html.parser")
    teamdetails_meta_soup_str = str(teamdetails_meta_soup)
    file_name = 'cycling_chaos_code'+'_'+'team_details'+'_'+'all'+'_'+str(season)+'_'+str(fc_division_count)+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
    # with open(r'/Users/zacrogers/Documents/cycling_chaos/python_code/calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(teamdetails_meta_soup_str)
        writefile.close()
    cci_output.append('team_details')
    cci_output_details.append('all')
    cci_file_name.append(file_name)

    print('Ingested #'+str(fc_division_count+1)+' '+file_name)

    fc_division_count = fc_division_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
