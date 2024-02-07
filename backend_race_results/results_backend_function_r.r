library(tidyverse)

##### RESULTS FUNCTION #####

#No pre-built filters
results_function <- function() {
  # read results_csv from python transformation
  results_csv <- read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/cyclingchaos_raceresults_df_master.csv') |>
    # make data unique
    unique() |>
    # rename column for gc_time_raw
    mutate(gc_time_raw_secs = gc_time_raw) |>
    # creating time behind leader column. If gc_position is 1 then 0.
    # time_raw is normally "+ [n]" [n] meaning time behind formatted to hours:mins:seconds.
    mutate(gc_time_behind_leader_secs = case_when(gc_position == "1" ~ "0",
                                                  gc_position != "1" ~ str_remove(gc_time_raw_secs,'\\+ '),
                                                  .default = "0"
    )) |>
    # work out gc_time behind leader in hours, minutes and seconds. Convert each into seconds.
    # the only race where time is displayed properly is the leader
    # split hours:mins:seconds by the colon count.
    # for hours, check if the rider is hours behind by counting colons.
    # If yes, then only look at number of hours times by seconds in an hour (3600)
    # default is that the rider is not hours behind.
    mutate(gc_time_behind_leader_hours = case_when(str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*3600,
                                                   .default = 0)) |>
    # for minutes, check if the rider is hours behind. That will impact where to split the answer to just pull minutes behind.
    # times minutes behind by number of seconds within a minute (60)
    # default is that the rider is not minutes behind.
    mutate(gc_time_behind_leader_mins = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',1))*60,
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2))*60,
                                                  .default = 0)) |>
    # for seconds, check if the rider is hours behind, that will impact where the split the text to just pull seconds behind.
    # default is that to pull number of seconds.
    mutate(gc_time_behind_leader_secs = case_when(str_count(gc_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',2)),
                                                  str_count(gc_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(gc_time_behind_leader_secs,':',3)),
                                                  .default = as.double(gc_time_behind_leader_secs))) |>
    # add all three columns into a single column which is time behind leaders in seconds
    mutate(gc_time_behind_leader = gc_time_behind_leader_hours+gc_time_behind_leader_mins+gc_time_behind_leader_secs) |>
    # make a new column for gc_position which is an int
    mutate(gc_position_int = as.double(gc_position)) |>
    # sort by season, race and gc_position 
    arrange(-season,first_cycling_race_id,gc_position_int) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    # first row = winner. 
    mutate(first_place_gc_time = gc_time_raw[1]) |>
    ungroup() |>
    # group by individual stage (season, race_id, stage_number)
    group_by(season,first_cycling_race_id,stage_number) |>
    # the only race where time is displayed properly is the leader
    # split hours:mins:seconds by the colon count.
    # Check if the race was over an hour long. If yes, then only look at number of hours times by seconds in an hour (3600)
    # default is that race was not an hour long.
    mutate(gc_time_raw_hours = case_when(str_count(gc_time_raw_secs[1][1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',1))*3600,
                                         .default = 0)) |>
    # Check if the race was over an hour long. This looks at how to split the string to pull just the minutes column
    # If yes, then only look at number of minutes times by seconds in an hour (60)
    # default is that race was not a minute long.
    
    mutate(gc_time_raw_mins = case_when(str_count(gc_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_raw_secs[1],':',1))*60,
                                        str_count(gc_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',2))*60,
                                        .default = 0)) |>
    # for seconds, check if the race is over an hour long behind, that will impact where the split the text to just pull seconds
    # default is that to pull number of seconds.
    mutate(gc_time_raw_secs_2 = case_when(str_count(gc_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(gc_time_raw_secs[1],':',2)),
                                          str_count(gc_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(gc_time_raw_secs[1],':',3)),
                                          .default = as.double(gc_time_raw_secs[1]))) |>
    # add hours (in seconds), minutes (in seconds) and seconds of the leader together
    mutate(gc_time_raw = gc_time_raw_hours+gc_time_raw_mins+gc_time_raw_secs_2) |>
    ungroup() |>
    # gc_time is time for the leader in seconds plus the number of seconds behind the leader 
    mutate(gc_time = gc_time_raw+gc_time_behind_leader) |>
    # deselect all columns which are built to create output
    select(-c(gc_time_raw_hours,gc_time_raw_mins,gc_time_raw_secs_2,
              gc_time_behind_leader_hours,gc_time_behind_leader_mins,
              gc_time_behind_leader_secs,first_place_gc_time,gc_time_behind_leader,gc_time_raw_secs,
              gc_time_raw
              #,future_race
    )) |>
    # left join team details to get team name
    left_join(team_details <- team_details_function(), by = c('season','first_cycling_team_id' = "first_cycling_team_id")) |>
    # create a single team_name field. Teams can be created for the race and are called "Invitational Teams".
    # these teams don't therefore have a proper team_id associated with them.
    mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
    # deselect unnecesary columns
    select(-c(team_name_invitational,uci_division_name,race_nationality)) |>
    # move the newly created column for `team_name` behind `team_id`
    relocate(team_name,.after = first_cycling_team_id) |>
    # ensure that the fields are the correct type
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  # create csv which looks into how quick the first rider for each stage was.
  results_function_gc_time_behind_first <- results_csv |>
    filter(!is.na(gc_time)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(gc_time_first = min(gc_time)) |>
    ungroup()
  
  # join how quick first rider for each stage was to main results_csv
  # this is to create gc_time_behind_first field
  results_csv <- results_csv |>
    left_join(results_function_gc_time_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(gc_time_behind_first = gc_time - gc_time_first) |>
    select(-gc_time_first)
  
  ##### Stage #####
  # replicate what was produced for gc_time for stage_time.
  results_csv <- results_csv |>
    # rename column for gc_time_raw
    mutate(stage_time_raw_secs = stage_time_raw) |>
    # creating time behind leader column. If gc_position is 1 then 0.
    # time_raw is normally "+ [n]" [n] meaning time behind formatted to hours:mins:seconds.
    mutate(stage_time_behind_leader_secs = case_when(stage_position == "1" ~ "0",
                                                     stage_position != "1" ~ str_remove(stage_time_raw_secs,'\\+ '),
                                                     .default = "0"
    )) |>
    # work out stage_time behind leader in hours, minutes and seconds. Convert each into seconds.
    # the only race where time is displayed properly is the leader
    # split hours:mins:seconds by the colon count.
    # for hours, check if the rider is hours behind by counting colons.
    # If yes, then only look at number of hours times by seconds in an hour (3600)
    # default is that the rider is not hours behind.
    mutate(stage_time_behind_leader_hours = case_when(str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*3600,
                                                      .default = 0)) |>
    # for minutes, check if the rider is hours behind. That will impact where to split the answer to just pull minutes behind.
    # times minutes behind by number of seconds within a minute (60)
    # default is that the rider is not minutes behind.
    mutate(stage_time_behind_leader_mins = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',1))*60,
                                                     str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2))*60,
                                                     .default = 0)) |>
    # for seconds, check if the rider is hours behind, that will impact where the split the text to just pull seconds behind.
    # default is that to pull number of seconds.
    mutate(stage_time_behind_leader_secs = case_when(str_count(stage_time_behind_leader_secs,':') == 1 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',2)),
                                                     str_count(stage_time_behind_leader_secs,':') == 2 ~ as.double(str_split_i(stage_time_behind_leader_secs,':',3)),
                                                     .default = as.double(stage_time_behind_leader_secs))) |>
    # add all three columns into a single column which is time behind leaders in seconds
    mutate(stage_time_behind_leader = stage_time_behind_leader_hours+stage_time_behind_leader_mins+stage_time_behind_leader_secs) |>
    # make a new column for stage_position which is an int
    mutate(stage_position_int = as.double(stage_position)) |>
    # sort by season, race and gc_position 
    arrange(-season,first_cycling_race_id,stage_position_int) |>
    # group by individual stage (season, race_id, stage_number)
    group_by(season,first_cycling_race_id,stage_number) |>
    # first row = winner. 
    mutate(first_place_stage_time = stage_time_raw[1]) |>
    ungroup() |>
    # the only race where time is displayed properly is the leader
    # split hours:mins:seconds by the colon count.
    # Check if the race was over an hour long. If yes, then only look at number of hours times by seconds in an hour (3600)
    # default is that race was not an hour long.
    group_by(season,first_cycling_race_id,stage_number) |>
    # the only race where time is displayed properly is the leader
    # split hours:mins:seconds by the colon count.
    # Check if the race was over an hour long. If yes, then only look at number of hours times by seconds in an hour (3600)
    # default is that race was not an hour long.
    mutate(stage_time_raw_hours = case_when(str_count(stage_time_raw_secs[1][1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',1))*3600,
                                            .default = 0)) |>
    # Check if the race was over an hour long. This looks at how to split the string to pull just the minutes column
    # If yes, then only look at number of minutes times by seconds in an hour (60)
    # default is that race was not a minute long.
    mutate(stage_time_raw_mins = case_when(str_count(stage_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(stage_time_raw_secs[1],':',1))*60,
                                           str_count(stage_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',2))*60,
                                           .default = 0)) |>
    # for seconds, check if the race is over an hour long behind, that will impact where the split the text to just pull seconds
    # default is that to pull number of seconds.
    mutate(stage_time_raw_secs_2 = case_when(str_count(stage_time_raw_secs[1],':') == 1 ~ as.double(str_split_i(stage_time_raw_secs[1],':',2)),
                                             str_count(stage_time_raw_secs[1],':') == 2 ~ as.double(str_split_i(stage_time_raw_secs[1],':',3)),
                                             .default = as.double(stage_time_raw_secs[1]))) |>
    # add hours (in seconds), minutes (in seconds) and seconds of the leader together
    mutate(stage_time_raw = stage_time_raw_hours+stage_time_raw_mins+stage_time_raw_secs_2) |>
    ungroup() |>
    # stage_time is time for the leader in seconds plus the number of seconds behind the leader 
    mutate(stage_time = stage_time_raw+stage_time_behind_leader) |>
    # deselect all columns which are built to create output
    select(-c(stage_time_raw_hours,stage_time_raw_mins,stage_time_raw_secs_2,
              stage_time_behind_leader_hours,stage_time_behind_leader_mins,
              stage_time_behind_leader_secs,first_place_stage_time,stage_time_behind_leader,stage_time_raw_secs,
              stage_time_raw
              #,future_race
    )) |>
    # ensure that the fields are the correct type
    mutate(first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.character(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id))
  
  # create df which looks into how quick the first rider for each stage was.
  results_function_stage_time_behind_first <- results_csv |>
    filter(!is.na(stage_time)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(stage_time_first = min(stage_time)) |>
    ungroup()
  
  # join how quick first rider for each stage was to main results_csv
  # this is to create stage_time_behind_first field
  results_csv <- results_csv |>
    left_join(results_function_stage_time_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(stage_time_behind_first = stage_time - stage_time_first) |>
    select(-c(stage_time_first))
  

  results_csv <- results_csv |>
    # change type of rider_id, team_id, race_id to double.
    mutate(first_cycling_rider_id = as.double(first_cycling_rider_id)) |>
    mutate(first_cycling_team_id = as.double(first_cycling_team_id)) |>
    mutate(first_cycling_race_id = as.double(first_cycling_race_id)) |>
    # create new field which is stage_number as int
    mutate(stage_number_int = as.double(stage_number)) |>
    arrange(season,first_cycling_race_id,stage_number) |>
    # group by rider within a race (season, race_id, rider_id)
    group_by(season,first_cycling_race_id,first_cycling_rider_id) |>
    # work out stage_number_order by doing cumsum of stages
    mutate(stage_number_order = 1) |>
    mutate(stage_number_order = cumsum(stage_number_order)) |>
    # create field that makes gc_time for each stage
    # ngl so confused
    mutate(gc_time_stage = case_when(
      stage_number == "GC" ~ gc_time,
      # Missing Stages from Transform
      stage_number_order < stage_number ~ NA,
      # If first stage of stage race then gc_time
      stage_number_order == 1 ~ gc_time,
      # GC time minus previous stage gc time
      stage_number_order-lag(stage_number_order,1) == 1 ~ gc_time - lag(gc_time,1),
      .default = NA
    )) |>
    # gc_time_bonus is stage_time minus gc_time for each stage
    mutate(gc_time_bonus = stage_time-gc_time_stage) |>
    ungroup() |>
    arrange(season,start_date,end_date,first_cycling_race_id,stage_number,stage_position_int,gc_position_int) |>
    # deselect fields used to build output
    select(-c(gc_position_int,stage_position_int))
  
  # create df which looks into how quick the first rider for each stage was for gc_time and how many bonus seconds the best rider got on the stage
  results_function_gc_time_stage_behind_first <- results_csv |>
    filter(!is.na(gc_time_stage)) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    summarise(gc_time_stage_first = min(gc_time_stage),
              gc_time_bonus_first = max(gc_time_bonus)) |>
    ungroup()
  
  # join how quick first rider for each stage was to main results_csv
  # this is to create gc_time_behind_first field
  results_csv <- results_csv |>
    left_join(results_function_gc_time_stage_behind_first, by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(gc_time_stage_behind_first = gc_time_stage - gc_time_stage_first,
           gc_time_bonus_behind_first = gc_time_bonus_first - gc_time_bonus) |>
    select(-c(gc_time_stage_first))
  
  # create gc_time for each stage position
  # create gc_time_bonus for each stage position
  results_csv <- results_csv |>
    # GC Time Stage
    arrange(season,first_cycling_race_id,stage_number,gc_time_stage,stage_position) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(gc_time_stage_position = row_number()) |>
    ungroup() |>
    # GC Time Bonus
    arrange(season,first_cycling_race_id,stage_number,-gc_time_bonus,gc_time_stage,stage_position) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    mutate(gc_time_bonus_position = row_number()) |>
    ungroup() |>
    # remove rider_name and join in name mapping function to get most recent name for the rider.
    select(-first_cycling_rider_name) |>
    left_join(rider_name_mapping_df_function() |> select(first_cycling_rider_id,first_cycling_rider_name), by = "first_cycling_rider_id")
  
}
