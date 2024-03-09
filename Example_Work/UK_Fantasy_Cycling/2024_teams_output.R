
library(tidyverse)
library(gt)
library(gtExtras)

##### SETTING UP BASE CSVs and DFs #####

{
base_csv <- read.csv('/Users/zacrogers/Downloads/uk_fantasy_cycling - team_list.csv') |>
  filter(team_name != 'Russells Renners') |>
  unique()

rider_details <- read.csv('/Users/zacrogers/Downloads/uk_fantasy_cycling - rider details-3.csv')

riders_vertical_rider1 <- base_csv |>
  select(team_name,rider = rider1)
riders_vertical_rider2 <- base_csv |>
  select(team_name,rider = rider2)
riders_vertical_rider3 <- base_csv |>
  select(team_name,rider = rider3)
riders_vertical_rider4 <- base_csv |>
  select(team_name,rider = rider4)
riders_vertical_rider5 <- base_csv |>
  select(team_name,rider = rider5)
riders_vertical_rider6 <- base_csv |>
  select(team_name,rider = rider6)

teams <- rbind(riders_vertical_rider1,riders_vertical_rider2,riders_vertical_rider3,riders_vertical_rider4,riders_vertical_rider5,riders_vertical_rider6) |>
  left_join(rider_details, by = 'rider') |>
  group_by(team_name) |>
  mutate(team_total_spend = sum(price)) |>
  ungroup() |>
  filter(team_total_spend <= 18) |>
  group_by(team_name) |>
  arrange(gender,-price) |>
  mutate(rider_selection_id = paste0('rider',row_number())) |>
  mutate(id = row_number()) |>
  mutate(max_rider_cost = max(price),min_rider_cost = min(price)) |>
  ungroup() |>
  mutate(cycling_chaos_team_identifer = case_when(team_name == 'CyclingChaos' ~ 'pink',
                                                  .default = 'black'))

}

##### Gender Spend Comparison #####

gender_spend_count <- teams |>
  group_by(team_name,gender,team_total_spend,cycling_chaos_team_identifer) |>
  summarise(total_gender_spend = sum(price)) |>
  ungroup()

gender_spend_count_men <- gender_spend_count |>
  filter(gender == "Men") |>
  rename(total_men_spend = total_gender_spend) |>
  select(-gender)

gender_spend_count_women <- gender_spend_count |>
  filter(gender == "Women") |>
  rename(total_women_spend = total_gender_spend) |>
  select(-gender)

gender_spend_comp <- gender_spend_count_men |>
  left_join(gender_spend_count_women, by = c("team_name","team_total_spend","cycling_chaos_team_identifer")) |>
  mutate(gender_split = paste0(total_men_spend,'-',total_women_spend)) |>
  mutate(net_gender_split = total_men_spend - total_women_spend)

gender_spend_comp_filters <- gender_spend_comp |>
  #filter(net_gender_split < 3, net_gender_split > -3)
  #group_by(gender_split) |>
  summarise(net_gender_split_total = sum(net_gender_split))
#select(-c(total_men_spend,total_women_spend)) 

ggplot(gender_spend_comp, aes(net_gender_split,fill = cycling_chaos_team_identifer)) +
  geom_vline(aes(xintercept = +4),color = "#000000", size = 1, linetype = "dashed") +
  geom_vline(aes(xintercept = -2),color = "#000000", size = 1, linetype = "dashed") +
  xlim(-12,12) +
  scale_y_continuous() +
  scale_fill_manual(values = c('pink' = "pink",'black'="grey")) +
  geom_histogram(binwidth = 1, center = TRUE) +
  theme_minimal() +
  theme(legend.position = 'none') +
  labs(x = "Stars Gender Split",
       y = "Frequency",
       title = "Stars Gender Split",
       caption = "By CyclingChaos.co.uk | Data from UK Fantasy Cycling")

##### Looking at team leverage and meta plays #####

rider_count <- teams |>
  group_by(rider,team,gender,price) |>
  summarise(count = n()) |>
  ungroup() |>
  arrange(-count,price) |>
  mutate(rank = row_number()) |>
  group_by(gender) |>
  mutate(gender_rank = row_number()) |>
  ungroup() |>
  mutate(selection_percent = count/55)

teams_leverage <- teams |>
  left_join(rider_count, by = c("rider","team","price","gender"))

teams_leverage_score <- teams_leverage |>
  group_by(team_name) |>
  summarise(leverage_score = sum(count)) |>
  ungroup() |>
  mutate(chaos = case_when(team_name == "CyclingChaos" ~ "pink",
                           .default = "black"))

ggplot(teams_leverage_score, aes(leverage_score, fill = chaos)) +
  geom_histogram(binwidth = 1, center = TRUE) +
  scale_fill_manual(values = c('pink' = "pink",'black'="grey")) +
  theme_minimal() +
  xlim(0,50) +
  theme(legend.position = 'none') +
  labs(x = "Team's Leverage Score",
       y = "Frequency",
       title = "Leverage Analysis",
       caption = "By CyclingChaos.co.uk | Data from UK Fantasy Cycling")

##### GT Table showing teams. Has option to look at leverage scores or gender strategies #####

