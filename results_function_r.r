library(tidyverse)

results_function <- function() {
  results_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_RaceResults_2023.csv') |>
    left_join(team_details <- team_details_function(), by = c('season','team_id')) |>
    mutate(team_name = ifelse(team_id == 'None',team_name_invitational,team_name)) |>
    select(-c(team_name_invitational,uci_division,race_nationality,gc_position,X,gc_time,race_tag)) |>
    relocate(team_name,.after = team_id) |>
    mutate(rider_id = as.character(rider_id)) |>
    mutate(team_id = as.character(team_id)) |>
    mutate(race_id = as.character(race_id))
}
