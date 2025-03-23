# Dataset Scrapping

In this part of the project, we scrapped games dataset from the website steam games website [https://store.steampowered.com/](https://store.steampowered.com/) using steam APIs.

The repository contains the following sections:

## 1. Games Dataset Scrapping

Here we scrapped the games dataset from the website using the following 2 steam APIs:

i. [Steam Games List API](https://api.steampowered.com/ISteamApps/GetAppList/v2/)

ii. [Steam Games Details API](https://store.steampowered.com/api/appdetails?appids=)


The combination of these 2 APIs helped us to get the games dataset from the website. The dataset contains the following columns:
- App ID
- name
- type
- description
- price
- release date
- platforms
- developers
- Genres
- Game Modes
- Features
- System Requirements(Minimum and Recommended)
- Age Ratings
- Links


## 2. Games Reviews Scrapping:

Here we scrapped the games reviews using Game ID(App ID) dataset from the website using the following steam API:

[Steam Reviews API](https://store.steampowered.com/appreviews/{review_appid})

The game reviews dataset contains the following columns:

- Recommendation ID
- Author Steam ID
- Playtime forever
- Playtime last two weeks
- Playtime at the time of review
- Last Played
- Review Text
- Timestamp Created
- Timestamp Updated
- Voted Up
- Voted Funny
- Weighted Vote Score
- Steam Purchase
- Received for Free
- Written during Early Access


After scrapping the dataset, we saved the dataset in the form of CSV files in the data folder.