teams_pivot <- teams |>
  mutate(rider_price = paste0(rider,' (',team,')',' - ',price)) |>
  select(team_name,team_total_spend,rider_selection_id,rider_price) |>
  pivot_wider(names_from = rider_selection_id,
              values_from = rider_price) |>
  left_join(gender_spend_comp, by = c("team_name","team_total_spend")) |> 
  mutate(net_gender_split_from0 = case_when(net_gender_split < 0 ~ net_gender_split*-1,
                                            .default = net_gender_split)) |>
  arrange(-net_gender_split_from0,net_gender_split,-team_total_spend) |>
  mutate(rank_gender_split = row_number()) |>
  select(-c(cycling_chaos_team_identifer,total_men_spend,total_women_spend,net_gender_split,net_gender_split_from0)) |>
  left_join(teams_leverage_score, by = c("team_name")) |>
  select(-c(chaos)) |>
  arrange(leverage_score) |>
  mutate(leverage_max_rank = row_number()) |>
  arrange(-leverage_score) |>
  mutate(leverage_min_rank = row_number()) |>
  #select(team_name,team_total_spend,net_gender_split,rider_price,gender_split) |>
  #filter(team_total_spend < 18) |>
  arrange(leverage_max_rank) |>
  gt() |>
  cols_align(align = c("center")) |>
  cols_move(gender_split,team_total_spend) |>
  cols_move(leverage_score,team_total_spend) |>
  #cols_move_to_start(rank_gender_split) |>
  cols_move_to_start(leverage_max_rank) |>
  cols_label(
    leverage_max_rank = "Rank",
    team_name = "Team Name",
    gender_split = "Gender Split",
    leverage_score = "Leverage Score",
    team_total_spend = "Budget",
    rider1 = "Rider 1",
    rider2 = "Rider 2",
    rider3 = "Rider 3",
    rider4 = "Rider 4",
    rider5 = "Rider 5",
    rider6 = "Rider 6",) |>
  cols_hide(c(gender_split,
              rank_gender_split,
              #leverage_max_rank,
              leverage_min_rank
  )) |>
  tab_header(title = md('**Most Leverage Team Scores**'),
             subtitle = md('UK Fantasy Cycling Teams | Analysis by CyclingChaos.co.uk')) |>
  tab_style(
    style = list(
      cell_borders(
        sides = "left",
        color = "black",
        weight = px(3)
      )
    ),
    locations = list(
      cells_body(
        columns = c(team_name,rider1,rider4))))|>
  tab_footnote(
    footnote = "CyclingChaos.co.uk | Data from UK Fantasy Cycling"
  ) |>
  print()

##### Looking at most popular rider (meta and leverage plays) #####

gt(rider_count) |>
  cols_align(align = c("center")) |>
  cols_label(
    rider = "Rider",
    team = "Team",
    gender = "Gender",
    price = "Price",
    count = "Selections",
    selection_percent = "Selection %",
    rank = "Rank",
    gender_rank = "Rank - Gender"
  ) |>
  cols_move_to_start(gender_rank) |>
  cols_move_to_start(rank) |>
  fmt_percent(columns = c(selection_percent)) |>
  # add cols format to selection %
  tab_header(title = md('**Rider Selection Table**'),
             subtitle = md('UK Fantasy Cycling Teams | Analysis by CyclingChaos.co.uk')) |>
  tab_style(
    style = list(
      cell_borders(
        sides = "right",
        color = "black",
        weight = px(3)
      )
    ),
    locations = list(
      cells_body(
        columns = c(gender_rank,price))))|>
  tab_footnote(
    footnote = "CyclingChaos.co.uk | Data from UK Fantasy Cycling"
  ) |>
  print()

team_count <- teams |>
  #group_by(team,gender) |>
  group_by(team_name,team,gender) |>
  summarise(count = n()) |>
  ungroup() |>
  arrange(gender,-count) |>
  group_by(team,gender,count) |>
  summarise(team_count_count = n()) |>
  ungroup() |>
  arrange(-count,-team_count_count) |>
  mutate(rank = row_number()) |>
  group_by(gender) |>
  mutate(gender_rank = row_number()) |>
  ungroup() |>
  mutate(selection_percent = team_count_count/55) |>
  gt() |>
  cols_align(align = c("center")) |>
  cols_label(
    team = "Team",
    gender = "Gender",
    count = "Riders in Team",
    team_count_count = "Selections",
    selection_percent = "Selection %",
    rank = "Rank",
    gender_rank = "Rank - Gender"
  ) |>
  cols_move_to_start(gender_rank) |>
  cols_move_to_start(rank) |>
  fmt_percent(columns = c(selection_percent)) |>
  # add cols format to selection %
  tab_header(title = md('**Team Selection Table**'),
             subtitle = md('UK Fantasy Cycling Teams | Analysis by CyclingChaos.co.uk')) |>
  tab_style(
    style = list(
      cell_borders(
        sides = "right",
        color = "black",
        weight = px(3)
      )
    ),
    locations = list(
      cells_body(
        columns = c(gender_rank,team))))|>
  tab_footnote(
    footnote = "CyclingChaos.co.uk | Data from UK Fantasy Cycling"
  ) |>
  print()
