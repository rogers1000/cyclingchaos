### Import Modules ###
import pandas as pd
import numpy as np
import requests
# from google.colab import data_table
from datetime import datetime
import time
from datetime import timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup
# from google.colab import files
import os
import re
from time import sleep
from random import randrange
# data_table.enable_dataframe_formatter()

### Get Data required from startlists ###

race_results_data = pd.read_csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_RaceResults_2023.csv')

number_of_riders = race_results_data['rider_id'].nunique()

### Create DF for riders ###

rider_details_df = pd.DataFrame(columns=['first_cycling_rider_id','rider_full_name'])

rider_id_extract = -1

season = 2023

for rider_id_extract in tqdm(range(0,
                                #  1
                                 number_of_riders
                                 )):
  rider_id_extract = rider_id_extract + 1
  time.sleep(5)
  url = 'https://firstcycling.com/rider.php?r='+str(first_cycling_rider_ids[rider_id_extract])+'&y='+str(season)
  rider_details_df_meta = requests.get(url)
  rider_details_df_meta_soup = BeautifulSoup(rider_details_df_meta.content, "html.parser")

  if(columns != []):
    first_cycling_rider_id = first_cycling_rider_ids[rider_id_extract]
    rider_full_name = str(rider_details_df_meta_soup.find_all('title')).split('title>')[1].split(' | ')[0]

    rider_details_df = rider_details_df.append({
        'first_cycling_rider_id':first_cycling_rider_id
        ,'rider_full_name':rider_full_name
    }, ignore_index=True)
