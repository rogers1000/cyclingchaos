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

### Team Details DF creation ###

team_details_df = pd.DataFrame(columns=['season','team_id','team_name'])

season = 2023

uci_division_extract = 0

for team_count in tqdm(range(0,9)):
  uci_division_extract = uci_division_extract + 1
  uci_division = np.where(uci_division_extract == 1,"Men's World Tour",
                          np.where(uci_division_extract == 2,"Men's ProConti",
                                   np.where(uci_division_extract == 3,"Men's Conti",
                                            np.where(uci_division_extract == 4,"Men's Junior",
                                                     np.where(uci_division_extract == 5,"Men's Amateur",
                                                              np.where(uci_division_extract == 6,"Women's World Tour",
                                                                       np.where(uci_division_extract == 7,"Women's Conti",
                                                                                np.where(uci_division_extract == 8,"Women's Other",
                                                                                         np.where(uci_division_extract == 9,"Women's Junior",
                                                                                                  "Error")))))))))
  time.sleep(5)
  url = 'https://firstcycling.com/team.php?d='+str(uci_division_extract)+'&y='+str(season)
  team_rider_details_df_meta = requests.get(url)
  team_rider_details_df_meta_soup = BeautifulSoup(team_rider_details_df_meta.content, "html.parser")
  team_rider_details_df_meta_soup_part2 = team_rider_details_df_meta_soup.find_all('tbody')[0]

  for row in team_rider_details_df_meta_soup_part2.find_all('tr'):
    columns = row.find_all('td')

    if(columns != []):
      season = str(season)
      team_logo = str(columns[0].find_all('span'))
      team_id = str(columns[1].find_all('a')).split('?l=')[1].split('" style=')[0]
      team_name = str(columns[1].find_all('a')).split('title="')[1].split('">')[0]
      # team_nationality = str(columns[3].find_all('span'))
      # team_bikes = columns[4].text
      # uci_points = columns[5]
      # test0 = columns[0]
      # test1 = columns[1]
      # test2 = columns[2]
      # test3 = columns[3]
      # test4 = columns[4]
      # test5 = columns[5]
      # test6 = columns[6]

      team_details_df = team_details_df.append({
        'season':season
        ,'uci_division':uci_division
        ,'team_id':team_id
        ,'team_name':team_name
        # ,'test0':test0
        # ,'test1':test1
        # ,'test2':test2
        # ,'test3':test3
        # ,'test4':test4
        # ,'test5':test5
        # ,'test6':test6
          }, ignore_index=True)
