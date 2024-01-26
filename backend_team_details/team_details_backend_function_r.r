library(tidyverse)

team_details_function <- function() {
  # load in csv
  team_details_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_team_details/CyclingChaos_backend_team_details.csv') |>
  # if no team name then use invitational team name
  mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
  # if no uci_division then put as "Invitational Team"
  mutate(uci_division_name = replace_na(uci_division_name,'Invitational Team'))
}

