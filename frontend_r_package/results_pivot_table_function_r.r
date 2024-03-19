library(tidyverse)
library(gt)
library(gtExtras)
library(ggplot2)
library(ggtext)

##### RESULTS_PIVOT #####
# pre-built filters for low-code capability
results_pivot <- function(season_function,gender_function,detail_slicer_function,value_from_function,race_filter_function,uci_race_classification_function,
                          race_location_function,stage_race_function,oneday_bonus_function, head_count_function,template_user_function) {
  # making Stages function within race_filter_function not dependent on capitalisation
  race_filter_function <- case_when(str_detect(str_to_title(race_filter_function),'Stages') == TRUE ~ str_to_title(race_filter_function),
            .default = race_filter_function)
  # making gender all lowercase
  gender_function <- str_to_lower(gender_function)
  # making detail_slicer_function (rider/team) into title case
  detail_slicer_function <- str_to_title(detail_slicer_function)
  # making value_from_function into upper case
  value_from_function <- str_to_upper(value_from_function)
  
  
  
  # read cleaned results csv from github
  results_pivot_filters <- read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/results.csv') |>
    select(-X) |>
  #results_pivot_filters <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/results.csv') |>
    # filter to selected season and gender
    filter(season == season_function
           , gender == gender_function
    ) |>
    # join in calendar csv to add in capability for filtering to race_nationality and race_tags
    left_join(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,race_nationality,race_tags) |> unique(), by = c("season","first_cycling_race_id")) |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,race_nationality,race_tags) |> unique(), by = c("season","first_cycling_race_id")) |>
    # uci_race_classification filter
    mutate(uci_race_classification_filter = case_when(str_detect(uci_race_classification,'UWT') & uci_race_classification_function == 'World Tour' ~ 1,
                                                      str_detect(uci_race_classification,'WWT') & uci_race_classification_function == 'World Tour' ~ 1,
                                                      uci_race_classification_function == "" ~ 1,
                                                      .default = 0)) |>
    filter(uci_race_classification_filter == 1) |>
    # race_nationality filter
    mutate(race_location_filter = case_when(race_location_function == race_nationality ~ 1,
                                            #race_location_function == race_location_id ~ 1,
                                            #race_location_function == race_location_name ~ 1,
                                            race_location_function == "" ~ 1,
                                            .default = 0)) |>
    filter(race_location_filter == 1) |>
    # stage race or one day races only filter
    mutate(stage_race_filter = case_when(stage_race_function == "Stage Race" ~ 1,
                                         stage_race_function == "One Day" ~ 1,
                                         stage_race_function == "" ~ 1,
                                         .default = 0)) |>
    filter(stage_race_filter == 1) |>
    ### Making Position data numeric for sorting purposes
    mutate(stage_position_edit = case_when(stage_position == "OOT" ~ 1000,
                                           stage_position == "DNF" ~ 1100,
                                           stage_position == "DNS" ~ 1200,
                                           stage_position == "DSQ" ~ 1300,
                                           .default = as.double(stage_position))) |>
    mutate(gc_time_stage_position_edit = case_when(gc_time_stage_position == "OOT" ~ 1000,
                                                   gc_time_stage_position == "DNF" ~ 1100,
                                                   gc_time_stage_position == "DNS" ~ 1200,
                                                   gc_time_stage_position == "DSQ" ~ 1300,
                                                   .default = as.double(gc_time_stage_position))) |>
    mutate(gc_time_bonus_position_edit = case_when(gc_time_stage_position == "OOT" ~ 1000,
                                                   gc_time_stage_position == "DNF" ~ 1100,
                                                   gc_time_stage_position == "DNS" ~ 1200,
                                                   gc_time_stage_position == "DSQ" ~ 1300,
                                                   .default = as.double(gc_time_bonus_position))) |>
    mutate(gc_position_edit = case_when(gc_position == "OOT" ~ 1000,
                                        gc_position == "DNF" ~ 1100,
                                        gc_position == "DNS" ~ 1200,
                                        gc_position == "DSQ" ~ 1300,
                                        .default = as.double(gc_position))) |>
    mutate(gc_time_bonus_oneday = case_when(stage_position == 1 & stage_race_boolean == "One Day" ~ 10 * oneday_bonus_function,
                                            stage_position == 2 & stage_race_boolean == "One Day" ~ 6 * oneday_bonus_function,
                                            stage_position == 3 & stage_race_boolean == "One Day" ~ 4 * oneday_bonus_function,
                                            .default = 0)) |>
    # merging traditional gc_time_bonus with one day bonus time
    mutate(gc_time_bonus = gc_time_bonus+gc_time_bonus_oneday) |>
    # updating gc_time_stage_behind_first to reflect new bonus seconds
    mutate(gc_time = gc_time-gc_time_bonus_oneday) |>
    mutate(gc_time_stage = gc_time_stage-gc_time_bonus_oneday) |>
    mutate(gc_time_stage_behind_first = gc_time_stage_behind_first-gc_time_bonus_oneday) |>
    mutate(gc_time_behind_first = gc_time_behind_first-gc_time_bonus_oneday) |>
    mutate(gc_time_bonus_behind_first = gc_time_bonus_behind_first-gc_time_bonus_oneday) |>
    group_by(season,first_cycling_race_id,stage_number) |>
    # if min time is below 0, add the difference to everyone
    mutate(gc_time_stage = case_when(min(gc_time_stage, na.rm = TRUE) < 0 ~ min(gc_time_stage, na.rm = TRUE)*-1+gc_time_stage,
                                     .default = gc_time_stage)) |>
    # if min time is below 0, add the difference to everyone
    mutate(gc_time_stage_behind_first = case_when(min(gc_time_stage_behind_first, na.rm = TRUE) < 0 ~ min(gc_time_stage_behind_first, na.rm = TRUE)*-1+gc_time_stage_behind_first,
                                                  .default = gc_time_stage_behind_first)) |>
    # if min time is below 0, add the difference to everyone
    mutate(gc_time = case_when(min(gc_time, na.rm = TRUE) < 0 ~ min(gc_time, na.rm = TRUE)*-1+gc_time,
                               .default = gc_time)) |>
    # if min time is below 0, add the difference to everyone
    mutate(gc_time_behind_first = case_when(min(gc_time_behind_first, na.rm = TRUE) < 0 ~ min(gc_time_behind_first, na.rm = TRUE)*-1+gc_time_behind_first,
                                            .default = gc_time_behind_first)) |>
    # if min time is below 0, add the difference to everyone
    mutate(gc_time_bonus_behind_first = case_when(min(gc_time_bonus_behind_first, na.rm = TRUE) < 0 ~ min(gc_time_bonus_behind_first, na.rm = TRUE)*-1+gc_time_bonus_behind_first,
                                                  .default = gc_time_bonus_behind_first)) |>
    ungroup()
  
  # if looking at riders, check rider is in the race
  results_pivot_filters_rider_calendar <- dplyr::pull(results_pivot_filters |> 
                                                        mutate(race_filter_rider = case_when(str_detect(race_filter_function,"Rider")
                                                                                             & first_cycling_rider_id == str_split_i(race_filter_function," - ",-1) ~ 1,
                                                                                             .default = 0)) |>
                                                        filter(race_filter_rider == 1),first_cycling_race_id) |> unique()
  # if looking at teams, check team is in the race
  results_pivot_filters_team_calendar <- dplyr::pull(results_pivot_filters |> 
                                                       mutate(race_filter_team = case_when(str_detect(race_filter_function,"Team")
                                                                                           & first_cycling_team_id == str_split_i(race_filter_function," - ",-1) ~ 1,
                                                                                           .default = 0)) |>
                                                       filter(race_filter_team == 1),first_cycling_race_id) |> unique()
  
  
  results_pivot_filters <- results_pivot_filters |>
    # Don't want to include GC results from Stage Races
    filter(!(stage_number == "GC" & stage_race_boolean == "Stage Race")) |>
    # Race Filter - Race Collection
    mutate(race_filter_race_collection = case_when(race_filter_function == "" ~ 1,
                                                   str_detect(race_tags,race_filter_function) ~ 1,
                                                   .default = 0)) |>
    # Race Filter - Rider Filter
    mutate(race_filter_rider = case_when(first_cycling_race_id %in% results_pivot_filters_rider_calendar ~ 1,
                                         .default = 0)) |>
    # Race Filter - Team Filter
    mutate(race_filter_team = case_when(first_cycling_race_id %in% results_pivot_filters_team_calendar ~ 1,
                                        .default = 0)) |>
    mutate(stage_or_gc_filter = case_when(str_detect(race_filter_function,"Stages") & (stage_number != "GC") & (first_cycling_race_id == str_split_i(race_filter_function," - ",-1)) ~ 1,
                                          (!str_detect(race_filter_function,"Stages")) & (stage_number == "GC") & (first_cycling_race_id == str_split_i(race_filter_function," - ",-1)) ~ 1,
                                          .default = 0)) |>
    filter(race_filter_race_collection == 1 | race_filter_rider == 1 | race_filter_team == 1 | stage_or_gc_filter == 1) |>
    #filter(stage_or_gc_filter == 1) |>
    mutate(pivot_id = case_when(detail_slicer_function == "Team" ~ first_cycling_team_id,
                                detail_slicer_function == "Rider" ~ first_cycling_rider_id)) |>
    mutate(pivot_name = case_when(detail_slicer_function == "Team" ~ team_name,
                                  detail_slicer_function == "Rider" ~ first_cycling_rider_name))
  
  # count how many races are included in the selection
  races_selected <- sum(dplyr::pull(results_pivot_filters |>
                                      select(first_cycling_race_id,stage_number) |>
                                      unique() |>
                                      summarise(count = n()),count))
  
  # check how many the rider/team has ridden out of the races in the selection
  results_pivot_races_count <- results_pivot_filters |>
    group_by(pivot_id) |>
    summarise(races_count = n_distinct(paste0(first_cycling_race_id,"_",stage_number)))
  
  # looking at totals metadata
  results_pivot_sort_totals <- results_pivot_filters |>
    # only look at racers who finished the stage
    filter(stage_position_edit < 1000) |>
    # count number of stage victories, top 3s, top 5s, top 10s
    mutate(victory = case_when(stage_position_edit == 1 ~ 1,
                               .default = 0),
           podium = case_when(stage_position_edit < 4 ~ 1,
                              .default = 0),
           topfive = case_when(stage_position_edit < 6 ~ 1,
                               .default = 0),
           topten = case_when(stage_position_edit < 11 ~ 1,
                              .default = 0)) |>
    # Need to calculate best stage position, stage_time, stage_time_from_leader
    # gc_stage_time position, gc_stage_time, gc_stage_time_from_leader
    # gc_position, gc_time, gc_time_from_leader
    group_by(pivot_id,pivot_name,season,first_cycling_race_id,stage_number,stage_number_order) |>
    summarise(stage_position_edit = min(stage_position_edit),
              stage_time = min(stage_time),
              stage_time_behind_first = min(stage_time_behind_first),
              gc_time_stage_position_edit = min(gc_time_stage_position_edit),
              gc_time_stage = min(gc_time_stage),
              gc_time_stage_behind_first = min(gc_time_stage_behind_first),
              gc_position_edit = min(gc_position_edit),
              gc_time = min(gc_time),
              gc_time_from_leader = min(gc_time_behind_first),
              gc_time_bonus = max(gc_time_bonus),
              gc_time_bonus_position_edit = min(gc_time_bonus_position_edit),
              gc_time_bonus_behind_first = min(gc_time_bonus_behind_first),
              kom_position = min(kom_position),
              kom_score_stage_position = min(kom_score_stage_position),
              kom_score_stage = max(kom_score_stage),
              kom_score_stage_behind_first = min(kom_score_stage_behind_first),
              points_position = min(points_position),
              points_score_stage_position = min(points_score_stage_position),
              points_score_stage = max(points_score_stage),
              points_score_stage_behind_first = min(points_score_stage_behind_first),
              victories = sum(victory),
              podiums = sum(podium),
              topfives = sum(topfive),
              toptens = sum(topten)) |>
    ungroup() |>
    group_by(pivot_id,pivot_name) |>
    # 1 = Individual Stage Metric | avg time/score
    # 2 = Individual Stage Position | avg position
    # 3 = Individual Stage Metric from Stage Leader | avg time/score
    # 4 = Individual Stage Metric from Overall Leader | avg time/score
    # 5 = Tallied Individual Stage Metric | avg time/score
    # 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader | avg time/score
    # 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader | avg time/score
    summarise(
      # Stage
      avg_position_stage = mean(stage_position_edit),
      total_stage_time = sum(stage_time),
      # GC Time Stage
      avg_position_gc_time_stage = mean(gc_time_stage_position_edit),
      total_gc_time_stage = sum(gc_time_stage),
      # GC Time
      avg_position_gc = mean(gc_position_edit),
      # GC Time Bonus
      total_gc_time_bonus = sum(gc_time_bonus),
      avg_position_gc_time_bonus = mean(gc_time_bonus_position_edit),
      # kom score
      avg_position_kom_score = mean(kom_score_stage_position),
      total_kom_score = sum(kom_score_stage),
      # points score
      avg_position_points_score = mean(points_score_stage_position),
      total_points_score = sum(points_score_stage),
      # Stage Results aggregations
      victories = sum(victories),
      podiums = sum(podiums),
      topfives = sum(topfives),
      toptens = sum(toptens),
      races_finished = n()) |>
    ungroup() |>
    # create race finished totqls. Exclude riders who didn't complete all races within seleciton
    mutate(total_stage_time = case_when(races_finished != races_selected ~ NA,
                                        .default = total_stage_time)) |>
    mutate(total_stage_time_from_leader = total_stage_time-min(total_stage_time, na.rm = TRUE)) |>
    mutate(total_gc_time_stage = case_when(races_finished != races_selected ~ NA,
                                           .default = total_gc_time_stage)) |>
    mutate(total_gc_time_bonus = case_when(races_finished != races_selected ~ NA,
                                           .default = total_gc_time_bonus)) |>
    mutate(total_kom_score = case_when(races_finished != races_selected ~ NA,
                                           .default = total_kom_score)) |>
    mutate(total_points_score = case_when(races_finished != races_selected ~ NA,
                                           .default = total_points_score)) |>
    mutate(total_gc_time_stage_from_leader = total_gc_time_stage-min(total_gc_time_stage, na.rm = TRUE)) |>
    mutate(total_gc_time_bonus_from_leader = total_gc_time_bonus-min(total_gc_time_bonus, na.rm = TRUE)) |>
    mutate(total_points_score_from_leader = total_points_score-max(total_points_score, na.rm = TRUE)) |>
    mutate(total_kom_score_from_leader = total_kom_score-max(total_kom_score, na.rm = TRUE)) |>
    left_join(results_pivot_races_count, by = "pivot_id")
  
  # looking at metadata for each stage
  results_pivot_sort_stage <- results_pivot_filters |>
    # filter riders who didn't finish the stage
    filter(stage_position_edit < 1000) |>
    # metadata surrounding results for each stage
    group_by(pivot_id,pivot_name,season,first_cycling_race_id,start_date,end_date,stage_number) |>
    summarise(
      # Stage
      stage_position_edit = min(stage_position_edit),
      stage_time = min(stage_time),
      stage_time_behind_first = min(stage_time_behind_first),
      # GC Time Stage
      gc_time_stage_position_edit = min(gc_time_stage_position_edit),
      gc_time_stage = min(gc_time_stage),
      gc_time_stage_behind_first = min(gc_time_stage_behind_first),
      # GC 
      gc_position_edit = min(gc_position_edit),
      gc_time_bonus = min(gc_time_bonus),
      gc_time_bonus_behind_first = min(gc_time_bonus_behind_first),
      # GC Time Bonus
      gc_time_bonus_position_edit = min(gc_time_bonus_position_edit),
      # KOM
      kom_position = min(kom_position),
      kom_score_stage_position = min(kom_score_stage_position),
      kom_score_stage = max(kom_score_stage),
      kom_score_stage_behind_first = min(kom_score_stage_behind_first),
      # Points
      points_position = min(points_position),
      points_score_stage_position = min(points_score_stage_position),
      points_score_stage = max(points_score_stage),
      points_score_stage_behind_first = min(points_score_stage_behind_first),
      
    ) |>
    ungroup() |>
    # join in races_finished_metadata details
    left_join(results_pivot_sort_totals, by = c("pivot_id","pivot_name"))
  
  # working out correct order for stages to make tally counting work
  entered_all_races <- results_pivot_sort_stage |>
    # join in github csv for calendar. Look for end_date and stage_number
    left_join(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number), by = c("season","first_cycling_race_id","stage_number")) |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number,start_date,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    # group by rider/team
    group_by(pivot_id) |>
    arrange(start_date,end_date,stage_number) |>
    # create column for count order of stages
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    group_by(pivot_id) |>
    # see how many stages the rider/team entered
    mutate(stage_number_order_all_races_max = max(stage_number_order)) |>
    ungroup() |>
    # filter table to only look at riders/teams that entered every race within the races selection
    filter(stage_number_order_all_races_max == races_selected) |>
    # unselect unnecessary columns
    select(first_cycling_race_id,stage_number,stage_number_order,stage_number_order_all_races_max) |>
    unique() |>
    # look at only race_id and stage number. Create a column for what the race order is meant to look like.
    group_by(first_cycling_race_id,stage_number) |>
    mutate(stage_number_order_all_races = max(stage_number_order)) |>
    ungroup() |>
    # filter to riders/teams that the order is correct
    filter(stage_number_order == stage_number_order_all_races) |>
    select(-c(stage_number_order_all_races_max,stage_number_order))
  
  # join from stage level metadata
  entered_all_races_tally_workings <- results_pivot_sort_stage |>
    # join in from github calendar csv. Look at stage_number and final date for stage
    left_join(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number), by = c("season","first_cycling_race_id","stage_number")) |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number,start_date,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    # join in dataframe for what it looks like if you entered all races
    left_join(entered_all_races, by = c("first_cycling_race_id","stage_number")) |>
    # group by rider/team and sort in order of races and count the order of the races each entered.
    group_by(pivot_id) |>
    arrange(start_date,end_date,stage_number) |>
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    # only select relevant columns
    select(pivot_id,first_cycling_race_id,stage_number,stage_number_order,stage_number_order_all_races) |>
    # check if stage_number_order for all races matches rider/team level. 
    mutate(stage_number_order_all_races_tally = case_when(stage_number_order == stage_number_order_all_races ~ 1,
                                                          .default = 0)) |>
    group_by(pivot_id) |>
    arrange(pivot_id,stage_number_order_all_races,stage_number_order) |>
    # count how many stages are correct
    mutate(stage_number_order_all_races_tally = cumsum(stage_number_order_all_races_tally)) |>
    # make percentage of races correct until that point
    mutate(stage_number_order_all_races_tally_percent = stage_number_order_all_races_tally/stage_number_order_all_races) |>
    ungroup() |>
    arrange(-stage_number_order_all_races_tally_percent)
  
  # subquery so don't have to build each time
  entered_all_races_tally <- entered_all_races_tally_workings |>
    select(pivot_id,first_cycling_race_id,stage_number,stage_number_order_all_races_tally_percent)
  
  # make tally ordering work how it should
  entered_all_races_tally_sort <- entered_all_races_tally_workings |>
    # filter so stage_order percentage is 100% aligned with race selection order
    filter(stage_number_order_all_races_tally_percent == 1) |>
    # group by rider/team and then create field looking at how long the team was doing all the stages for.
    group_by(pivot_id) |>
    mutate(tally_stage_number_sort = max(stage_number_order_all_races)) |>
    ungroup() |>
    # only bring in rider/team and the output of the stage_number = race selection order max.
    select(pivot_id,tally_stage_number_sort) |>
    unique()
  
  # now additional metadata has been created, make additions to base dataframe
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # look at race selections matching to rider/team race entered
    left_join(entered_all_races_tally, by = c("pivot_id","first_cycling_race_id","stage_number")) |>
    # filter out issues with data source
    filter(stage_time != Inf) |>
    # make varchar replicas of the stage_position_edits I created for sorting purposes
    mutate(stage_position_varchar = case_when(
      stage_position_edit == "1000" ~ "OOT",
      stage_position_edit == "1100" ~ "DNF",
      stage_position_edit == "1200" ~ "DNS",
      stage_position_edit == "1300" ~ "DSQ",
      .default = as.character(stage_position_edit))) |>
    mutate(stage_time_varchar = as.character(stage_time)) |>
    mutate(stage_time_from_leader_varchar = as.character(stage_time_behind_first)) |>
    mutate(gc_time_stage_position_edit = case_when(
      gc_time_stage_position_edit == "1000" ~ "OOT",
      gc_time_stage_position_edit == "1100" ~ "DNF",
      gc_time_stage_position_edit == "1200" ~ "DNS",
      gc_time_stage_position_edit == "1300" ~ "DSQ",
      .default = as.character(gc_time_stage_position_edit))) |>
    mutate(gc_time_bonus_position_edit = case_when(
      gc_time_bonus_position_edit == "1000" ~ "OOT",
      gc_time_bonus_position_edit == "1100" ~ "DNF",
      gc_time_bonus_position_edit == "1200" ~ "DNS",
      gc_time_bonus_position_edit == "1300" ~ "DSQ",
      .default = as.character(gc_time_bonus_position_edit))) |>
    mutate(gc_time_stage_varchar = as.character(gc_time_stage)) |>
    mutate(gc_time_stage_from_leader_varchar = as.character(gc_time_stage_behind_first)) |>
    mutate(gc_time_bonus_varchar = as.character(gc_time_bonus)) |>
    mutate(gc_time_bonus_from_leader_varchar = as.character(gc_time_bonus_behind_first)) |>
    mutate(kom_score_from_leader_varchar = as.character(kom_score_stage_behind_first)) |>
    mutate(kom_position_stage_varchar = as.character(kom_score_stage_position)) |>
    mutate(points_score_from_leader_varchar = as.character(points_score_stage_behind_first)) |>
    mutate(points_position_stage_varchar = as.character(points_score_stage_position)) |>
    mutate(stage_number_int = as.double(stage_number)) |>
    arrange(first_cycling_race_id,pivot_id,stage_number) |>
    # create tally totals for riders/teams. If not aligned with entering all races until that point, put the result as NA.
    group_by(pivot_id,pivot_name) |>
    arrange(start_date,end_date,stage_number) |>
    mutate(tally_total_stage_time = cumsum(stage_time)) |>
    mutate(tally_total_stage_time = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                              .default = tally_total_stage_time)) |>
    mutate(tally_total_gc_time_stage = cumsum(gc_time_stage)) |>
    mutate(tally_total_gc_time_stage = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                 .default = tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_bonus = cumsum(gc_time_bonus)) |>
    mutate(tally_total_gc_time_bonus = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                 .default = tally_total_gc_time_bonus)) |>
    mutate(tally_total_kom_score = cumsum(kom_score_stage)) |>
    mutate(tally_total_kom_score = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                 .default = tally_total_kom_score)) |>
    mutate(tally_total_points_score = cumsum(points_score_stage)) |>
    mutate(tally_total_points_score = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                 .default = tally_total_points_score)) |>
    ungroup() |>
    # create tally totals from leader in each classifcation
    group_by(first_cycling_race_id,stage_number) |>
    mutate(tally_total_stage_time_from_leader = tally_total_stage_time-min(tally_total_stage_time,na.rm = TRUE)) |>
    mutate(tally_total_gc_time_stage_from_leader = tally_total_gc_time_stage-min(tally_total_gc_time_stage,na.rm = TRUE)) |>
    mutate(tally_total_gc_time_bonus_from_leader = max(tally_total_gc_time_bonus,na.rm = TRUE)-tally_total_gc_time_bonus) |>
    mutate(tally_total_kom_score_from_leader = max(tally_total_kom_score,na.rm = TRUE)-tally_total_kom_score) |>
    mutate(tally_total_points_score_from_leader = max(tally_total_points_score,na.rm = TRUE)-tally_total_points_score) |>
    ungroup() |>
    # make varchar replicas of columns just created
    mutate(tally_total_stage_time_varchar = as.character(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_from_leader_varchar = as.character(tally_total_stage_time_from_leader)) |>
    mutate(tally_total_gc_time_stage_varchar = as.character(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_from_leader_varchar = as.character(tally_total_gc_time_stage_from_leader)) |>
    mutate(tally_total_gc_time_bonus_from_leader_varchar = as.character(tally_total_gc_time_bonus_from_leader)) |>
    mutate(tally_total_gc_time_bonus_varchar = as.character(tally_total_gc_time_bonus)) |>
    mutate(gc_time_bonus_varchar = as.character(gc_time_bonus)) |>
    mutate(tally_total_kom_score_from_leader_varchar = as.character(tally_total_kom_score_from_leader)) |>
    mutate(tally_total_kom_score_varchar = as.character(tally_total_kom_score)) |>
    mutate(kom_score_varchar = as.character(kom_score_stage)) |>
    mutate(tally_total_points_score_from_leader_varchar = as.character(tally_total_points_score_from_leader)) |>
    mutate(tally_total_points_score_varchar = as.character(tally_total_points_score)) |>
    mutate(points_score_varchar = as.character(points_score_stage))
    
  
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # left join calendar csv from github for stage_number and end_date
    left_join(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number), by = c("season","first_cycling_race_id","stage_number")) |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,stage_number,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    # create stage_number_order for each rider/team
    group_by(pivot_id) |>
    arrange(start_date,end_date,stage_number) |>
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    select(-end_date)
  
  # create vector value for overall leader looking at stage_time
  overall_leader_stage_tallied_pivot_id <- dplyr::pull(results_pivot_sort_stage |>
                                                         # filter where rider/team had to enter all races
                                                         filter(stage_number_order == races_selected) |>
                                                         # arrange so that if two riders/teams are equal, the order is how I want it to be.
                                                         arrange(tally_total_stage_time,avg_position_stage,-victories,-podiums,-topfives,-toptens,total_gc_time_stage,-total_gc_time_bonus) |>
                                                         # filter so that it only shows rider/team with minimum stage_time
                                                         filter(tally_total_stage_time == min(tally_total_stage_time)) |>
                                                         # select columns within arrange to just check if curious
                                                         select(pivot_id,pivot_name,tally_total_stage_time,avg_position_stage,victories,podiums,topfives,toptens,total_gc_time_stage,total_gc_time_bonus),
                                                       # only bring first result as otherwise equal on time brings in multiple riders/teams.
                                                       pivot_id)[1]
  
  # create dataframe looking at the what the overall leader of tallied stage time did across the metadata
  overall_leader_stage_tallied_time <- results_pivot_sort_stage |>
    # rename columns so it's obvious what it relates to
    select(pivot_id,stage_number_order,
           tally_total_stage_time_overall_leader_time = tally_total_stage_time,
           stage_time_overall_leader_time = stage_time) |>
    # filter so pivot_id = vector of pivot_id leader
    filter(pivot_id == overall_leader_stage_tallied_pivot_id) |>
    # unselect pivot_id as not interested in it.
    select(-c(pivot_id))
  
  # create vector value for overall leader looking at gc_time
  overall_leader_gc_time_stage_tallied_pivot_id <- dplyr::pull(results_pivot_sort_stage |>
                                                                 filter(stage_number_order == races_selected) |>
                                                                 arrange(total_gc_time_stage,avg_position_gc_time_stage,-victories,-podiums,-topfives,-toptens) |>
                                                                 filter(total_gc_time_stage == min(total_gc_time_stage)),pivot_id)[1]
  
  # create vector value for overall leader looking at gc_time_bonus
  overall_leader_gc_time_bonus_tallied_pivot_id <- dplyr::pull(results_pivot_sort_stage |>
                                                                 filter(stage_number_order == races_selected) |>
                                                                 arrange(-tally_total_gc_time_bonus,-victories,-podiums,-topfives,-toptens,avg_position_stage) |>
                                                                 filter(total_gc_time_bonus == max(total_gc_time_bonus)),pivot_id)[1]
  
  # create vector value for overall leader looking at gc_time_bonus
  overall_leader_kom_score_tallied_pivot_id <- dplyr::pull(results_pivot_sort_stage |>
                                                                 filter(stage_number_order == races_selected) |>
                                                                 arrange(-tally_total_kom_score,-victories,-podiums,-topfives,-toptens,avg_position_stage) |>
                                                                 filter(total_kom_score == max(total_kom_score)),pivot_id)[1]
  
  # create vector value for overall leader looking at gc_time_bonus
  overall_leader_points_score_tallied_pivot_id <- dplyr::pull(results_pivot_sort_stage |>
                                                             filter(stage_number_order == races_selected) |>
                                                             arrange(-tally_total_points_score,-victories,-podiums,-topfives,-toptens,avg_position_stage) |>
                                                             filter(total_points_score == max(total_points_score)),pivot_id)[1]
  
  # create dataframe which gives tally total gc_time and individual stage gc_time for overall leader for gc_time
  overall_leader_gc_time_stage_tallied_time <- results_pivot_sort_stage |>
    select(pivot_id,stage_number_order,tally_total_gc_time_stage_time_overall_leader_time = tally_total_gc_time_stage,gc_time_stage_time_overall_leader_time = gc_time_stage) |>
    filter(pivot_id == overall_leader_gc_time_stage_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  # create dataframe which gives tally total gc_time_bonus and individual stage gc_time_bonus for overall leader for gc_time_bonus
  overall_leader_gc_time_bonus_tallied_time <- results_pivot_sort_stage |>
    select(pivot_id,stage_number_order,tally_total_gc_time_bonus_time_overall_leader_time = tally_total_gc_time_bonus,gc_time_bonus_time_overall_leader_time = gc_time_bonus) |>
    filter(pivot_id == overall_leader_gc_time_bonus_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  # create dataframe which gives tally total kom_score and individual stage kom_score for overall leader for kom_score
  overall_leader_kom_score_tallied_score <- results_pivot_sort_stage |>
    select(pivot_id,stage_number_order,tally_total_kom_score_overall_leader_score = tally_total_kom_score,kom_score_overall_leader_score = kom_score_stage) |>
    filter(pivot_id == overall_leader_kom_score_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  # create dataframe which gives tally total kom_score and individual stage points_score for overall leader for points_score
  overall_leader_points_score_tallied_score <- results_pivot_sort_stage |>
    select(pivot_id,stage_number_order,tally_total_points_score_overall_leader_score = tally_total_points_score,points_score_overall_leader_score = points_score_stage) |>
    filter(pivot_id == overall_leader_points_score_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # join in overall_leader for tallied stage time
    left_join(overall_leader_stage_tallied_time, by = c("stage_number_order")) |>
    mutate(tally_total_stage_time_overall_leader_time = as.double(tally_total_stage_time_overall_leader_time)) |>
    # create filed to do time from overall leader when looking at stage_time on individual stage level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(stage_time_from_overall_leader = stage_time-stage_time_overall_leader_time) |>
    mutate(stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                      .default = stage_time_from_overall_leader)) |>
    mutate(stage_time_from_overall_leader_varchar = as.character(stage_time_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at stage_time on overall race selection level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(tally_total_stage_time_overall_leader_time = as.double(tally_total_stage_time_overall_leader_time)) |>
    mutate(tally_total_stage_time = as.double(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_varchar = as.character(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_from_overall_leader = tally_total_stage_time-tally_total_stage_time_overall_leader_time) |>
    mutate(tally_total_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                  .default = tally_total_stage_time_from_overall_leader)) |>
    mutate(tally_total_stage_time_from_overall_leader_varchar = as.character(tally_total_stage_time_from_overall_leader)) |>
    
    #join in overall leader gc time for tallied gc_time time
    left_join(overall_leader_gc_time_stage_tallied_time, by = c("stage_number_order")) |>
    mutate(tally_total_gc_time_stage_time_overall_leader_time = as.double(tally_total_gc_time_stage_time_overall_leader_time)) |>
    # create filed to do time from overall leader when looking at gc_time on individual stage level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(gc_time_stage_time_from_overall_leader = gc_time_stage-gc_time_stage_time_overall_leader_time) |>
    mutate(gc_time_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                              .default = gc_time_stage_time_from_overall_leader)) |>
    mutate(gc_time_stage_time_from_overall_leader_varchar = as.character(gc_time_stage_time_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at gc_time on overall race selection level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(tally_total_gc_time_stage_time_overall_leader_time = as.double(tally_total_gc_time_stage_time_overall_leader_time)) |>
    mutate(tally_total_gc_time_stage = as.double(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_varchar = as.character(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader = tally_total_gc_time_stage-tally_total_gc_time_stage_time_overall_leader_time) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                          .default = tally_total_gc_time_stage_time_from_overall_leader)) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader_varchar = as.character(tally_total_gc_time_stage_time_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at gc_time_bonus on individual stage level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    left_join(overall_leader_gc_time_bonus_tallied_time, by = c("stage_number_order")) |>
    mutate(tally_total_gc_time_bonus_time_overall_leader_time = as.double(tally_total_gc_time_bonus_time_overall_leader_time)) |>
    mutate(gc_time_bonus_time_from_overall_leader = gc_time_bonus_time_overall_leader_time-gc_time_bonus) |>
    mutate(gc_time_bonus_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                              .default = gc_time_bonus_time_from_overall_leader)) |>
    mutate(gc_time_bonus_time_from_overall_leader_varchar = as.character(gc_time_bonus_time_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at gc_time_bonus on overall race selection level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(tally_total_gc_time_bonus_time_overall_leader_time = as.double(tally_total_gc_time_bonus_time_overall_leader_time)) |>
    mutate(tally_total_gc_time_bonus = as.double(tally_total_gc_time_bonus)) |>
    mutate(tally_total_gc_time_bonus_varchar = as.character(tally_total_gc_time_bonus)) |>
    mutate(tally_total_gc_time_bonus_time_from_overall_leader = tally_total_gc_time_bonus_time_overall_leader_time-tally_total_gc_time_bonus) |>
    mutate(tally_total_gc_time_bonus_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                          .default = tally_total_gc_time_bonus_time_from_overall_leader)) |>
    mutate(tally_total_gc_time_bonus_time_from_overall_leader_varchar = as.character(tally_total_gc_time_bonus_time_from_overall_leader)) |>
    
    # create filed to do time from overall leader when looking at gc_time_bonus on individual stage level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    left_join(overall_leader_kom_score_tallied_score, by = c("stage_number_order")) |>
    mutate(tally_total_kom_score_overall_leader_score = as.double(tally_total_kom_score_overall_leader_score)) |>
    mutate(kom_score_from_overall_leader = kom_score_overall_leader_score-kom_score_stage) |>
    mutate(kom_score_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                              .default = kom_score_from_overall_leader)) |>
    mutate(kom_score_from_overall_leader_varchar = as.character(kom_score_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at gc_time_bonus on overall race selection level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(tally_total_kom_score_overall_leader_score = as.double(tally_total_kom_score_overall_leader_score)) |>
    mutate(tally_total_kom_score = as.double(tally_total_kom_score)) |>
    mutate(tally_total_kom_score_varchar = as.character(tally_total_kom_score)) |>
    mutate(tally_total_kom_score_from_overall_leader = tally_total_kom_score_overall_leader_score-tally_total_kom_score) |>
    mutate(tally_total_kom_score_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                          .default = tally_total_kom_score_from_overall_leader)) |>
    mutate(tally_total_kom_score_from_overall_leader_varchar = as.character(tally_total_kom_score_from_overall_leader)) |>
    
    # create filed to do time from overall leader when looking at gc_time_bonus on individual stage level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    left_join(overall_leader_points_score_tallied_score, by = c("stage_number_order")) |>
    mutate(tally_total_points_score_overall_leader_score = as.double(tally_total_points_score_overall_leader_score)) |>
    mutate(points_score_from_overall_leader = points_score_overall_leader_score-points_score_stage) |>
    mutate(points_score_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                        .default = points_score_from_overall_leader)) |>
    mutate(points_score_from_overall_leader_varchar = as.character(points_score_from_overall_leader)) |>
    # create filed to do time from overall leader when looking at gc_time_bonus on overall race selection level.
    # Filter out riders/teams who didn't finish race selection.
    # Make into varchar
    mutate(tally_total_points_score_overall_leader_score = as.double(tally_total_points_score_overall_leader_score)) |>
    mutate(tally_total_points_score = as.double(tally_total_points_score)) |>
    mutate(tally_total_points_score_varchar = as.character(tally_total_points_score)) |>
    mutate(tally_total_points_score_from_overall_leader = tally_total_points_score_overall_leader_score-tally_total_points_score) |>
    mutate(tally_total_points_score_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                    .default = tally_total_points_score_from_overall_leader)) |>
    mutate(tally_total_points_score_from_overall_leader_varchar = as.character(tally_total_points_score_from_overall_leader))
    
  # creating dataframe with metadata from final race to be used for sorting
  final_stage_tally_total <- results_pivot_sort_stage |>
    filter(stage_number_order == races_selected) |>
    select(pivot_id,
           final_stage_total_gc_time_stage_from_overall_leader = tally_total_gc_time_stage_time_from_overall_leader,
           final_stage_total_stage_from_overall_leader = tally_total_stage_time_from_overall_leader,
           final_stage_total_gc_time_bonus_from_overall_leader = tally_total_gc_time_bonus_time_from_overall_leader,
           final_stage_total_kom_score_from_overall_leader = tally_total_kom_score_from_overall_leader,
           final_stage_total_points_score_from_overall_leader = tally_total_points_score_from_overall_leader) |>
    mutate(final_stage_total_gc_time_stage_from_overall_leader_varchar = as.character(final_stage_total_gc_time_stage_from_overall_leader),
           final_stage_total_stage_from_overall_leader_varchar = as.character(final_stage_total_stage_from_overall_leader),
           final_stage_total_gc_time_bonus_from_overall_leader_varchar = as.character(final_stage_total_gc_time_bonus_from_overall_leader),
           final_stage_total_kom_score_from_overall_leader_varchar = as.character(final_stage_total_kom_score_from_overall_leader),
           final_stage_total_points_score_from_overall_leader_varchar = as.character(final_stage_total_points_score_from_overall_leader)
    )
  
  # joining in final race metadata
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    left_join(final_stage_tally_total, by = "pivot_id") |>
    left_join(entered_all_races_tally_sort, by = "pivot_id") |>
    # ensuring that sorting works properly for riders/teams who didn't finish all races
    mutate(tally_stage_number_sort = case_when(is.na(tally_stage_number_sort) == TRUE ~ 0,
                                               .default = tally_stage_number_sort))
  
  # putting final table together for pivot table
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # creating field that is dynamic to metric selected as part of the function
    mutate(value_from = case_when(
      # 1 = Individual Stage Metric
      # 2 = Individual Stage Position
      # 3 = Individual Stage Metric from Stage Leader
      # 4 = Individual Stage Metric from Overall Leader
      # 5 = Tallied Individual Stage Metric
      # 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader
      # 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader
      # 8 = Individual Stage Metric from GC Overall Leader
      # 9 = Tallied Individial Stage Metric from GC Overall Tallied Stage Leader
      value_from_function == "S1" ~ stage_time_varchar,
      value_from_function == "S2" ~ stage_position_varchar,
      value_from_function == "S3" ~ stage_time_from_leader_varchar,
      value_from_function == "S4" ~ stage_time_from_overall_leader_varchar,
      value_from_function == "S5" ~ tally_total_stage_time_varchar,
      value_from_function == "S6" ~ tally_total_stage_time_from_leader_varchar,
      value_from_function == "S7" ~ tally_total_stage_time_from_overall_leader_varchar,
      value_from_function == "GC1" ~ gc_time_stage_varchar,
      value_from_function == "GC2" ~ gc_time_stage_position_edit,
      value_from_function == "GC3" ~ gc_time_stage_from_leader_varchar,
      value_from_function == "GC4" ~ gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "GC5" ~ tally_total_gc_time_stage_varchar,
      value_from_function == "GC6" ~ tally_total_gc_time_stage_from_leader_varchar,
      value_from_function == "GC7" ~ tally_total_gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "GC8" ~ gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "GC9" ~ tally_total_gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "B1" ~ gc_time_bonus_varchar,
      value_from_function == "B2" ~ gc_time_bonus_position_edit,
      value_from_function == "B3" ~ gc_time_bonus_from_leader_varchar,
      value_from_function == "B4" ~ gc_time_bonus_time_from_overall_leader_varchar,
      value_from_function == "B5" ~ tally_total_gc_time_bonus_varchar,
      value_from_function == "B6" ~ tally_total_gc_time_bonus_from_leader_varchar,
      value_from_function == "B7" ~ tally_total_gc_time_bonus_time_from_overall_leader_varchar,
      value_from_function == "KOM1" ~ kom_score_varchar,
      value_from_function == "KOM2" ~ kom_position_stage_varchar,
      value_from_function == "KOM3" ~ kom_score_from_leader_varchar,
      value_from_function == "KOM4" ~ kom_score_from_overall_leader_varchar,
      value_from_function == "KOM5" ~ tally_total_kom_score_varchar,
      value_from_function == "KOM6" ~ tally_total_kom_score_from_leader_varchar,
      value_from_function == "KOM7" ~ tally_total_kom_score_from_overall_leader_varchar,
      value_from_function == "P1" ~ points_score_varchar,
      value_from_function == "P2" ~ points_position_stage_varchar,
      value_from_function == "P3" ~ points_score_from_leader_varchar,
      value_from_function == "P4" ~ points_score_from_overall_leader_varchar,
      value_from_function == "P5" ~ tally_total_points_score_varchar,
      value_from_function == "P6" ~ tally_total_points_score_from_leader_varchar,
      value_from_function == "P7" ~ tally_total_points_score_from_overall_leader_varchar,
      
      .default = stage_position_varchar)) |>
    # creating field for sorting data using the right field depending on what was selected as part of the function
    mutate(value_from_metric = case_when(
      # Aggregated Metrics
      value_from_function == "S1" ~ total_stage_time,
      value_from_function == "S2" ~ avg_position_stage,
      value_from_function == "S3" ~ total_stage_time_from_leader,
      value_from_function == "S4" ~ final_stage_total_stage_from_overall_leader,
      value_from_function == "S5" ~ total_stage_time,
      value_from_function == "S6" ~ total_stage_time_from_leader,
      value_from_function == "S7" ~ total_stage_time,
      value_from_function == "GC1" ~ total_gc_time_stage,
      value_from_function == "GC2" ~ avg_position_gc_time_stage,
      value_from_function == "GC3" ~ total_gc_time_stage_from_leader,
      value_from_function == "GC4" ~ final_stage_total_gc_time_stage_from_overall_leader,
      value_from_function == "GC5" ~ total_gc_time_stage,
      value_from_function == "GC6" ~ total_gc_time_stage_from_leader,
      value_from_function == "GC7" ~ total_gc_time_stage,
      value_from_function == "GC8" ~ final_stage_total_gc_time_stage_from_overall_leader,
      value_from_function == "GC9" ~ final_stage_total_gc_time_stage_from_overall_leader,
      value_from_function == "B1" ~ total_gc_time_bonus*-1,
      value_from_function == "B2" ~ avg_position_gc_time_bonus,
      value_from_function == "B3" ~ total_gc_time_bonus_from_leader*-1,
      value_from_function == "B4" ~ final_stage_total_gc_time_bonus_from_overall_leader,
      value_from_function == "B5" ~ total_gc_time_bonus*-1,
      value_from_function == "B6" ~ total_gc_time_bonus_from_leader*-1,
      value_from_function == "B7" ~ total_gc_time_bonus*-1,
      value_from_function == "KOM1" ~ total_kom_score*-1,
      value_from_function == "KOM2" ~ avg_position_kom_score,
      value_from_function == "KOM3" ~ total_kom_score_from_leader*-1,
      value_from_function == "KOM4" ~ final_stage_total_kom_score_from_overall_leader,
      value_from_function == "KOM5" ~ total_kom_score*-1,
      value_from_function == "KOM6" ~ total_kom_score_from_leader*-1,
      value_from_function == "KOM7" ~ total_kom_score*-1,
      value_from_function == "P1" ~ total_points_score*-1,
      value_from_function == "P2" ~ avg_position_points_score,
      value_from_function == "P3" ~ total_points_score_from_leader*-1,
      value_from_function == "P4" ~ final_stage_total_points_score_from_overall_leader,
      value_from_function == "P5" ~ total_points_score*-1,
      value_from_function == "P6" ~ total_points_score_from_leader*-1,
      value_from_function == "P7" ~ total_points_score*-1,
      .default = avg_position_stage
    )) |>
    # joining in calendar function to put stage profile category into pivot table field names
    left_join(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv'), by = c("season","first_cycling_race_id","stage_number","start_date")) |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv'), by = c("season","first_cycling_race_id","stage_number","start_date")) |>
    # place holder incase I want to look at multiple seasons of certain races
    # concat race_name, stage number and stage profile together.
    #mutate(names_from = paste0(season, " | ",race_name," | ",stage_number," | ",stage_profile)) |>
    mutate(names_from = paste0(race_name," | ",stage_number," | ",stage_profile)) |>
    # ensure that the data is ordered on a start_date and stage number basis so the table is in date order.
    mutate(stg_number = as.double(stage_number)) |>
    arrange(start_date,stg_number) |>
    
    # avg_position and classification_metric should be dynamic to classification selected
    mutate(classification_avg_position = case_when(str_detect(value_from_function,'S') ~ avg_position_stage,
                                                   str_detect(value_from_function,'GC') ~ avg_position_gc_time_stage,
                                                   str_detect(value_from_function,'B') ~ avg_position_gc_time_bonus,
                                                   str_detect(value_from_function,'KOM') ~ avg_position_kom_score,
                                                   str_detect(value_from_function,'P') ~ avg_position_points_score,
                                                   #str_detect(value_from_function,'Y') ~ "Youth",
                                                   .default = avg_position_stage)
    ) |>
    mutate(classification_total_score = case_when(str_detect(value_from_function,'S') ~ total_stage_time,
                                                   str_detect(value_from_function,'GC') ~ total_gc_time_stage,
                                                   str_detect(value_from_function,'B') ~ total_gc_time_bonus,
                                                   str_detect(value_from_function,'KOM') ~ total_kom_score,
                                                   str_detect(value_from_function,'P') ~ total_points_score,
                                                   #str_detect(value_from_function,'Y') ~ "Youth",
                                                   .default = total_gc_time_stage)
    )
    
    # stages gaining KOM points
    
  points_scoring_stages_count_df <- results_pivot_sort_stage |>
    mutate(points_scoring_stages_count = case_when(
      str_detect(value_from_function,'B') & gc_time_bonus_varchar > 0 ~ 1,
      str_detect(value_from_function,'KOM') & kom_score_varchar > 0 ~ 1,
      str_detect(value_from_function,'P') & points_score_varchar > 0 ~ 1,
      .default = 0
    )) |>
    group_by(pivot_id) |>
    summarise(points_scoring_stages_count = sum(points_scoring_stages_count))
    
    results_pivot_sort_stage <- results_pivot_sort_stage |>
    left_join(points_scoring_stages_count_df, by = "pivot_id") |>
    # deselect any columns that were built to form the table output
    select(-c(stage_time_varchar,stage_time_from_leader_varchar,stage_time,
              stage_time_behind_first
              #,gc_time_stage_from_overall_leader_stage_time
              #,gc_time_stage_overall_leader_stage_time
              ,first_cycling_race_id,season,stage_profile,stage_number,race_name,
              start_date,stg_number,
              race_nationality,gender,category,uci_race_classification,stage_race_boolean,
              end_date,
              race_tags,
              route,distance,
              stage_number
              ,tally_total_stage_time,tally_total_stage_time_from_leader
              ,gc_time_stage,
              gc_time_stage_varchar,gc_time_stage_from_leader_varchar,stage_number_int,tally_total_gc_time_stage,tally_total_gc_time_stage_from_leader
              ,total_stage_time,total_stage_time_from_leader,gc_time_stage_behind_first,
              total_gc_time_stage_from_leader,
              stage_position_edit,gc_time_stage_position_edit,gc_position_edit,avg_position_gc_time_stage,
              stage_position_varchar
              ,tally_total_stage_time_overall_leader_time,stage_time_overall_leader_time
              ,stage_time_from_overall_leader,stage_time_from_overall_leader_varchar,
              stage_number_order,
              tally_total_stage_time_varchar,tally_total_stage_time_from_leader_varchar
              ,tally_total_stage_time_from_overall_leader_varchar,tally_total_stage_time_from_overall_leader
              ,tally_total_gc_time_stage_time_overall_leader_time,gc_time_stage_time_overall_leader_time
              ,tally_total_gc_time_stage_time_from_overall_leader,tally_total_gc_time_stage_time_from_overall_leader_varchar
              ,gc_time_stage_time_from_overall_leader,tally_total_gc_time_stage_varchar,
              gc_time_stage_time_from_overall_leader_varchar
              ,final_stage_total_gc_time_stage_from_overall_leader
              ,gc_time_bonus,gc_time_bonus_varchar
              ,final_stage_total_gc_time_stage_from_overall_leader_varchar
              ,final_stage_total_stage_from_overall_leader,final_stage_total_stage_from_overall_leader_varchar
              ,stage_number_order_all_races_tally_percent
              ,tally_total_gc_time_bonus,tally_total_gc_time_bonus_varchar
              ,gc_time_bonus_position_edit,avg_position_gc_time_bonus,gc_time_bonus_behind_first
              ,total_gc_time_bonus_from_leader,gc_time_bonus_from_leader_varchar,
              tally_total_gc_time_bonus_time_overall_leader_time,gc_time_bonus_time_overall_leader_time,
              gc_time_bonus_time_from_overall_leader,gc_time_bonus_time_from_overall_leader_varchar,
              tally_total_gc_time_bonus_time_from_overall_leader,tally_total_gc_time_bonus_time_from_overall_leader_varchar,
              final_stage_total_gc_time_bonus_from_overall_leader,final_stage_total_gc_time_bonus_from_overall_leader_varchar
              ,tally_total_gc_time_bonus_from_leader,tally_total_gc_time_stage_from_leader_varchar,tally_total_gc_time_bonus_from_leader,
              tally_total_gc_time_bonus_from_leader_varchar
              ,X
              ,paralympics_race_id,
              kom_position,kom_score_stage,
              points_position,avg_position_kom_score,
              total_kom_score,avg_position_points_score,
              total_points_score,
              total_points_score_from_leader,points_score_stage_position,points_score_stage,avg_position_kom_score,
              total_kom_score_from_leader,kom_score_from_leader_varchar,tally_total_kom_score,
              tally_total_points_score,tally_total_kom_score_from_leader,tally_total_points_score_from_leader,
              tally_total_kom_score_from_leader_varchar,tally_total_kom_score_varchar,kom_score_varchar,
              tally_total_points_score_from_leader_varchar,tally_total_points_score_varchar,
              tally_total_kom_score_overall_leader_score,kom_score_overall_leader_score,
              kom_score_from_overall_leader,kom_score_from_overall_leader_varchar,tally_total_kom_score_from_overall_leader,
              tally_total_kom_score_from_overall_leader_varchar,final_stage_total_kom_score_from_overall_leader,
              final_stage_total_kom_score_from_overall_leader_varchar,kom_score_stage_behind_first,points_score_stage_behind_first,
              points_score_from_leader_varchar,points_score_varchar,tally_total_points_score_overall_leader_score,
              points_score_overall_leader_score,points_score_from_overall_leader,points_score_from_overall_leader_varchar,
              tally_total_points_score_from_overall_leader,tally_total_points_score_from_overall_leader_varchar,
              final_stage_total_points_score_from_overall_leader,
              final_stage_total_points_score_from_overall_leader_varchar,
              avg_position_stage,total_gc_time_stage,
              kom_score_stage_position,kom_position_stage_varchar,points_position_stage_varchar
    )) |>
      
      # additional metadata, bonus seconds or days scoring
      mutate(pivot_metadata = case_when(str_detect(value_from_function,'S') ~ total_gc_time_bonus,
                                        str_detect(value_from_function,'GC') ~ total_gc_time_bonus,
                                        str_detect(value_from_function,'B') ~ points_scoring_stages_count,
                                        str_detect(value_from_function,'KOM') ~ points_scoring_stages_count,
                                        str_detect(value_from_function,'P') ~ points_scoring_stages_count,
                                        #str_detect(value_from_function,'Y') ~ total_gc_time_bonus,
                                        .default = total_gc_time_bonus)
      )
  
  # make the table into a pivot table
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    pivot_wider(
      names_from = names_from,
      values_from = value_from
    )
  
  
  
  # sorting table into correct order depending on function selection
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # table sort 1 looks into if tallied (races until tally breaks) or not (races_finished)
    mutate(table_sort1 = case_when(str_detect(value_from_function,'5') == TRUE ~ tally_stage_number_sort*-1,
                                   str_detect(value_from_function,'6') == TRUE ~ tally_stage_number_sort*-1,
                                   str_detect(value_from_function,'7') == TRUE ~ tally_stage_number_sort*-1,
                                   .default = as.double(0)*-1)) |>
    # table sort 2 looks at races_finished descending
    mutate(table_sort2 = as.double(races_finished)*-1) |>
    # table sort 3 looks at races entered descending
    mutate(table_sort3 = as.double(races_count)*-1) |>
    # table sort 4 looks at metric
    # 1 = Individual Stage Metric | avg time/score
    # 2 = Individual Stage Position | avg position
    # 3 = Individual Stage Metric from Stage Leader | avg time/score
    # 4 = Individual Stage Metric from Overall Leader | avg time/score
    # 5 = Tallied Individual Stage Metric | avg time/score
    # 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader | avg time/score
    # 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader | avg time/score
    
    mutate(table_sort4 = value_from_metric) |>
    # table sort 5 looks at average stage position for the classification selected
    mutate(table_sort5 = classification_avg_position) |>
    mutate(table_sort5b = pivot_metadata*-1) |>
    # Victories, Podiums, top5s, top10s descending
    mutate(table_sort6 = as.double(victories)*-1,
           table_sort7 = as.double(podiums)*-1,
           table_sort8 = as.double(topfives)*-1,
           table_sort9 = as.double(toptens)*-1) |>
    # arrange data based on table sorts
    arrange(
      table_sort1,
      table_sort2,table_sort3
      ,table_sort4
      ,table_sort5,
      table_sort5b,
      table_sort6,table_sort7,table_sort8,table_sort9
    ) |>
    # filters
    #filter(races_count == 1) |>
    #filter(total_gc_time_stage == 32039) |>
    # create ranking column
    mutate(rank = row_number()) |>
    # deselect all columns that shouldn't be shown in table output
    select(-c(
      table_sort1,
      table_sort2
      ,table_sort3
      ,table_sort4
      ,table_sort5,
      table_sort5b,table_sort6,table_sort7,table_sort8,table_sort9
      ,victories,podiums,topfives,toptens,avg_position_gc
      ,tally_stage_number_sort
      ,pivot_id
    ))
  
  # only show number of rows given by user
  head_count <- head_count_function
  
  # dynamic table header, focusing on gender.
  gt_title_gender <- case_when(gender_function == "men" ~ "Men's",
                               gender_function == "women" ~ "Women's",
                               .default = "")
  
  # dynamic table header, focusing on race selected. Needs to be adaptable to different methods of selecting races.
  gt_title_race_filter <- case_when(!str_detect(race_filter_function,'Stages') ~ dplyr::pull(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> filter(first_cycling_race_id == str_split_i(race_filter_function," - ",-1), season == season_function) |> select(race_name) |> unique(),race_name),
                                    .default = race_filter_function)
  #gt_title_race_filter <- case_when(str_detect(race_filter_function,'Stages') ~ dplyr::pull(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> filter(first_cycling_race_id == str_split_i(race_filter_function," - ",-1), season == season_function) |> select(race_name) |> unique(),race_name),
  #                                  .default = race_filter_function)
  
  # Base metric. Current options are Stage Time, GC Time and GC Bonus Time.
  gt_title_value_from_metric <- case_when(str_detect(value_from_function,'S') ~ "Stage Time",
                                          str_detect(value_from_function,'GC') ~ "GC Time",
                                          str_detect(value_from_function,'B') ~ "GC Bonus Time",
                                          str_detect(value_from_function,'KOM') ~ "KOM",
                                          str_detect(value_from_function,'P') ~ "Points",
                                          str_detect(value_from_function,'Y') ~ "Youth",
                                          .default = '')
  
  # Metadata for base metric. Currently got 7 options, but will expand in the future.
  gt_title_value_from_metric2 <- case_when(str_detect(value_from_function,'1') ~ "on each stage",
                                           str_detect(value_from_function,'2') ~ "Position on each stage",
                                           str_detect(value_from_function,'3') ~ "on each stage from Stage Leader",
                                           str_detect(value_from_function,'4') ~ "on each stage from Overall Leader",
                                           str_detect(value_from_function,'5') ~ "Tallied",
                                           str_detect(value_from_function,'6') ~ "Tailled from Stage Leader",
                                           str_detect(value_from_function,'7') ~ "Tallied from Overall Leader",
                                           .default = '')
  
  # merge all the different sections of title into one vector.
  gt_title <- paste0('**',gt_title_gender,' ',gt_title_race_filter, ' | ',gt_title_value_from_metric,' ',gt_title_value_from_metric2,'**')
  
  # create single vector showing all races within table and who did the analysis.
  # Need to turn this into a single vector with ' | ' between them.
  gt_subtitle_race_names <- case_when(str_detect(race_filter_function,'Stages') ~ '',
                                      !(str_detect(race_filter_function,'Stages')) ~ dplyr::pull(read.csv('/Users/zacrogers/Documents/cycling_chaos/python_code/frontend_csv/calendar.csv') |> filter(str_detect(race_tags,race_filter_function), gender == gender_function, season == season_function) |> select(race_name) |> unique(),race_name),
                                      .default = "")
  #gt_subtitle_race_names <- case_when(str_detect(race_filter_function,'Stages') ~ '',
  #                                    !(str_detect(race_filter_function,'Stages')) ~ dplyr::pull(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> filter(str_detect(race_tags,race_filter_function), gender == gender_function, season == season_function) |> select(race_name) |> unique(),race_name),
  #                                    .default = "")
  
  gt_subtitle_race_names <- paste(gt_subtitle_race_names,collapse = " | ")
  
  gt_subtitle_work_by <- paste0('Analytics by ',template_user_function)
  
  gt_subtitle <- paste0(gt_subtitle_race_names,' ',gt_subtitle_work_by)
  
  # making vector for metadata label. Options are bonus seconds (when using GC related metrics and classification stage cobnt for non-GC)
  pivot_metadata_table_label <- case_when(str_detect(value_from_function,'S') ~ "Bonus Seconds*",
                                          str_detect(value_from_function,'GC') ~ "Bonus Seconds*",
                                          str_detect(value_from_function,'B') ~ "Days Scoring",
                                          str_detect(value_from_function,'KOM') ~ "Days Scoring",
                                          str_detect(value_from_function,'P') ~ "Days Scoring",
                                          str_detect(value_from_function,'Y') ~ "Bonus Seconds*",
                                          .default = '')
  
  # making pivot table into a gt()
  results_pivot_sort_stage <- results_pivot_sort_stage |>
    # filter to show the top [x] riders/teams. [x] is a function selection by the user
    head(head_count) |>
    
    # make classification_avg_position readable to humans
    mutate(classification_avg_position = round(classification_avg_position,1)) |>
    gt() |>
    # format table to look nice
    cols_align(align = c("center")) |>
    # move columns around so they are aligned where it makes sense
    cols_move_to_start(rank) |>
    cols_move(classification_avg_position,pivot_name) |>
    cols_move(classification_total_score,classification_avg_position) |>
    cols_move(total_gc_time_bonus,classification_total_score) |>
    cols_move(pivot_metadata,classification_total_score) |>
    # change field names so it is more readable
    cols_label(
      pivot_name = "Name",
      rank = "Rank",
      classification_avg_position = "Avg Position",
      classification_total_score = gt_title_value_from_metric,
      races_finished = "Races Finished",
      races_count = "Race Startlist",
      total_gc_time_bonus = "Bonus Seconds*",
      pivot_metadata = pivot_metadata_table_label,
      value_from_metric = "Metric"
    ) |>
    # hide field that is used for sorting
    cols_hide(value_from_metric) |>
    cols_hide(c(total_gc_time_bonus,points_scoring_stages_count)) |>
    # testing area for additional metadata within table
    #gt_badge(palette = c("1" = "gold","2" = "#A7A7AD", "3" = "#A77044")) |>
    # table header should be dynamic to function selection.
    tab_header(title = md(gt_title),
               subtitle = md(gt_subtitle)) |>
    #tab_header(title = md("**Aussie Men's WT Race Block | GC Time from Best Rider on each Stage**"),
    #tab_header(title = md("**Aussie Men's WT Race Block | Most Consistent Stage Finisher**"),
    #subtitle = md("Tour Down Under & Cadel Evans Road Race | CyclingChaos.co.uk")) |>
    # adding some lines to split out rank and metadata from stage level data
    tab_style(
      style = list(
        cell_borders(
          sides = "right",
          color = "black",
          weight = px(3)
        )
      ),
      locations = list(
        cells_body(
          columns = c(rank,races_count))))|>
    tab_footnote(
      footnote = "Template by CyclingChaos.co.uk | Data from FirstCycling.com | Bonus Seconds* are GC Time minus total Stage Time & Added Bonus Seconds to One Day Races"
    )
  
}

# reminder of what each of the functions mean

# 1 = Individual Stage Metric | avg time/score
# 2 = Individual Stage Position | avg position
# 3 = Individual Stage Metric from Stage Leader | avg time/score
# 4 = Individual Stage Metric from Overall Leader | avg time/score
# 5 = Tallied Individual Stage Metric | avg time/score
# 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader | avg time/score
# 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader | avg time/score
print(results_pivot(2024,"men","team","gc7","SB-MSR","","","",1,200,"CyclingChaos.co.uk"))

