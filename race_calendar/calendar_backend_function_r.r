library(tidyverse)

calendar_function <- function(gc_or_stage_function) {
  calendar_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/race_calendar/CyclingChaos_RaceCalendar.csv') |>
    #left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/mapping_dfs/CyclingChaos_nationality_mapping.csv') |> select(nationality_id_two,nationality_name) |> filter(nationality_id_two != ""), by = c("race_nationality" = "nationality_id_two")) |>
    #mutate(nationality_name = case_when(is.na(nationality_name) ~ race_nationality,
    #                                    .default = nationality_name)) |>
    mutate(first_cycling_race_id = as.character(first_cycling_race_id)) |>
    mutate(race_tag_monument = case_when(first_cycling_race_id == "4" ~ "Monument",
                                         first_cycling_race_id == "5" ~ "Monument",
                                         first_cycling_race_id == "8" ~ "Monument",
                                         first_cycling_race_id == "11" ~ "Monument",
                                         first_cycling_race_id == "24" ~ "Monument",
                                         .default = "")) |>
    mutate(race_tag_world_tour = case_when(str_detect(uci_race_classification,'UWT') ~ "World Tour",
                                           .default = "")) |>
    mutate(race_tag_big7 = case_when(first_cycling_race_id == "4" ~ "Big7",
                                     first_cycling_race_id == "5" ~ "Big7",
                                     first_cycling_race_id == "8" ~ "Big7",
                                     first_cycling_race_id == "11" ~ "Big7",
                                     first_cycling_race_id == "24" ~ "Big7",
                                     first_cycling_race_id == "26" ~ "Big7",
                                     first_cycling_race_id == "54" ~ "Big7",
                                         .default = "")) |>
    mutate(race_tag_grandtour = case_when(first_cycling_race_id == "13" ~ "Grand Tour",
                                          first_cycling_race_id == "17" ~ "Grand Tour",
                                          first_cycling_race_id == "23" ~ "Grand Tour",
                                          .default = "")) |>
    mutate(race_tag_cobbled_classic = case_when(first_cycling_race_id == "53" ~ "Cobbled Classic",
                                                first_cycling_race_id == "84" ~ "Cobbled Classic",
                                                first_cycling_race_id == "116" ~ "Cobbled Classic",
                                                first_cycling_race_id == "40" ~ "Cobbled Classic",
                                                first_cycling_race_id == "47" ~ "Cobbled Classic",
                                                first_cycling_race_id == "7" ~ "Cobbled Classic",
                                                first_cycling_race_id == "75" ~ "Cobbled Classic",
                                                first_cycling_race_id == "131" ~ "Cobbled Classic",
                                                first_cycling_race_id == "56" ~ "Cobbled Classic",
                                                first_cycling_race_id == "8" ~ "Cobbled Classic",
                                                first_cycling_race_id == "5" ~ "Cobbled Classic",
                                                .default = "")) |>
    mutate(race_tag_ardennes = case_when(first_cycling_race_id == "9" ~ "Ardennes",
                                          first_cycling_race_id == "10" ~ "Ardennes",
                                          first_cycling_race_id == "11" ~ "Ardennes",
                                          .default = "")) |>
    mutate(race_tag_cobbles_openingweekend = case_when(first_cycling_race_id == "53" ~ "Cobbles Opening Weekend",
                                         first_cycling_race_id == "84" ~ "Cobbles Opening Weekend",
                                         .default = "")) |>
    
    mutate(race_tags = paste(race_tag_monument,race_tag_world_tour,race_tag_big7,race_tag_grandtour,race_tag_cobbled_classic,
                             race_tag_ardennes,race_tag_cobbles_openingweekend,sep = " ")) |>
    select(-c(race_tag_monument,race_tag_world_tour,race_tag_big7,race_tag_grandtour,race_tag_cobbled_classic,
              race_tag_ardennes,race_tag_cobbles_openingweekend)) |>
    left_join(read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/race_calendar/CyclingChaos_RaceCalendar_stages.csv') |> mutate(first_cycling_race_id = as.character(first_cycling_race_id)), by = c('season','first_cycling_race_id')) |>
    mutate(stage_profile_category = case_when(stage_profile_category == "Flatt" ~ "Flat",
                                              stage_profile_category == "Tempo" ~ "Flat ITT",
                                              stage_profile_category == "Bakketempo" ~ "Mountain ITT",
                                              stage_profile_category == "Fjell-MF" ~ "Mountain MTF",
                                              stage_profile_category == "Fjell" ~ "Mountain",
                                              stage_profile_category == "Smaakupert-MF" ~ "Hilly MTF",
                                              stage_profile_category == "Smaakupert" ~ "Hilly",
                                              stage_profile_category == "Brosten" ~ "Cobbles",
                                              stage_profile_category == "Lagtempo" ~ "TTT",
                                              stage_profile_category == "Ukjent" ~ "Unknown",
                                              stage_profile_category == "<td></td>" ~ "Unknown",
                                              .default = stage_profile_category))
}
