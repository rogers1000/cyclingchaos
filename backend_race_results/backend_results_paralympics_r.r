library(tidyverse)

paralympics_results_csv <- read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/paralympics_results.csv') |>
  mutate(race_time_edit = race_time) |>
  mutate(results = case_when(
    (is.na(race_time) | race_time == '') & (is.na(race_results_info) | race_results_info == '') ~ race_irm,
    (is.na(race_time) | race_time == '') ~ race_results_info,
    .default = race_time_edit
  )) |>
  select(-c(race_time,race_irm,race_results_info,race_time_edit))
