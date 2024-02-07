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

# setwd = working directory

# set season you want to ingest
season = 2023
# fc_division_id starts at 1
fc_division_count = 1
# create lists of preingested data to append to during the ingestion process
cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

# ingestion loop

# there are 10 divisions within first_cycling
for fc_division_count in tqdm(range(0,
                                          9
                                        )):
    # get code to sleep for 5 seconds to not overload website.
    # probably should look at making this dynamic and more random
    time.sleep(5)
    # url = base website + season + '&d=' + division_id. 'd=' means division
    url = 'https://firstcycling.com/team.php?y='+str(season)+'&d='+str(fc_division_count)
    # beautiful soup to ingest html file
    teamdetails_meta = requests.get(url)
    teamdetails_meta_soup = BeautifulSoup(teamdetails_meta.content, "html.parser")
    teamdetails_meta_soup_str = str(teamdetails_meta_soup)
    # create file_name and write to disk
    file_name = 'cycling_chaos_code'+'_'+'team_details'+'_'+'all'+'_'+str(season)+'_'+str(fc_division_count)+'.txt'
    with open(setwd+'calendar_ingestion_files/souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(teamdetails_meta_soup_str)
        writefile.close()
    # append ingestion tracker lists, convert to dataframe and write to disk
    cci_output.append('team_details')
    cci_output_details.append('all')
    cci_file_name.append(file_name)

    print('Ingested #'+str(fc_division_count+1)+' '+file_name)

    fc_division_count = fc_division_count + 1

cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})

cycling_chaos_ingestion = cycling_chaos_ingestion.drop_duplicates()

cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df_master.csv', index=False)

print(cycling_chaos_ingestion)
