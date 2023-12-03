library(tidyverse)

calendar_function <- function() {
  calendar_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/CyclingChaos_RaceCalendar.csv') |>
    mutate(race_id = as.character(race_id)) |>
    select(-race_tag) |>
    mutate(race_tag_monument = case_when(race_id == "4" ~ "Monument",
                                         race_id == "5" ~ "Monument",
                                         race_id == "8" ~ "Monument",
                                         race_id == "11" ~ "Monument",
                                         race_id == "24" ~ "Monument",
                                         .default = "")) |>
    mutate(race_tag_world_tour = case_when(str_detect(uci_race_classification,'UWT') ~ "World Tour",
                                           .default = "")) |>
    mutate(race_tag_big7 = case_when(race_id == "4" ~ "Big7",
                                         race_id == "5" ~ "Big7",
                                         race_id == "8" ~ "Big7",
                                         race_id == "11" ~ "Big7",
                                         race_id == "24" ~ "Big7",
                                         race_id == "26" ~ "Big7",
                                         race_id == "54" ~ "Big7",
                                         .default = "")) |>
    mutate(race_tag_grandtour = case_when(race_id == "13" ~ "Grand Tour",
                                          race_id == "17" ~ "Grand Tour",
                                          race_id == "23" ~ "Grand Tour",
                                          .default = "")) |>
    mutate(race_tag_cobbled_classic = case_when(race_id == "53" ~ "Cobbled Classic",
                                                race_id == "84" ~ "Cobbled Classic",
                                                race_id == "116" ~ "Cobbled Classic",
                                                race_id == "40" ~ "Cobbled Classic",
                                                race_id == "47" ~ "Cobbled Classic",
                                                race_id == "7" ~ "Cobbled Classic",
                                                race_id == "75" ~ "Cobbled Classic",
                                                race_id == "131" ~ "Cobbled Classic",
                                                race_id == "56" ~ "Cobbled Classic",
                                                race_id == "8" ~ "Cobbled Classic",
                                                .default = "")) |>
    mutate(race_tag_ardennes = case_when(race_id == "9" ~ "Ardennes",
                                          race_id == "10" ~ "Ardennes",
                                          race_id == "11" ~ "Ardennes",
                                          .default = "")) |>
    mutate(race_tag_cobbles_openingweekend = case_when(race_id == "53" ~ "Cobbles Opening Weekend",
                                         race_id == "84" ~ "Cobbles Opening Weekend",
                                         .default = "")) |>
    
    mutate(race_tags = paste(race_tag_monument,race_tag_world_tour,race_tag_big7,race_tag_grandtour,race_tag_cobbled_classic,
                             race_tag_ardennes,race_tag_cobbles_openingweekend,sep = " ")) |>
    select(-c(race_tag_world_tour,race_tag_big7,race_tag_grandtour))
}
