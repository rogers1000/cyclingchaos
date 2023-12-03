library(tidyverse)

team_details_function <- function() {
  team_details_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_team_details.csv') |>
  mutate(team_id = as.character(team_id)) |>
  mutate(team_name = ifelse(team_id == 'None',team_name_invitational,team_name)) |>
  mutate(uci_division = replace_na(uci_division,'Invitational Team'))
}
