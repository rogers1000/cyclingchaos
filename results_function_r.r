library(tidyverse)

results_function <- function() {
  results_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_RaceResults_2023.csv') |>
    left_join(team_details <- team_details_function(), by = c('season','team_id')) |>
    mutate(team_name = ifelse(team_id == 'None',team_name_invitational,team_name)) |>
    mutate(uci_division = replace_na(uci_division,'Invitational Team')) |>
    select(-c(team_name_invitational,uci_division,race_nationality)) |>
    relocate(team_name,.after = team_id)
}
