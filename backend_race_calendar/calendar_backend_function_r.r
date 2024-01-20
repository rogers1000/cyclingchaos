library(tidyverse)

calendar_function <- function(gc_or_stage_function) {
    calendar_csv <- read.csv('https://raw.githubusercontent.com/rogers1000/cyclingchaos/main/backend_race_calendar/CyclingChaos_RaceCalendar_df_master.csv') |>
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
    mutate(race_tag_aussie_kiwi_wt = case_when(first_cycling_race_id == "1" ~ "Aussie WT",
                                               first_cycling_race_id == "1172" ~ "Aussie WT",
                                               .default = "")) |>
    mutate(race_tag_middle_east = case_when(first_cycling_race_id == "868" ~ "Middle East Races",
                                            #first_cycling_race_id == "57" ~ "Middle East Races",
                                            first_cycling_race_id == "9800" ~ "Middle East Races",
                                               .default = "")) |>
    mutate(race_tag_world_champs = case_when(first_cycling_race_id == "26" ~ "World Champs",
                                               first_cycling_race_id == "27" ~ "World Champs",
                                               .default = "")) |>
    mutate(race_tag_euro_champs = case_when(first_cycling_race_id == "4020" ~ "Euro Champs",
                                             first_cycling_race_id == "4019" ~ "Euro Champs",
                                             .default = "")) |>
    mutate(race_tag_mallorca4 = case_when(first_cycling_race_id == "100" ~ "Mallorca Warmup",
                                          first_cycling_race_id == "271" ~ "Mallorca Warmup",
                                          first_cycling_race_id == "274" ~ "Mallorca Warmup",
                                          first_cycling_race_id == "83" ~ "Mallorca Warmup",
                                            .default = "")) |>
    mutate(race_tags = paste(race_tag_monument,race_tag_world_tour,race_tag_big7,race_tag_grandtour,race_tag_cobbled_classic,
                             race_tag_ardennes,race_tag_cobbles_openingweekend,race_tag_aussie_kiwi_wt,race_tag_middle_east,race_tag_world_champs,
                             race_tag_euro_champs,race_tag_mallorca4,sep = " ")) |>
    select(-c(race_tag_monument,race_tag_world_tour,race_tag_big7,race_tag_grandtour,race_tag_cobbled_classic,
              race_tag_ardennes,race_tag_cobbles_openingweekend,race_tag_aussie_kiwi_wt,race_tag_middle_east,race_tag_world_champs,
              race_tag_euro_champs,race_tag_mallorca4)) |>
    mutate(first_cycling_race_id = as.double(first_cycling_race_id))
}
