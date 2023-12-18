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
    mutate(position_edit_gc = case_when(stage == "GC" & position == "DNF" ~ "1100",
                                        stage == "GC" & position == "OOT" ~ "1000",
                                        stage == "GC" & position == "DNS" ~ "1200",
                                        stage == "GC" & position == "DSQ" ~ "1300",
                                        .default = position)) |>
    mutate(position_edit_gc = as.double(position_edit_gc)) |>
    mutate(stage_time_edit = case_when(stage == "GC" & position == "DNF" ~ NA,
                                       stage == "GC" & position == "OOT" ~ NA,
                                       stage == "GC" & position == "DNS" ~ NA,
                                       stage == "GC" & position == "DSQ" ~ NA,
                                       .default = gc_time)) |>
    mutate(stage_time_edit = as.double(stage_time_edit)) |>
    mutate(stage_time_from_leader_edit = case_when(stage == "GC" & position == "DNF" ~ NA,
                                                   stage == "GC" & position == "OOT" ~ NA,
                                                   stage == "GC" & position == "DNS" ~ NA,
                                                   stage == "GC" & position == "DSQ" ~ NA,
                                                   .default = gc_time_behind_first)) |>
    mutate(stage_time_from_leader_edit = as.double(stage_time_from_leader_edit))
  
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
    filter(!(stage == "GC" & stage_race_boolean == "Stage Race")) |>
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
    mutate(stage_or_gc_filter = case_when(str_detect(race_filter_function,"Stages") & (stage != "GC") & (first_cycling_race_id == str_split_i(race_filter_function," - ",-1)) ~ 1,
                                          (!str_detect(race_filter_function,"Stages")) & (stage == "GC") & (first_cycling_race_id == str_split_i(race_filter_function," - ",-1)) ~ 1,
                                          .default = 0)) |>
    filter(race_filter_race_collection == 1 | race_filter_rider == 1 | race_filter_team == 1 | stage_or_gc_filter == 1) |>
    #filter(stage_or_gc_filter == 1) |>
    mutate(pivot_id = case_when(detail_slicer_function == "Team" ~ first_cycling_team_id,
                                detail_slicer_function == "Rider" ~ first_cycling_rider_id))
  
  races_selected <- dplyr::pull(results_pivot_filters |>
                                  select(first_cycling_race_id,stage) |>
                                  unique() |>
                                  summarise(count = n()),count)
  
  results_pivot_races_count <- results_pivot_filters |>
    group_by(pivot_id) |>
    summarise(races_count = n_distinct(paste0(first_cycling_race_id,"_",stage)))
  
  results_pivot_sort <- results_pivot_filters |>
    filter(position_edit_gc < 1000) |>
    mutate(victory = case_when(position_edit_gc == 1 ~ 1,
                               .default = 0),
           podium = case_when(position_edit_gc < 4 ~ 1,
                              .default = 0),
           topfive = case_when(position_edit_gc < 6 ~ 1,
                               .default = 0),
           topten = case_when(position_edit_gc < 11 ~ 1,
                              .default = 0)) |>
    group_by(pivot_id,season,first_cycling_race_id,stage) |>
    summarise(best_result_stage = min(position_edit_gc),
              stage_time_edit = min(stage_time_edit),
              stage_time_from_leader_edit = min(stage_time_from_leader_edit),
              victories = sum(victory),
              podiums = sum(podium),
              topfives = sum(topfive),
              toptens = sum(topten)) |>
    ungroup() |>
    group_by(pivot_id) |>
    summarise(avg_position_gc = mean(best_result_stage),
              total_stage_time = sum(stage_time_edit),
              #total_stage_time_from_leader = sum(stage_time_from_leader_edit),
              victories = sum(victories),
              podiums = sum(podiums),
              topfives = sum(topfives),
              toptens = sum(toptens),
              races_finished = n()) |>
    ungroup() |>
    mutate(total_stage_time = case_when(races_finished != races_selected ~ NA,
                                        .default = total_stage_time)) |>
    mutate(total_stage_time_from_leader = total_stage_time-min(total_stage_time, na.rm = TRUE)) |>
    left_join(results_pivot_races_count, by = "pivot_id")
  
  results_pivot_sort2 <- results_pivot_filters |>
    filter(position_edit_gc < 1000) |>
    group_by(pivot_id,season,first_cycling_race_id,stage) |>
    summarise(best_result_stage = min(position_edit_gc),
              stage_time_edit = min(stage_time_edit),
              stage_time_from_leader_edit = min(stage_time_from_leader_edit)) |>
    ungroup() |>
    left_join(results_pivot_sort, by = "pivot_id")
  
  
  results_pivot_sort3 <- results_pivot_sort2 |>
    filter(stage_time_edit != Inf) |>
    mutate(best_result_stage = as.character(best_result_stage)) |>
    mutate(best_result_stage = case_when(
      best_result_stage == "1000" ~ "OOT",
      best_result_stage == "1100" ~ "DNF",
      best_result_stage == "1200" ~ "DNS",
      best_result_stage == "1300" ~ "DSQ",
      #stage == "GC" & best_result_stage == "1000" ~ "OOT",
      #stage == "GC" & best_result_stage == "1100" ~ "DNF",
      #stage == "GC" & best_result_stage == "1200" ~ "DNS",
      #stage == "GC" & best_result_stage == "1300" ~ "DSQ",
      .default = best_result_stage)) |>
    mutate(stage_time_varchar = as.character(stage_time_edit)) |>
    mutate(stage_time_from_leader_varchar = as.character(stage_time_from_leader_edit)) |>
    mutate(stage_number = as.double(stage)) |>
    arrange(first_cycling_race_id,pivot_id,stage_number) |>
    group_by(first_cycling_race_id,pivot_id) |>
    mutate(tally_total_stage_time = cumsum(stage_time_edit)) |>
    ungroup() |>
    group_by(first_cycling_race_id,stage) |>
    mutate(tally_total_stage_time_from_leader = tally_total_stage_time-min(tally_total_stage_time)) |>
    ungroup() |>
    mutate(tally_total_stage_time = as.character(tally_total_stage_time)) |>
    mutate(tally_total_stage_time_from_leader = as.character(tally_total_stage_time_from_leader))
  
  ?cumsum()
  
  results_pivot_gc_leader_rank <- results_pivot_sort3 |>
    arrange(-races_finished,-races_count,total_stage_time,-victories,-podiums,-topfives,-toptens) |>
    select(pivot_id,total_stage_time) |>
    unique() |>
    mutate(gc_rank = case_when(is.na(total_stage_time) ~ NA,
                               .default = row_number())) |>
    select(-total_stage_time) |>
    ungroup()
  
  results_pivot_sort3b <- results_pivot_sort3 |>
    left_join(results_pivot_gc_leader_rank, by = "pivot_id") |>
    mutate(gc_time_overall_leader_stage_time = case_when(gc_rank == 1 ~ stage_time_edit,
                                                         .default = 0)) |>
    group_by(first_cycling_race_id,stage) |>
    mutate(gc_time_overall_leader_stage_time = max(gc_time_overall_leader_stage_time)) |>
    ungroup() |>
    mutate(gc_time_from_overall_leader_stage_time = stage_time_edit-gc_time_overall_leader_stage_time) |>
    mutate(gc_time_from_overall_leader_stage_time = as.character(gc_time_from_overall_leader_stage_time))
  
  results_pivot_sort4 <- results_pivot_sort3b |>
    mutate(value_from = case_when(value_from_function == "Stage Time" ~ stage_time_varchar,
                                  value_from_function == "Stage Position" ~ best_result_stage,
                                  value_from_function == "Stage Time from Stage Leader" ~ stage_time_from_leader_varchar,
                                  value_from_function == "Stage Time from Overall Leader" ~ gc_time_from_overall_leader_stage_time,
                                  value_from_function == "Tallied Stage Time" ~ tally_total_stage_time,
                                  value_from_function == "Tallied Stage Time from Leader" ~ tally_total_stage_time_from_leader,
                                  .default = best_result_stage)) |>
    #mutate(names_from = paste0(race_name," | ",stage)) |>
    left_join(calendar_function(""), by = c("season","first_cycling_race_id","stage" = "stage_number")) |>
    mutate(names_from = paste0(season, " | ",race_name," | ",stage," | ",stage_profile_category)) |>
    mutate(stg_number = as.double(stage)) |>
    arrange(start_date,stg_number) |>
    select(-c(stage_time_varchar,best_result_stage,stage_time_from_leader_varchar,stage_time_edit,
              stage_time_from_leader_edit
              ,gc_time_from_overall_leader_stage_time
              ,gc_time_overall_leader_stage_time
              ,first_cycling_race_id,season,stage_profile_category,stage,race_name,
              start_date,stg_number,
              race_nationality,gender,category,uci_race_classification,stage_race_boolean,end_date,race_tags,
              route,distance,
              stage_number
              ,tally_total_stage_time,tally_total_stage_time_from_leader
    ))
  #relocate(time_from_leader,total_stage_time) |>
  
  
  
  results_pivot_sort5 <- results_pivot_sort4 |>
    pivot_wider(
      names_from = names_from,
      values_from = value_from
    )
  
  results_pivot_sort6 <- results_pivot_sort5 |>
    mutate(table_sort1 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(races_finished)*-1,
                                   .default = as.double(races_finished))) |>
    
    mutate(table_sort2 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(races_count)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(races_finished)*-1,
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(races_finished)*-1,
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort3 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(avg_position_gc),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(avg_position_gc),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(total_stage_time),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(total_stage_time),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(total_stage_time_from_leader),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(total_stage_time_from_leader),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort4 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(victories),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(victories),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(victories),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort5 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(podiums),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(podiums),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(podiums),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort6 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(topfives),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(topfives),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(topfives),
                                   .default = as.double(avg_position_gc))) |>
    
    mutate(table_sort7 = case_when(detail_slicer_function == "Team" & value_from_function == "Stage Position" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Position" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Stage Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Stage Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "Stage Time from Overall Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Stage Time from Overall Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time" ~ as.double(toptens),
                                   detail_slicer_function == "Team" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(toptens),
                                   detail_slicer_function == "Rider" & value_from_function == "Tallied Stage Time from Leader" ~ as.double(toptens),
                                   .default = as.double(avg_position_gc))) |>
    
    arrange(table_sort1,table_sort2,table_sort3,table_sort4,table_sort5,table_sort6,table_sort7) |>
    #filter(stage == "GC") |>
    mutate(rank = row_number()) |>
    arrange(-races_finished,-races_count,total_stage_time,-victories,-podiums,-topfives,-toptens) |>
    mutate(gc_rank = case_when(is.na(total_stage_time) ~ NA,
                               .default = row_number())) |>
    arrange(rank) |>
    select(-c(table_sort1,table_sort2,table_sort3,table_sort4,table_sort5,table_sort6,table_sort7
              ,victories,podiums,topfives,toptens,
              #tally_total_stage_time,tally_total_stage_time_from_leader
              #season,first_cycling_race_id
              #,names_from
    ))
}
  
  results_pivot_gt <- results_pivot(2023,"Men","Rider","Stage Time","Down Under Races","","","") |>
  #results_pivot_gt <- results_pivot_sort6 |>
    mutate(avg_position_gc = round(avg_position_gc,1)) |>
    gt() |>
    cols_align(align = c("center")) |>
    cols_move_to_start(rank) |>
    cols_move(total_stage_time_from_leader,total_stage_time) |>
    cols_move(gc_rank,avg_position_gc) |>
    cols_label(rank = "Rank",
               "avg_position_gc" = "Avg Position",
               "total_stage_time" = "GC Time",
               "total_stage_time_from_leader" = "GC Time from Leader",
               "pivot_id" = "ID",
               "races_finished" = "Races Finished",
               "races_count" = "Race Startlist",
               "gc_rank" = "GC Rank") |>
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
      footnote = "Data from FirstCycling.com"
    ) |>
    print()
  
