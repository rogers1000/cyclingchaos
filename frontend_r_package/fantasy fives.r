library(tidyverse)

##### Fantasy Fives #####

### inputting roster

ff_rosters_input <- read.csv('ff_rosters_test_2_csv.csv') |>
  mutate(season = 2023) |>
  select(-c(X)) |>
  mutate(first_cycling_race_id = as.character(first_cycling_race_id)) |>
  mutate(rider1 = as.character(rider1),
         rider2 = as.character(rider2),
         rider3 = as.character(rider3),
         rider4 = as.character(rider4),
         rider5 = as.character(rider5),
         ) |>
  rename("ff_team_name" = "team_name")

fantasy_fives_scores_stages <- function(rosters_input_function,race_filter_function,stage_position_limit_function) {
  ### adding scores up
  
  fantasy_fives_rosters_rider1 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider1)
  fantasy_fives_rosters_rider2 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider2)
  fantasy_fives_rosters_rider3 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider3)
  fantasy_fives_rosters_rider4 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider4)
  fantasy_fives_rosters_rider5 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider5)
  
  fantasy_fives_rosters <- rbind(fantasy_fives_rosters_rider1,fantasy_fives_rosters_rider2
                                 ,fantasy_fives_rosters_rider3
                                 ,fantasy_fives_rosters_rider4,fantasy_fives_rosters_rider5
  )
  
  ff_rider_stage_score_df <- results_function() |>
    select(season,first_cycling_race_id,first_cycling_rider_id,stage,position) |>
    filter(first_cycling_race_id == 17) |>
    mutate(ff_rider_stage_score = case_when(as.double(position) > stage_position_limit_function ~ stage_position_limit_function,
                                            is.na(as.double(position)) ~ stage_position_limit_function,
                                            .default = as.double(position)))
  
  ff_team_score <- fantasy_fives_rosters |>
    left_join(ff_rider_stage_score_df, by = c("season","first_cycling_race_id","first_cycling_rider_id"),relationship = "many-to-many") |>
    mutate(stg_number = as.double(stage)) |>
    arrange(-season,first_cycling_race_id,stg_number,ff_team_name,ff_rider_stage_score) |>
    select(-stg_number) |>
    group_by(season,first_cycling_race_id,ff_team_name,stage) |>
    mutate(stage_rider1 = ff_rider_stage_score[1],stage_rider2 = ff_rider_stage_score[2]) |>
    ungroup() |>
    mutate(ff_team_stage_score = stage_rider1 + stage_rider2) |>
    select(-c(first_cycling_rider_id,position,ff_rider_stage_score)) |>
    unique()
}

fantasy_fives_scores_gc <- function(rosters_input_function,race_filter_function,stage_position_limit_function) {
  ### adding scores up
  
  fantasy_fives_rosters_rider1 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider1)
  fantasy_fives_rosters_rider2 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider2)
  fantasy_fives_rosters_rider3 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider3)
  fantasy_fives_rosters_rider4 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider4)
  fantasy_fives_rosters_rider5 <- ff_rosters_input |>
    select(season,first_cycling_race_id,ff_team_name,first_cycling_rider_id = rider5)
  
  fantasy_fives_rosters <- rbind(fantasy_fives_rosters_rider1,fantasy_fives_rosters_rider2
                                 ,fantasy_fives_rosters_rider3
                                 ,fantasy_fives_rosters_rider4,fantasy_fives_rosters_rider5
  )
  
  ff_rider_stage_score_df <- results_function() |>
    select(season,first_cycling_race_id,first_cycling_rider_id,stage,position) |>
    filter(first_cycling_race_id == 17) |>
    mutate(ff_rider_stage_score = case_when(as.double(position) > stage_position_limit_function ~ stage_position_limit_function,
                                            is.na(as.double(position)) ~ stage_position_limit_function,
                                            .default = as.double(position)))
  
  ff_team_score <- fantasy_fives_rosters |>
    left_join(ff_rider_stage_score_df, by = c("season","first_cycling_race_id","first_cycling_rider_id"),relationship = "many-to-many") |>
    mutate(stg_number = as.double(stage)) |>
    arrange(-season,first_cycling_race_id,stg_number,ff_team_name,ff_rider_stage_score) |>
    select(-stg_number) |>
    group_by(season,first_cycling_race_id,ff_team_name,stage) |>
    mutate(stage_rider1 = ff_rider_stage_score[1],stage_rider2 = ff_rider_stage_score[2]) |>
    ungroup() |>
    mutate(ff_team_stage_score = stage_rider1 + stage_rider2) |>
    select(-c(first_cycling_rider_id,position,ff_rider_stage_score)) |>
    unique() |>
    group_by(season,first_cycling_race_id,ff_team_name) |>
    summarise(ff_gc_score = sum(ff_team_stage_score)) |>
    arrange(ff_gc_score) |>
    mutate(rank = row_number()) |>
    relocate(rank,season)
  
}

test_fantasy_fives_scores_overall <- fantasy_fives_scores_gc("",17,50)
