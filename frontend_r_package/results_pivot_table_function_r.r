library(tidyverse)

results_pivot <- function(season_function,gender_function,detail_slicer_function,value_from_function,race_filter_function,uci_race_classification_function,
                          race_location_function,stage_race_function) {
  results_pivot_filters <- results_function() |>
    filter(season == season_function, gender == gender_function) |>
    left_join(calendar_function() |> select(season,first_cycling_race_id,race_nationality,race_tags) |> unique(), by = c("season","first_cycling_race_id")) |>
    # uci_race_classification filter
    mutate(uci_race_classification_filter = case_when(str_detect(uci_race_classification,'UWT') & uci_race_classification_function == 'World Tour' ~ 1,
                                                      str_detect(uci_race_classification,'WWT') & uci_race_classification_function == 'World Tour' ~ 1,
                                                      uci_race_classification_function == "" ~ 1,
                                                      .default = 0)) |>
    filter(uci_race_classification_filter == 1) |>
    mutate(race_location_filter = case_when(race_location_function == race_nationality ~ 1,
                                            #race_location_function == race_location_id ~ 1,
                                            #race_location_function == race_location_name ~ 1,
                                            race_location_function == "" ~ 1,
                                            .default = 0)) |>
    filter(race_location_filter == 1) |>
    mutate(stage_race_filter = case_when(stage_race_function == "Stage Race" ~ 1,
                                         stage_race_function == "One Day" ~ 1,
                                         stage_race_function == "" ~ 1,
                                         .default = 0)) |>
    filter(stage_race_filter == 1) |>
    ### Making Position data numeric
    # Need to do gc_time_position
    # Need to do gc_position
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
    mutate(gc_position_edit = case_when(gc_position == "OOT" ~ 1000,
                                        gc_position == "DNF" ~ 1100,
                                        gc_position == "DNS" ~ 1200,
                                        gc_position == "DSQ" ~ 1300,
                                        .default = as.double(gc_position)))
  
  results_pivot_filters_rider_calendar <- dplyr::pull(results_pivot_filters |> 
                                                        mutate(race_filter_rider = case_when(str_detect(race_filter_function,"Rider")
                                                                                             & first_cycling_rider_id == str_split_i(race_filter_function," - ",-1) ~ 1,
                                                                                             .default = 0)) |>
                                                        filter(race_filter_rider == 1),first_cycling_race_id) |> unique()
  
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
  
  races_selected <- sum(dplyr::pull(results_pivot_filters |>
                                      select(first_cycling_race_id,stage_number) |>
                                      unique() |>
                                      summarise(count = n()),count))
  
  results_pivot_races_count <- results_pivot_filters |>
    group_by(pivot_id) |>
    summarise(races_count = n_distinct(paste0(first_cycling_race_id,"_",stage_number)))
  
  results_pivot_sort <- results_pivot_filters |>
    filter(stage_position_edit < 1000) |>
    mutate(victory = case_when(stage_position_edit == 1 ~ 1,
                               .default = 0),
           podium = case_when(stage_position_edit < 4 ~ 1,
                              .default = 0),
           topfive = case_when(stage_position_edit < 6 ~ 1,
                               .default = 0),
           topten = case_when(stage_position_edit < 11 ~ 1,
                              .default = 0)) |>
    group_by(pivot_id,pivot_name,season,first_cycling_race_id,stage_number,stage_number_order) |>
    # Need to calculate best stage position, stage_time, stage_time_from_leader
    # gc_stage_time position, gc_stage_time, gc_stage_time_from_leader
    # gc_position, gc_time, gc_time_from_leader
    summarise(stage_position_edit = min(stage_position_edit),
              stage_time = min(stage_time),
              stage_time_behind_first = min(stage_time_behind_first),
              gc_time_stage_position_edit = min(gc_time_stage_position_edit),
              gc_time_stage = min(gc_time_stage),
              gc_time_stage_behind_first = min(gc_time_stage_behind_first),
              gc_position_edit = min(gc_position_edit),
              gc_time = min(gc_time),
              gc_time_from_leader = min(gc_time_behind_first),
              gc_time_bonus = min(gc_time_bonus),
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
      total_bonus_seconds = sum(gc_time_bonus),
      #total_gc_time = sum(gc_time),
      # Stage Results aggregations
      victories = sum(victories),
      podiums = sum(podiums),
      topfives = sum(topfives),
      toptens = sum(toptens),
      races_finished = n()) |>
    ungroup() |>
    mutate(total_stage_time = case_when(races_finished != races_selected ~ NA,
                                        .default = total_stage_time)) |>
    mutate(total_stage_time_from_leader = total_stage_time-min(total_stage_time, na.rm = TRUE)) |>
    mutate(total_gc_time_stage = case_when(races_finished != races_selected ~ NA,
                                           .default = total_gc_time_stage)) |>
    mutate(total_gc_time_stage_from_leader = total_gc_time_stage-min(total_gc_time_stage, na.rm = TRUE)) |>
    left_join(results_pivot_races_count, by = "pivot_id")
  
  results_pivot_sort2 <- results_pivot_filters |>
    filter(stage_position_edit < 1000) |>
    group_by(pivot_id,pivot_name,season,first_cycling_race_id,stage_number) |>
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
      gc_time_bonus = min(gc_time_bonus)
      
    ) |>
    ungroup() |>
    left_join(results_pivot_sort, by = c("pivot_id","pivot_name"))
  
  entered_all_races <- results_pivot_sort2 |>
    left_join(calendar_function() |> select(season,first_cycling_race_id,stage_number,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    group_by(pivot_id) |>
    arrange(end_date,stage_number) |>
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    group_by(pivot_id) |>
    mutate(stage_number_order_all_races_max = max(stage_number_order)) |>
    ungroup() |>
    filter(stage_number_order_all_races_max == races_selected) |>
    select(first_cycling_race_id,stage_number,stage_number_order,stage_number_order_all_races_max) |>
    unique() |>
    group_by(first_cycling_race_id,stage_number) |>
    mutate(stage_number_order_all_races = max(stage_number_order)) |>
    ungroup() |>
    filter(stage_number_order == stage_number_order_all_races) |>
    select(-c(stage_number_order_all_races_max,stage_number_order))
  
  ### In process of building tally stage_number_order so tally totals don't show NAs for riders who did the first 2 races but didn't do 3 etc.
  # Like Pog in Ardennes week. Should show tally from leader as him for first 2 races.
  # Also tally sort works so that it orders riders in order of who did the most stages in stage_number_order before rest of filter
  # probably need to move this up before a load of the sorts.
  
  entered_all_races_tally_workings <- results_pivot_sort2 |>
    left_join(calendar_function() |> select(season,first_cycling_race_id,stage_number,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    left_join(entered_all_races, by = c("first_cycling_race_id","stage_number")) |>
    group_by(pivot_id) |>
    arrange(end_date,stage_number) |>
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    select(pivot_id,first_cycling_race_id,stage_number,stage_number_order,stage_number_order_all_races) |>
    mutate(stage_number_order_all_races_tally = case_when(stage_number_order == stage_number_order_all_races ~ 1,
                                                          .default = 0)) |>
    group_by(pivot_id) |>
    arrange(pivot_id,stage_number_order_all_races,stage_number_order) |>
    mutate(stage_number_order_all_races_tally = cumsum(stage_number_order_all_races_tally)) |>
    mutate(stage_number_order_all_races_tally_percent = stage_number_order_all_races_tally/stage_number_order_all_races) |>
    ungroup() |>
    arrange(-stage_number_order_all_races_tally_percent)
  
  entered_all_races_tally <- entered_all_races_tally_workings |>
    select(pivot_id,first_cycling_race_id,stage_number,stage_number_order_all_races_tally_percent)
  
  entered_all_races_tally_sort <- entered_all_races_tally_workings |>
    filter(stage_number_order_all_races_tally_percent == 1) |>
    group_by(pivot_id) |>
    mutate(tally_stage_number_sort = max(stage_number_order_all_races)) |>
    ungroup() |>
    select(pivot_id,tally_stage_number_sort) |>
    unique()
  
  
  results_pivot_sort3a <- results_pivot_sort2 |>
    left_join(entered_all_races_tally, by = c("pivot_id","first_cycling_race_id","stage_number")) |>
    filter(stage_time != Inf) |>
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
    mutate(gc_time_stage_varchar = as.character(gc_time_stage)) |>
    mutate(gc_time_stage_from_leader_varchar = as.character(gc_time_stage_behind_first)) |>
    mutate(stage_number_int = as.double(stage_number)) |>
    arrange(first_cycling_race_id,pivot_id,stage_number) |>
    group_by(pivot_id,pivot_name) |>
    mutate(tally_total_stage_time = cumsum(stage_time)) |>
    mutate(tally_total_stage_time = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                              .default = tally_total_stage_time)) |>
    mutate(tally_total_gc_time_stage = cumsum(gc_time_stage)) |>
    mutate(tally_total_gc_time_stage = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                 .default = tally_total_gc_time_stage)) |>
    ungroup() |>
    group_by(first_cycling_race_id,stage_number) |>
    mutate(tally_total_stage_time_from_leader = tally_total_stage_time-min(tally_total_stage_time,na.rm = TRUE)) |>
    mutate(tally_total_gc_time_stage_from_leader = tally_total_gc_time_stage-min(tally_total_gc_time_stage,na.rm = TRUE)) |>
    ungroup() |>
    mutate(tally_total_stage_time = as.character(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_from_leader_varchar = as.character(tally_total_stage_time_from_leader)) |>
    mutate(tally_total_gc_time_stage = as.character(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_from_leader = as.character(tally_total_gc_time_stage_from_leader)) |>
    mutate(gc_time_bonus_varchar = as.character(gc_time_bonus))
  
  #?cumsum()
  
  results_pivot_sort3b <- results_pivot_sort3a |>
    left_join(calendar_function() |> select(season,first_cycling_race_id,stage_number,end_date), by = c("season","first_cycling_race_id","stage_number")) |>
    group_by(pivot_id) |>
    arrange(end_date,stage_number) |>
    mutate(stage_number_order = row_number()) |>
    ungroup() |>
    select(-end_date)
  
  overall_leader_stage_tallied_pivot_id <- dplyr::pull(results_pivot_sort3b |>
                                                         filter(stage_number_order == races_selected) |>
                                                         filter(tally_total_stage_time == min(tally_total_stage_time)),pivot_id)
  
  overall_leader_stage_tallied_time <- results_pivot_sort3b |>
    select(pivot_id,stage_number_order,tally_total_stage_time_overall_leader_time = tally_total_stage_time,stage_time_overall_leader_time = stage_time) |>
    filter(pivot_id == overall_leader_stage_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  overall_leader_gc_time_stage_tallied_pivot_id <- dplyr::pull(results_pivot_sort3b |>
                                                                 filter(stage_number_order == races_selected) |>
                                                                 filter(total_gc_time_stage == min(total_gc_time_stage)),pivot_id)
  
  overall_leader_gc_time_stage_tallied_time <- results_pivot_sort3b |>
    select(pivot_id,stage_number_order,tally_total_gc_time_stage_time_overall_leader_time = tally_total_gc_time_stage,gc_time_stage_time_overall_leader_time = gc_time_stage) |>
    filter(pivot_id == overall_leader_gc_time_stage_tallied_pivot_id) |>
    select(-c(pivot_id))
  
  
  results_pivot_sort3c <- results_pivot_sort3b |>
    # need to create a boolean for who finished
    left_join(overall_leader_stage_tallied_time, by = c("stage_number_order")) |>
    mutate(tally_total_stage_time_overall_leader_time = as.double(tally_total_stage_time_overall_leader_time)) |>
    mutate(stage_time_from_overall_leader = stage_time-stage_time_overall_leader_time) |>
    mutate(stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                      .default = stage_time_from_overall_leader)) |>
    mutate(stage_time_from_overall_leader_varchar = as.character(stage_time_from_overall_leader)) |>
    mutate(tally_total_stage_time_overall_leader_time = as.double(tally_total_stage_time_overall_leader_time)) |>
    mutate(tally_total_stage_time = as.double(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_varchar = as.character(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_from_overall_leader = tally_total_stage_time-tally_total_stage_time_overall_leader_time) |>
    mutate(tally_total_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                  .default = tally_total_stage_time_from_overall_leader)) |>
    mutate(tally_total_stage_time_from_overall_leader_varchar = as.character(tally_total_stage_time_from_overall_leader)) |>
    
    ### gc_time_stage
    left_join(overall_leader_gc_time_stage_tallied_time, by = c("stage_number_order")) |>
    mutate(tally_total_gc_time_stage_time_overall_leader_time = as.double(tally_total_gc_time_stage_time_overall_leader_time)) |>
    mutate(gc_time_stage_time_from_overall_leader = gc_time_stage-gc_time_stage_time_overall_leader_time) |>
    mutate(gc_time_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                              .default = gc_time_stage_time_from_overall_leader)) |>
    mutate(gc_time_stage_time_from_overall_leader_varchar = as.character(gc_time_stage_time_from_overall_leader)) |>
    mutate(tally_total_gc_time_stage_time_overall_leader_time = as.double(tally_total_gc_time_stage_time_overall_leader_time)) |>
    mutate(tally_total_gc_time_stage = as.double(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_varchar = as.character(tally_total_gc_time_stage)) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader = tally_total_gc_time_stage-tally_total_gc_time_stage_time_overall_leader_time) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader = case_when(stage_number_order_all_races_tally_percent != 1 ~ NA,
                                                                          .default = tally_total_gc_time_stage_time_from_overall_leader)) |>
    mutate(tally_total_gc_time_stage_time_from_overall_leader_varchar = as.character(tally_total_gc_time_stage_time_from_overall_leader))
  
  final_stage_tally_total <- results_pivot_sort3c |>
    filter(stage_number_order == races_selected) |>
    select(pivot_id,
           final_stage_total_gc_time_stage_from_overall_leader = tally_total_gc_time_stage_time_from_overall_leader,
           final_stage_total_stage_from_overall_leader = tally_total_stage_time_from_overall_leader) |>
    mutate(final_stage_total_gc_time_stage_from_overall_leader_varchar = as.character(final_stage_total_gc_time_stage_from_overall_leader),
           final_stage_total_stage_from_overall_leader_varchar = as.character(final_stage_total_stage_from_overall_leader))
  
  results_pivot_sort3d <- results_pivot_sort3c |>
    left_join(final_stage_tally_total, by = "pivot_id") |>
    left_join(entered_all_races_tally_sort, by = "pivot_id") |>
    mutate(tally_stage_number_sort = case_when(is.na(tally_stage_number_sort) == TRUE ~ 0,
                                               .default = tally_stage_number_sort))
  
  results_pivot_sort4 <- results_pivot_sort3d |>
    mutate(value_from = case_when(
      # 1 = Individual Stage Metric
      # 2 = Individual Stage Position
      # 3 = Individual Stage Metric from Stage Leader
      # 4 = Individual Stage Metric from Overall Leader
      # 5 = Tallied Individual Stage Metric
      # 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader
      # 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader
      value_from_function == "Stage - 1" ~ stage_time_varchar,
      value_from_function == "Stage - 2" ~ stage_position_varchar,
      value_from_function == "Stage - 3" ~ stage_time_from_leader_varchar,
      value_from_function == "Stage - 4" ~ stage_time_from_overall_leader_varchar,
      value_from_function == "Stage - 5" ~ tally_total_stage_time_varchar,
      value_from_function == "Stage - 6" ~ tally_total_stage_time_from_leader_varchar,
      value_from_function == "Stage - 7" ~ tally_total_stage_time_from_overall_leader_varchar,
      value_from_function == "GC - 1" ~ gc_time_stage_varchar,
      value_from_function == "GC - 2" ~ gc_time_stage_position_edit,
      value_from_function == "GC - 3" ~ gc_time_stage_from_leader_varchar,
      value_from_function == "GC - 4" ~ gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "GC - 5" ~ tally_total_gc_time_stage_varchar,
      value_from_function == "GC - 6" ~ tally_total_gc_time_stage_from_leader,
      value_from_function == "GC - 7" ~ tally_total_gc_time_stage_time_from_overall_leader_varchar,
      value_from_function == "GC - 8" ~ gc_time_bonus_varchar,
      .default = stage_position_varchar)) |>
    mutate(value_from_metric = case_when(
      # Aggregated Metrics
      value_from_function == "Stage - 1" ~ total_stage_time,
      value_from_function == "Stage - 2" ~ avg_position_stage,
      value_from_function == "Stage - 3" ~ total_stage_time_from_leader,
      value_from_function == "Stage - 4" ~ final_stage_total_stage_from_overall_leader,
      value_from_function == "Stage - 5" ~ total_stage_time,
      value_from_function == "Stage - 6" ~ total_stage_time_from_leader,
      value_from_function == "Stage - 7" ~ final_stage_total_stage_from_overall_leader,
      value_from_function == "GC - 1" ~ total_gc_time_stage,
      value_from_function == "GC - 2" ~ avg_position_gc_time_stage,
      value_from_function == "GC - 3" ~ total_gc_time_stage_from_leader,
      value_from_function == "GC - 4" ~ final_stage_total_gc_time_stage_from_overall_leader,
      value_from_function == "GC - 5" ~ total_gc_time_stage,
      value_from_function == "GC - 6" ~ total_gc_time_stage_from_leader,
      value_from_function == "GC - 7" ~ final_stage_total_gc_time_stage_from_overall_leader,
      value_from_function == "GC - 8" ~ total_bonus_seconds*-1,
      .default = avg_position_stage
      
    )) |>
    left_join(calendar_function(""), by = c("season","first_cycling_race_id","stage_number")) |>
    mutate(names_from = paste0(season, " | ",race_name," | ",stage_number," | ",stage_profile_category_mapping_eng)) |>
    mutate(stg_number = as.double(stage_number)) |>
    arrange(start_date,stg_number) |>
    select(-c(stage_time_varchar,stage_time_from_leader_varchar,stage_time,
              stage_time_behind_first
              #,gc_time_stage_from_overall_leader_stage_time
              #,gc_time_stage_overall_leader_stage_time
              ,first_cycling_race_id,season,stage_profile_category_mapping_eng,stage_number,race_name,
              start_date,stg_number,
              race_nationality,gender,category,uci_race_classification,stage_race_boolean,
              end_date,
              race_tags,
              route,distance,
              stage_number
              ,tally_total_stage_time,tally_total_stage_time_from_leader
              #,best_result_gc
              ,gc_time_stage,
              gc_time_stage_varchar,gc_time_stage_from_leader_varchar,stage_number_int,tally_total_gc_time_stage,tally_total_gc_time_stage_from_leader
              ,total_stage_time,total_stage_time_from_leader,gc_time_stage_behind_first,
              total_gc_time_stage_from_leader,
              stage_position_edit,gc_time_stage_position_edit,gc_position_edit,avg_position_gc_time_stage,
              stage_position_varchar
              #,stage_time_overall_leader_stage_time
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
              #,avg_position_gc
    ))
  #relocate(time_from_leader,total_stage_time) |>
  
  
  
  results_pivot_sort5 <- results_pivot_sort4 |>
    pivot_wider(
      names_from = names_from,
      values_from = value_from
    )
  
  ##### this needs working on #####
  
  #?contains()
  
  results_pivot_sort7 <- results_pivot_sort5 |>
    # table sort 1 looks into if tallied (races until tally breaks) or not (races_finished)
    mutate(table_sort1 = case_when(str_detect(value_from_function,'5') == TRUE ~ tally_stage_number_sort*-1,
                                   str_detect(value_from_function,'6') == TRUE ~ tally_stage_number_sort*-1,
                                   str_detect(value_from_function,'7') == TRUE ~ tally_stage_number_sort*-1,
                                   .default = as.double(0)*-1)) |>
    # table sort 2 is just races_finished
    mutate(table_sort2 = as.double(races_finished)*-1) |>
    mutate(table_sort3 = as.double(races_count)*-1) |>
    # table sort.3 looks at metric
    # 1 = Individual Stage Metric | avg time/score
    # 2 = Individual Stage Position | avg position
    # 3 = Individual Stage Metric from Stage Leader | avg time/score
    # 4 = Individual Stage Metric from Overall Leader | avg time/score
    # 5 = Tallied Individual Stage Metric | avg time/score
    # 6 = Tallied Individual Stage Metric from Tallied Individual Stage Leader | avg time/score
    # 7 = Tallied Individual Stage Metric from Overall Tallied Stage Leader | avg time/score
    
    mutate(table_sort4 = value_from_metric) |>
    mutate(table_sort5 = avg_position_stage) |>
    # Victories, Podiums, top5s, top10s
    mutate(table_sort6 = as.double(victories),
           table_sort7 = as.double(podiums),
           table_sort8 = as.double(topfives),
           table_sort9 = as.double(toptens),) |>
    
    arrange(
      table_sort1,
      table_sort2,table_sort3
      ,table_sort4
      ,table_sort5,table_sort6,table_sort7,table_sort8,table_sort9
    ) |>
    mutate(rank = row_number()) |>
    select(-c(
      table_sort1,
      table_sort2
      ,table_sort3
      ,table_sort4
      ,table_sort5,table_sort6,table_sort7,table_sort8,table_sort9
      ,victories,podiums,topfives,toptens,avg_position_gc
      ,tally_stage_number_sort
      ,pivot_id
    ))
  
  #results_pivot_gt <- results_pivot(2023,"Men","Rider","Tallied Stage Time from Leader","Down Under Races","","","") |>
  results_pivot_gt <- results_pivot_sort7 |>
    mutate(avg_position_stage = round(avg_position_stage,1)) |>
    gt() |>
    cols_align(align = c("center")) |>
    cols_move_to_start(rank) |>
    cols_move(value_from_metric,total_gc_time_stage) |>
    cols_move(total_bonus_seconds,total_gc_time_stage) |>
    #cols_move(total_stage_time_from_leader,total_stage_time) |>
    #cols_move(gc_rank,avg_position_stage) |>
    cols_label(
      pivot_name = "Name",
      rank = "Rank",
      "avg_position_stage" = "Avg Position",
      "total_gc_time_stage" = "GC Time",
      #           "gc_time_stage_behind_first" = "GC Time from Leader",
      #           "pivot_id" = "ID",
      "races_finished" = "Races Finished",
      "races_count" = "Race Startlist",
      total_bonus_seconds = "Bonus Seconds*",
      value_from_metric = "Metric"
      #           "gc_rank" = "GC Rank"
    ) |>
    cols_hide(value_from_metric) |>
    #gt_badge(palette = c("1" = "gold","2" = "#A7A7AD", "3" = "#A77044")) |>
    tab_header(title = md("**Cycling Analysis by CyclingChaos.co.uk**")) |>
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
      footnote = "Data from FirstCycling.com | Bonus Seconds* calculated by GC Time on a Stage minus Stage Time"
    )
  
}

print(results_pivot(2023,"Men","Rider","GC - 8","Aussie WT","","",""))
