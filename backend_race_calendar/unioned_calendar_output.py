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

##### Calendar Unioned #####

paralympics_calendar = pd.read_csv(setwd+'paralympics_calendar_df_master.csv')
first_cycling_road_calendar = pd.read_csv(setwd+'first_cycling_calendar_df_master.csv')

calendar = pd.concat([first_cycling_road_calendar,paralympics_calendar])

calendar.to_csv(setwd+'cyclingchaos_calendar_df_master.csv')

calendar
