
library(tidyverse)
library(ggplot2)
library(ggtext)

##### START LIST HEATMAP #####

startlist_heatmap <- function(season_function,gender_function,race_collection_filter_function){
  # need to put cleaned results csv into github
  results_data <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/results.csv') |>
    left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/frontend_csv/calendar.csv') |> select(season,first_cycling_race_id,race_tags), by = c("season","first_cycling_race_id")) |>
    filter(season == season_function, gender == gender_function,str_detect(race_tags,race_collection_filter_function))
  
  startlists_a <- results_data |>
    arrange(desc(start_date),desc(end_date)) |>
    select(first_cycling_race_id,race_name,first_cycling_rider_id) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id),
           first_cycling_rider_id = as.character(first_cycling_rider_id)) |>
    #filter(first_cycling_race_id == 1 | first_cycling_race_id == 1172) |>
    unique()
  
  race_id_max_riders = startlists_a |>
    unique() |>
    group_by(first_cycling_race_id) |>
    summarise(rider_entry = n())
  
  startlist_data <- startlists_a |>
    left_join(startlists_a, by = c("first_cycling_rider_id"),relationship = "many-to-many") |>
    rename(first_cycling_race_id_x_axis = first_cycling_race_id.x) |>
    rename(race_name_x_axis = race_name.x) |>
    rename(first_cycling_race_id_y_axis = first_cycling_race_id.y) |>
    rename(race_name_y_axis = race_name.y) |>
    group_by(first_cycling_race_id_x_axis,race_name_x_axis,first_cycling_race_id_y_axis,race_name_y_axis) |>
    summarise(rider_count = n()) |>
    ungroup() |>
    left_join(race_id_max_riders |> rename(rider_entry_x_axis = rider_entry), by = c("first_cycling_race_id_x_axis" = "first_cycling_race_id")) |>
    left_join(race_id_max_riders |> rename(rider_entry_y_axis = rider_entry), by = c("first_cycling_race_id_y_axis" = "first_cycling_race_id")) |>
    group_by(first_cycling_race_id_x_axis,race_name_x_axis,first_cycling_race_id_y_axis,race_name_y_axis) |>
    mutate(rider_entry = min(rider_entry_x_axis,rider_entry_y_axis)) |>
    select(-c(rider_entry_x_axis,rider_entry_y_axis)) |>
    mutate(percent_of_max_entry = round(rider_count/rider_entry*100,1)) |>
    ungroup() |>
    mutate(max_entry2 = max(rider_count)) |>
    mutate(percent_of_max_entry2 = round(rider_count/max_entry2*100,1))
  
  
  startlist_data %>%
    ggplot(aes(x = race_name_x_axis, y = race_name_y_axis)) +
    geom_tile(aes(fill = percent_of_max_entry2)) +
    geom_richtext(aes(label = paste0(rider_count,' | ',percent_of_max_entry,'%'), color = '#2C2F2B'), size = 7,
                  label.color = NA, fill = NA) +
    scale_color_identity() +
    scale_fill_gradient(low = '#F2F2F2', high = '#F7565A', limits =c(0,100)) +
    #scale_fill_gradient(low = '#F2F2F2', high = '#F7565A') +
    coord_fixed(clip = 'off') +
    theme_minimal() +
    theme(legend.position = 'none') +
    labs(x = "Race Name", y = "Race Name",
         title = "Start List Comparison Heat Map",
         subtitle = "By CyclingChaos.co.uk",
         caption = "Using FirstCycling.com Data")
}

print(startlist_heatmap(2024,'women','Aussie WT'))

