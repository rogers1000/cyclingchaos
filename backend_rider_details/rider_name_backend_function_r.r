library(tidyverse)
# No function filters
rider_name_mapping_df_function <- function() {
  # read csv from online github
  df <- read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/cyclingchaos_raceresults_df_master.csv') |>
    # select only fields relevant
    # rider_id, name and end_date to see when the date for if the name changes.
    select(first_cycling_rider_id,first_cycling_rider_name,end_date) |>
    # make csv distinct to fields selected
    unique() |>
    # group_by rider_id and create most recent race for each rider
    group_by(first_cycling_rider_id) |>
    mutate(last_race_for_rider = max(end_date)) |>
    # ungroup and mutate so if last_race for rider = end_date then use that rider id or filter out data
    ungroup() |>
    mutate(first_cycling_rider_name_latest = case_when(last_race_for_rider == end_date ~ first_cycling_rider_name,
                                                       .default = "filter_out")) |>
    filter(first_cycling_rider_name_latest != "filter_out") |>
    # leave csv with rider_id and rider_name
    select(first_cycling_rider_id, first_cycling_rider_name = first_cycling_rider_name_latest)
}
