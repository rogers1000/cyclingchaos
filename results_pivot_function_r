library(tidyverse)

results_pivot <- function(season_function,gender_function,detail_slicer_function,race_filter_function) {
  results_pivot_filters <- results_function() |>
    filter(season == season_function, gender == gender_function) |>
    left_join(calendar_function() |> select(race_id,race_tags), by = "race_id") |>
    mutate(position_edit = case_when(position == "DNF" ~ "1100",
                                     position == "OOT" ~ "1000",
                                     position == "DNS" ~ "1200",
                                     position == "DSQ" ~ "1300",
                                     .default = position)) |>
    mutate(position_edit = as.double(position_edit)) |>
    mutate(race_filter = case_when(race_filter_function == "" ~ 1,
                                   str_detect(race_tags,race_filter_function) ~ 1,
                                   .default = 0)) |>
    filter(race_filter == 1) |>
    mutate(pivot_name = case_when(detail_slicer_function == "Team" ~ team_name,
                                  detail_slicer_function == "Rider" ~ rider_id))
  
  results_pivot_sort <- results_pivot_filters |>
    filter(position_edit < 1000) |>
    group_by(pivot_name,race_id) |>
    summarise(best_result = min(position_edit)) |>
    ungroup() |>
    group_by(pivot_name) |>
    summarise(avg_position = mean(best_result),race_count = n()) |>
    ungroup()
  
  results_pivot <- results_pivot_filters |>
    left_join(results_pivot_sort, by = "pivot_name") |>
    group_by(start_date,race_name,pivot_name,avg_position,race_count) |>
    #rename(pivot_name)
    summarise(best_result = min(position_edit)) |>
    ungroup() |>
    arrange(start_date) |>
    select(-start_date) |>
    pivot_wider(
      names_from = race_name,
      values_from = best_result
    ) |>
    mutate(table_sort = case_when(pivot_name_function == "Team" ~avg_position*-1,
                                  pivot_name_function == "Rider" ~ race_count)) |>
    arrange(-table_sort,avg_position) |>
    select(-c(table_sort))
}
