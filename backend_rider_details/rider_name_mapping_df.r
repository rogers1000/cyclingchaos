rider_name_mapping_df_function <- function() {
  df <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_results/CyclingChaos_RaceResults_df_master.csv') |>
    select(first_cycling_rider_id,first_cycling_rider_name,end_date) |>
    unique() |>
    group_by(first_cycling_rider_id) |>
    mutate(last_race_for_rider = max(end_date)) |>
    ungroup() |>
    mutate(first_cycling_rider_name_latest = case_when(last_race_for_rider == end_date ~ first_cycling_rider_name,
                                                       .default = "filter_out")) |>
    filter(first_cycling_rider_name_latest != "filter_out") |>
    select(first_cycling_rider_id, first_cycling_rider_name = first_cycling_rider_name_latest)
}
