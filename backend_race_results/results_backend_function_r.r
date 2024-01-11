library(tidyverse)

results_function <- function() {
  results_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_results/CyclingChaos_RaceResults_df_master.csv') |>
    unique() |>
    mutate(gc_time_raw_secs = gc_time_raw) |>
    mutate(gc_time_behind_leader_secs = case_when(gc_position == "1" ~ "0",
                                                  gc_position != "1" ~ str_remove(gc_time_raw_secs,'\\+ '),
                                                  .default = "0"
    )) |>
    mutate(gc_time_behind_leader_hours = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                   .default = 0)) |>
    mutate(gc_time_behind_leader_mins = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                  .default = 0)) |>
    mutate(gc_time_behind_leader_secs = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                  .default = as.double(gc_time_behind_leader_secs))) |>
    mutate(gc_time_behind_leader = gc_time_behind_leader_hours+gc_time_behind_leader_mins+gc_time_behind_leader_secs) |>
    mutate(gc_position_int = as.double(gc_position)) |>
    arrange(-season,first_cycling_race_id,gc_position_int) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(first_place_gc_time = gc_time_raw[1]) |>
    ungroup() |>
    mutate(gc_time_behind_leader_hours_test = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                        .default = 0)) |>
    mutate(gc_time_behind_leader_mins_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                       .default = 0)) |>
    mutate(gc_time_behind_leader_secs_test = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                       str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                       .default = as.double(gc_time_behind_leader_secs))) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(gc_time_raw_hours = case_when(str_count(gc_time_raw_secs[1][1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',1))*3600,
                                         .default = 0)) |>
    mutate(gc_time_raw_mins = case_when(str_count(gc_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_raw_secs[1],':',1))*60,
                                        str_count(gc_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',2))*60,
                                        .default = 0)) |>
    mutate(gc_time_raw_secs_2 = case_when(str_count(gc_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_raw_secs[1],':',2)),
                                          str_count(gc_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',3)),
                                          .default = as.double(gc_time_raw_secs[1]))) |>
    mutate(gc_time_raw = gc_time_raw_hours+gc_time_raw_mins+gc_time_raw_secs_2) |>
    ungroup() |>
    mutate(gc_time = gc_time_raw+gc_time_behind_leader) |>
    select(-c(gc_time_raw_hours,gc_time_raw_mins,gc_time_raw_secs_2,
              gc_time_behind_leader_hours_test,gc_time_behind_leader_mins_test,
              gc_time_behind_leader_secs_test,gc_time_behind_leader_hours,gc_time_behind_leader_mins,
              gc_time_behind_leader_secs,first_place_gc_time,gc_time_behind_leader,gc_time_raw_secs,
              gc_time_raw
              #,future_race
    )) |>
    left_join(team_details <- team_details_function(), by = c('season','first_cycling_team_id' = "first_cycling_team_id")) |>
    mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
    select(-c(team_name_invitational,uci_division_name,race_nationality)) |>
    relocate(team_name,.after = first_cycling_team_id) |>
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  results_function_gc_time_behind_first <- results_csv |>
    filter(!is.na(gc_time)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(gc_time_first = min(gc_time)) |>
    ungroup()
  
  results_csv <- results_csv |>
    left_join(results_function_gc_time_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(gc_time_behind_first = gc_time - gc_time_first) |>
    select(-gc_time_first)
  
  ##### Stage #####
  results_csv <- results_csv |>
    mutate(stage_time_raw_secs = stage_time_raw) |>
    mutate(stage_time_behind_leader_secs = case_when(stage_position == "1" ~ "0",
                                                     stage_position != "1" ~ str_remove(stage_time_raw_secs,'\\+ '),
                                                     .default = "0"
    )) |>
    mutate(stage_time_behind_leader_hours = case_when(str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*3600,
                                                      .default = 0)) |>
    mutate(stage_time_behind_leader_mins = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*60,
                                                     str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2))*60,
                                                     .default = 0)) |>
    mutate(stage_time_behind_leader_secs = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2)),
                                                     str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',3)),
                                                     .default = as.double(stage_time_behind_leader_secs))) |>
    mutate(stage_time_behind_leader = stage_time_behind_leader_hours+stage_time_behind_leader_mins+stage_time_behind_leader_secs) |>
    mutate(stage_position_int = as.double(stage_position)) |>
    arrange(-season,first_cycling_race_id,stage_position_int) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(first_place_stage_time = stage_time_raw[1]) |>
    ungroup() |>
    mutate(stage_time_behind_leader_hours_test = case_when(str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*3600,
                                                           .default = 0)) |>
    mutate(stage_time_behind_leader_mins_test = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*60,
                                                          str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2))*60,
                                                          .default = 0)) |>
    mutate(stage_time_behind_leader_secs_test = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2)),
                                                          str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',3)),
                                                          .default = as.double(stage_time_behind_leader_secs))) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(stage_time_raw_hours = case_when(str_count(stage_time_raw_secs[1][1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',1))*3600,
                                            .default = 0)) |>
    mutate(stage_time_raw_mins = case_when(str_count(stage_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(stage_time_raw_secs[1],':',1))*60,
                                           str_count(stage_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',2))*60,
                                           .default = 0)) |>
    mutate(stage_time_raw_secs_2 = case_when(str_count(stage_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(stage_time_raw_secs[1],':',2)),
                                             str_count(stage_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',3)),
                                             .default = as.double(stage_time_raw_secs[1]))) |>
    mutate(stage_time_raw = stage_time_raw_hours+stage_time_raw_mins+stage_time_raw_secs_2) |>
    ungroup() |>
    mutate(stage_time = stage_time_raw+stage_time_behind_leader) |>
    select(-c(stage_time_raw_hours,stage_time_raw_mins,stage_time_raw_secs_2,
              stage_time_behind_leader_hours_test,stage_time_behind_leader_mins_test,
              stage_time_behind_leader_secs_test,stage_time_behind_leader_hours,stage_time_behind_leader_mins,
              stage_time_behind_leader_secs,first_place_stage_time,stage_time_behind_leader,stage_time_raw_secs,
              stage_time_raw
              #,future_race
    )) |>
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  results_function_stage_time_behind_first <- results_csv |>
    filter(!is.na(stage_time)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(stage_time_first = min(stage_time)) |>
    ungroup()
  
  results_csv <- results_csv |>
    left_join(results_function_stage_time_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(stage_time_behind_first = stage_time - stage_time_first) |>
    select(-c(stage_time_first))
  
  results_csv <- results_csv |>
    mutate(first_cycling_rider_id = as.double(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.double(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.double(first_cycling_race_id)) |>
    mutate(stage_number_int = as.double(stage_number)) |>
    arrange(season,first_cycling_race_id,stage_number) |>
    group_by(season,first_cycling_race_id,first_cycling_rider_id) |>
    mutate(stage_number_order = 1) |>
    mutate(stage_number_order = cumsum(stage_number_order)) |>
    mutate(gc_time_stage = case_when(
      # Missing Stages from Transform
      stage_number_order < stage_number ~ NA,
      # If first stage of stage race then gc_time
      stage_number_order == 1 ~ gc_time,
      # GC time minus previous stage gc time
      stage_number_order-lag(stage_number_order,1) == 1 ~ gc_time - lag(gc_time,1),
      .default = NA
    )) |>
    mutate(gc_time_bonus = stage_time-gc_time_stage) |>
    ungroup() |>
    arrange(season,start_date,end_date,first_cycling_race_id,stage_number,stage_position_int,gc_position_int) |>
    select(-c(gc_position_int,stage_position_int))
  
  results_function_gc_time_stage_behind_first <- results_csv |>
    filter(!is.na(gc_time_stage)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(gc_time_stage_first = min(gc_time_stage)) |>
    ungroup()
  
  results_csv <- results_csv |>
    left_join(results_function_gc_time_stage_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(gc_time_stage_behind_first = gc_time_stage - gc_time_stage_first) |>
    select(-c(gc_time_stage_first))
  
  results_csv <- results_csv |>
    arrange(season,first_cycling_race_id,stage_number,gc_time_stage,stage_position) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(gc_time_stage_position = row_number()) |>
    select(-first_cycling_rider_name) |>
    left_join(rider_name_mapping_df_function() |> select(first_cycling_rider_id,first_cycling_rider_name), by = "first_cycling_rider_id")
  
}
