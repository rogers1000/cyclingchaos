library(tidyverse)

results_pivot <- function(season_function,gender_function,detail_slicer_function,value_from_function,race_filter_function) {
  results_pivot_filters <- results_function() |>
    filter(season == season_function, gender == gender_function) |>
    left_join(calendar_function() |> select(first_cycling_race_id,race_tags) |> unique(), by = "first_cycling_race_id") |>
    mutate(position_edit_gc = case_when(stage == "GC" & position == "DNF" ~ "1100",
                                        stage == "GC" & position == "OOT" ~ "1000",
                                        stage == "GC" & position == "DNS" ~ "1200",
                                        stage == "GC" & position == "DSQ" ~ "1300",
                                        .default = position)) |>
    mutate(position_edit_gc = as.double(position_edit_gc)) |>
    mutate(gc_time_edit = case_when(stage == "GC" & position == "DNF" ~ NA,
                                    stage == "GC" & position == "OOT" ~ NA,
                                    stage == "GC" & position == "DNS" ~ NA,
                                    stage == "GC" & position == "DSQ" ~ NA,
                                    .default = gc_time)) |>
    mutate(gc_time_edit = as.double(gc_time_edit)) |>
    mutate(gc_time_from_leader_edit = case_when(stage == "GC" & position == "DNF" ~ NA,
                                    stage == "GC" & position == "OOT" ~ NA,
                                    stage == "GC" & position == "DNS" ~ NA,
                                    stage == "GC" & position == "DSQ" ~ NA,
                                    .default = gc_time_behind_first)) |>
    mutate(gc_time_from_leader_edit = as.double(gc_time_from_leader_edit)) |>
    mutate(race_filter = case_when(race_filter_function == "" ~ 1,
                                   str_detect(race_tags,race_filter_function) ~ 1,
                                   .default = 0)) |>
    filter(race_filter == 1) |>
    mutate(pivot_id = case_when(detail_slicer_function == "Team" ~ first_cycling_team_id,
                                detail_slicer_function == "Rider" ~ first_cycling_rider_id))
  
  results_pivot_sort <- results_pivot_filters |>
    filter(position_edit_gc < 1000) |>
    group_by(pivot_id,season,first_cycling_race_id) |>
    summarise(best_result_gc = min(position_edit_gc),
              gc_time_edit = min(gc_time_edit),
              gc_time_from_leader_edit = min(gc_time_from_leader_edit)) |>
    ungroup() |>
    group_by(pivot_id) |>
    summarise(avg_position_gc = mean(best_result_gc),
              total_gc_time = sum(gc_time_edit),
              total_gc_time_from_leader = sum(gc_time_from_leader_edit),
              races_finished = n()) |>
    ungroup()
  
  results_pivot_races_count <- results_pivot_filters |>
    #filter(position_edit < 1000) |>
    group_by(pivot_id,season,first_cycling_race_id) |>
    summarise(best_result_gc = min(position_edit_gc),
              gc_time_edit = min(gc_time_edit),
              gc_time_from_leader_edit = min(gc_time_from_leader_edit)) |>
    ungroup() |>
    group_by(pivot_id) |>
    summarise(races_count = n()) |>
    ungroup()
  
  results_pivot <- results_pivot_filters |>
    left_join(results_pivot_sort, by = "pivot_id") |>
    left_join(results_pivot_races_count, by = "pivot_id") |>
    mutate(victory = case_when(position_edit_gc == 1 ~ 1,
                               .default = 0),
           podium = case_when(position_edit_gc < 4 ~ 1,
                              .default = 0),
           topfive = case_when(position_edit_gc < 6 ~ 1,
                               .default = 0),
           topten = case_when(position_edit_gc < 11 ~ 1,
                              .default = 0)) |>
    group_by(start_date,race_name,pivot_id,stage,avg_position_gc,total_gc_time,total_gc_time_from_leader,races_finished,races_count) |>
    #rename(pivot_id)
    summarise(best_result_gc = min(position_edit_gc),
              gc_time_edit = min(gc_time_edit, na.rm = TRUE),
              gc_time_from_leader_edit = min(gc_time_from_leader_edit, na.rm = TRUE),
              victories = sum(victory),
              podiums = sum(podium),
              topfives = sum(topfive),
              toptens = sum(topten)) |>
    ungroup() |>
    mutate(best_result_gc = as.character(best_result_gc)) |>
    mutate(best_result_gc = case_when(
      stage == "GC" & best_result_gc == "1000" ~ "OOT",
      stage == "GC" & best_result_gc == "1100" ~ "DNF",
      stage == "GC" & best_result_gc == "1200" ~ "DNS",
      stage == "GC" & best_result_gc == "1300" ~ "DSQ",
      .default = best_result_gc)) |>
    mutate(gc_time_varchar = as.character(gc_time_edit)) |>
    mutate(gc_time_from_leader_varchar = as.character(gc_time_from_leader_edit)) |>
    view()
  
  results_pivot_gc_time_from_leader <- results_pivot |>
    select(pivot_id,total_gc_time,races_finished) |>
    filter(!is.na(races_finished)) |>
    filter(races_finished == max(races_finished)) |>
    mutate(time_from_leader = as.character(total_gc_time - min(total_gc_time))) |>
    unique() |>
    select(pivot_id,time_from_leader)
  
  results_pivot_sort_summarised <- results_pivot |>
    group_by(pivot_id) |>
    summarise(victories = sum(victories),
              podiums = sum(podiums),
              topfives = sum(topfives),
              toptens = sum(toptens))
  
  results_pivot <- results_pivot |>
    select(-c(victories,podiums,topfives,toptens)) |>
    left_join(results_pivot_gc_time_from_leader, by = "pivot_id") |>
    mutate(value_from = case_when(value_from_function == "GC Time" ~ gc_time_varchar,
                                  value_from_function == "Position" ~ best_result_gc,
                                  value_from_function == "GC Time from Leader" ~ gc_time_from_leader_varchar,
                                  .default = best_result_gc)) |>
    left_join(results_pivot_sort_summarised, by = "pivot_id") |>
    arrange(start_date) |>
    select(-c(start_date,best_result_gc,gc_time_varchar,gc_time_edit,gc_time_from_leader_edit,
              total_gc_time_from_leader,gc_time_from_leader_varchar)) |>
    #relocate(time_from_leader,total_gc_time) |>
    pivot_wider(
      names_from = race_name,
      values_from = value_from
    ) |>
    mutate(table_sort1 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(races_finished)*-1,
                                  detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(races_finished)*-1,
                                  detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(races_finished)*-1,
                                  detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(races_finished)*-1,
                                  detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(races_finished)*-1,
                                  detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(races_finished)*-1,
                                  .default = as.double(races_finished))) |>
    
    mutate(table_sort2 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(races_count)*-1,
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort3 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(avg_position_gc),
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(avg_position_gc),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(total_gc_time),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(total_gc_time),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(time_from_leader),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(time_from_leader),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort4 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(victories),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort5 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(podiums),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort6 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(topfives),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort7 = case_when(detail_slicer_function == "Team" & value_from_function == "Position" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Position" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "GC Time from Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "GC Time from Leader" ~ as.double(toptens),
                                   .default = as.double(avg_position_gc))) |>
    
    arrange(table_sort1,table_sort2,table_sort3,table_sort4,table_sort5,table_sort6,table_sort7) |>
    mutate(rank = row_number()) |>
    select(-c(table_sort1,table_sort2,table_sort3,table_sort4,table_sort5,table_sort6,table_sort7
              ,victories,podiums,topfives,toptens
              ))
}

### Broken

test_results_pivot_gt <- results_pivot(2023,"Men","Team","GC Time from Leader","Ardennes") |>
  mutate(avg_position_gc = round(avg_position_gc,1)) |>
  gt() |>
  cols_move_to_start(rank) |>
  cols_move(time_from_leader,total_gc_time) |>
  cols_label(rank = "Rank") |>
  cols_label("avg_position_gc" = "Avg Position") |>
  cols_label("total_gc_time" = "GC Time") |>
  cols_label("time_from_leader" = "GC Time from Leader") |>
  cols_label("pivot_id" = "ID") |>
  cols_label("races_finished" = "Races Finished") |>
  cols_label("races_count" = "Race Startlist") |>
  #gt_badge(palette = c("1" = "gold","2" = "#A7A7AD", "3" = "#A77044")) |>
  print()
