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

cci_output = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output'].to_list()
cci_output_details = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['output_details'].to_list()
cci_file_name = pd.read_csv(setwd+'cycling_chaos_ingestion_df_master.csv')['file_name'].to_list()

season_start = 2023
season_end = 2023
page_count = 1

# page_limit is manual process that takes number of pages that filter within url pulls out.
# needs to be automated using file_soup output

page_limit = 4

for page_count in tqdm(range(1,page_limit)):
    time.sleep(5)
    url = 'https://www.britishcycling.org.uk/events/results?&myevents=0&fromdate=01%2F01%2F2023&startdate=01%2F01%2F2023&todate=31%2F12%2F'+str(season_start)+'&enddate=31%2F12%2F'+str(season_end)+'&day_of_week%5B0%5D=1&day_of_week%5B1%5D=2&day_of_week%5B2%5D=3&day_of_week%5B3%5D=4&day_of_week%5B4%5D=5&day_of_week%5B5%5D=6&day_of_week%5B6%5D=7&zuv_bc_event_filter_id%5B0%5D=21&zuv_bc_race_category_id%5B0%5D=9&zuv_bc_race_category_id%5B1%5D=13&zuv_bc_race_category_id%5B2%5D=9&zuv_bc_race_category_id%5B3%5D=13&series_only=0&online_entry_only=0&gender=&frontend=1&resultsperpage=100&show=results_only&search_type=results&page='+str(page_count)
    british_calendar_meta = requests.get(url)
    british_calendar_meta_soup = BeautifulSoup(british_calendar_meta.content, "html.parser")
    british_calendar_meta_soup_str = str(british_calendar_meta_soup)
    file_name = 'cycling_chaos_code'+'_'+'calendar'+'_'+'british'+'_'+str(page_count)+'.txt'
    # write file to disk
    with open(setwd+'souped_html_txt_files/'+file_name, 'w') as writefile:
        writefile.write(british_calendar_meta_soup_str)
        writefile.close()
    # add ingest details to ingestion master tracker
    cci_output.append('calendar')
    cci_output_details.append('British')
    cci_file_name.append(file_name)
    # ensures that code is working and ingesting properly.
    print('Ingested '+file_name)

page_count = page_count + 1

    # make ingestion master lists back into a dataframe and save the new csv
cycling_chaos_ingestion = pd.DataFrame({'output':cci_output, 'output_details':cci_output_details, 'file_name':cci_file_name})
cycling_chaos_ingestion.to_csv(setwd+'cycling_chaos_ingestion_df.csv', index=False)

# check ingestion master is working
print(cycling_chaos_ingestion)
