library(tidyverse)

results_function <- function() {
  #results_csv <- read.csv('CyclingChaos_RaceResults.csv') |>
  results_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_results/CyclingChaos_RaceResults.csv') |>
    mutate(gc_time_leader_secs = gc_time_leader) |>
    mutate(gc_time_behind_leader_secs = case_when(position == "1" ~ "0",
                                                  position != "1" ~ str_remove(gc_time_leader_secs,'\\+ '),
                                                  .default = "0"
    )) |>
    #select(season,first_cycling_race_id,first_cycling_rider_id,position,gc_time_leader,gc_time_behind_leader_secs,gc_time_leader_secs) |>
    mutate(gc_time_behind_leader_hours = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                   .default = 0)) |>
    mutate(gc_time_behind_leader_mins = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                  .default = 0)) |>
    mutate(gc_time_behind_leader_secs = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                  .default = as.double(gc_time_behind_leader_secs))) |>
    mutate(gc_time_behind_leader = gc_time_behind_leader_hours+gc_time_behind_leader_mins+gc_time_behind_leader_secs) |>
    mutate(position_int = as.double(position)) |>
    arrange(-season,first_cycling_race_id,position_int) |>
    group_by(season,first_cycling_race_id) |>
    mutate(first_place_gc_time = gc_time_leader[1]) |>
    ungroup() |>
    mutate(gc_time_behind_leader_hours_test = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                        .default = 0)) |>
    mutate(gc_time_behind_leader_mins_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                       .default = 0)) |>
    mutate(gc_time_behind_leader_secs_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                       .default = as.double(gc_time_behind_leader_secs))) |>
    group_by(season,first_cycling_race_id) |>
    mutate(gc_time_leader_hours = case_when(str_count(gc_time_leader_secs[1][1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',1))*3600,
                                            .default = 0)) |>
    mutate(gc_time_leader_mins = case_when(str_count(gc_time_leader_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_leader_secs[1],':',1))*60,
                                           str_count(gc_time_leader_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',2))*60,
                                           .default = 0)) |>
    mutate(gc_time_leader_secs_2 = case_when(str_count(gc_time_leader_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_leader_secs[1],':',2)),
                                             str_count(gc_time_leader_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',3)),
                                             .default = as.double(gc_time_leader_secs[1]))) |>
    mutate(gc_time_leader = gc_time_leader_hours+gc_time_leader_mins+gc_time_leader_secs_2) |>
    ungroup() |>
    mutate(gc_time = gc_time_leader+gc_time_behind_leader) |>
    select(-c(gc_time_leader_hours,gc_time_leader_mins,gc_time_leader_secs_2,
              gc_time_behind_leader_hours_test,gc_time_behind_leader_mins_test,
              gc_time_behind_leader_secs_test,gc_time_behind_leader_hours,gc_time_behind_leader_mins,
              gc_time_behind_leader_secs,first_place_gc_time,gc_time_behind_leader,gc_time_leader_secs,
              gc_time_leader,future_race,X)) |>
    left_join(team_details <- team_details_function(), by = c('season','first_cycling_team_id' = "team_id")) |>
    mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
    select(-c(team_name_invitational,uci_division,race_nationality,position_int,"Unnamed..0")) |>
    relocate(team_name,.after = first_cycling_team_id) |>
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  results_function_gc_time_behind_first <- results_csv |>
    filter(!is.na(gc_time)) |>
    group_by(season,first_cycling_race_id,stage) |>
    summarise(gc_time_first = min(gc_time)) |>
    ungroup()
  
  results_csv <- results_csv |>
    left_join(results_function_gc_time_behind_first, by = c("season","first_cycling_race_id","stage")) |>
    mutate(gc_time_behind_first = gc_time - gc_time_first)
  
  results_stages_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_results/CyclingChaos_RaceResults_stages.csv') |>
    mutate(gc_time_leader_secs = gc_time_leader) |>
    mutate(gc_time_behind_leader_secs = case_when(position == "1" ~ "0",
                                                  position != "1" ~ str_remove(gc_time_leader_secs,'\\+ '),
                                                  .default = "0"
    )) |>
    #select(season,first_cycling_race_id,first_cycling_rider_id,position,gc_time_leader,gc_time_behind_leader_secs,gc_time_leader_secs) |>
    mutate(gc_time_behind_leader_hours = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                   .default = 0)) |>
    mutate(gc_time_behind_leader_mins = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                  .default = 0)) |>
    mutate(gc_time_behind_leader_secs = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                  .default = as.double(gc_time_behind_leader_secs))) |>
    mutate(gc_time_behind_leader = gc_time_behind_leader_hours+gc_time_behind_leader_mins+gc_time_behind_leader_secs) |>
    mutate(position_int = as.double(position)) |>
    arrange(-season,first_cycling_race_id,position_int) |>
    group_by(season,first_cycling_race_id) |>
    mutate(first_place_gc_time = gc_time_leader[1]) |>
    ungroup() |>
    mutate(gc_time_behind_leader_hours_test = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                        .default = 0)) |>
    mutate(gc_time_behind_leader_mins_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                       .default = 0)) |>
    mutate(gc_time_behind_leader_secs_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                       .default = as.double(gc_time_behind_leader_secs))) |>
    group_by(season,first_cycling_race_id) |>
    mutate(gc_time_leader_hours = case_when(str_count(gc_time_leader_secs[1][1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',1))*3600,
                                            .default = 0)) |>
    mutate(gc_time_leader_mins = case_when(str_count(gc_time_leader_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_leader_secs[1],':',1))*60,
                                           str_count(gc_time_leader_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',2))*60,
                                           .default = 0)) |>
    mutate(gc_time_leader_secs_2 = case_when(str_count(gc_time_leader_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_leader_secs[1],':',2)),
                                             str_count(gc_time_leader_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_leader_secs[1],':',3)),
                                             .default = as.double(gc_time_leader_secs[1]))) |>
    mutate(gc_time_leader = gc_time_leader_hours+gc_time_leader_mins+gc_time_leader_secs_2) |>
    ungroup() |>
    mutate(gc_time = gc_time_leader+gc_time_behind_leader) |>
    select(-c(gc_time_leader_hours,gc_time_leader_mins,gc_time_leader_secs_2,
              gc_time_behind_leader_hours_test,gc_time_behind_leader_mins_test,
              gc_time_behind_leader_secs_test,gc_time_behind_leader_hours,gc_time_behind_leader_mins,
              gc_time_behind_leader_secs,first_place_gc_time,gc_time_behind_leader,gc_time_leader_secs,
              gc_time_leader,X)) |>
    left_join(team_details <- team_details_function() |> mutate(team_id = as.character(team_id)), by = c('season','first_cycling_team_id' = "first_cycling_team_id")) |>
    mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
    select(-c(team_name_invitational,uci_division,race_nationality,position_int,"Unnamed..0")) |>
    relocate(team_name,.after = first_cycling_team_id) |>
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  results_stages_function_gc_time_behind_first <- results_stages_csv |>
    filter(!is.na(gc_time)) |>
    group_by(season,first_cycling_race_id,stage) |>
    summarise(gc_time_first = min(gc_time)) |>
    ungroup()
  
  results_stages_csv <- results_stages_csv |>
    left_join(results_stages_function_gc_time_behind_first, by = c("season","first_cycling_race_id","stage")) |>
    mutate(gc_time_behind_first = gc_time - gc_time_first)
  
  results_gc_stages_csv <- union_all(results_csv,results_stages_csv)
