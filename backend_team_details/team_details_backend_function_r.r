library(tidyverse)

team_details_function <- function() {
  team_details_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_team_details/CyclingChaos_backend_team_details.csv') |>
  mutate(team_name = ifelse(first_cycling_team_id == 'None',team_name_invitational,team_name)) |>
  mutate(uci_division_name = replace_na(uci_division_name,'Invitational Team'))
}
