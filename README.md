# Steam Game Review Analysis Project

This project focuses on scraping game details and user reviews from Steam, followed by cleaning and preparing the review data for analysis. The project is divided into three main parts:

## Part 1: Game Detail Scrapping

**Location:** `dataset_scrapping/app_info_scrapper/`

**Methodology:**

1.  **App ID Input:** The process starts with a list of Steam application IDs, typically stored in `app_ids_with_reviews.txt`.
2.  **API Fetching:** The script `app_info_filterer.py` iterates through the app IDs and uses the official Steam API (`https://store.steampowered.com/api/appdetails`) to request detailed information for each application in Turkish (`l=turkish`).
3.  **Filtering & Error Handling:**
    *   It checks the `success` flag in the API response. If `false`, the app ID is added to an `excluded_apps_list` (e.g., for games no longer available).
    *   It handles potential API errors like rate limits (HTTP 429) by pausing and retrying, and forbidden access (HTTP 403) by pausing for a longer duration. App IDs causing other request/decoding errors are added to an `error_apps_list`.
4.  **Data Extraction:** For successful responses, relevant game details (like Name, Type, Description, Price, Release Date, Platforms, Developers, Genres, Categories, System Requirements, etc.) are extracted from the JSON response.
5.  **Checkpointing:** To handle long processing times and potential interruptions, the script saves its progress periodically (every 2500 apps). The current dictionary of fetched game details (`apps_dict`), the list of excluded apps (`excluded_apps_list`), and the list of error apps (`error_apps_list`) are saved as pickle files (`.p`) in the `checkpoints/` directory. The script automatically resumes from the latest checkpoint upon restart.
6.  **Output Generation:** The extracted details for each valid game are appended to the `games.csv` file.

**Output Data:**

*   `dataset_scrapping/app_info_scrapper/games/games.csv`: A CSV file containing detailed information for the scraped games.
*   `dataset_scrapping/app_info_scrapper/checkpoints/`: Contains checkpoint files (`*.p`) storing the state of the scraper (`apps_dict`, `excluded_apps_list`, `error_apps_list`) for resuming interrupted sessions.
*   `dataset_scrapping/app_info_scrapper/app_ids_with_reviews.txt`: The input list of app IDs processed.
*   `dataset_scrapping/app_info_scrapper/excluded_apps_list-ckpt-fin.p`: (Pickle file) List of app IDs excluded during scraping (e.g., invalid, removed).
*   `dataset_scrapping/app_info_scrapper/error_apps_list-ckpt-fin.p`: (Pickle file) List of app IDs that caused errors during the API request or processing.

## Part 2: Reviews Scrapping

**Location:** `dataset_scrapping/app_reviews_scrapper/`

**Methodology:**

1.  **App ID Input:** This part likely uses a list of game app IDs (potentially filtered from the previous step, e.g., using `app_ids_filter.ipynb` or `filter_app_ids.ipynb`) stored in `app_ids.txt` or `app_ids_with_reviews.txt`.
2.  **Scraping Process:** The `review_scrapper.ipynb` notebook contains the code responsible for fetching user reviews for the specified app IDs. This typically involves interacting with Steam's review endpoints (API or web scraping).
3.  **Handling Pagination:** The scraper needs to handle pagination to retrieve a large number of reviews for popular games.
4.  **Data Storage:** Scraped reviews are collected and stored.

**Output Data:**

*   `dataset_scrapping/app_reviews_scrapper/reviews/reviews.csv`: A CSV file containing the raw user reviews scraped from Steam, likely including review text, user information, playtime, timestamps, and ratings.

## Part 3: Cleaning and Labeling Reviews

**Location:** `data_preparation/`

**Methodology:**

1.  **Input Data:** The process uses the raw `reviews.csv` file generated in Part 2.
2.  **Cleaning:** The `cleaning.ipynb` notebook performs text preprocessing and cleaning tasks on the review text. This may include:
    *   Lowercasing text.
    *   Removing punctuation, special characters, and URLs.
    *   Handling emojis or non-standard characters.
    *   Potentially using Turkish-specific NLP techniques (indicated by the use of `zemberek` in output filenames and potentially libraries listed in `requirements.txt`) for tasks like stemming or lemmatization, possibly using rules defined in `constants/suffixes.json`.
3.  **Labeling (Potential):** Based on the files in `constants/` (`aspects_keywords.json`, `sentiment_keywords.json`), this step might involve:
    *   **Sentiment Analysis:** Assigning a sentiment label (e.g., positive, negative, neutral) to each review.
    *   **Aspect Extraction:** Identifying specific game aspects mentioned in the reviews (e.g., graphics, gameplay, story). This could use keyword matching based on the predefined lists.
4.  **Data Structuring:** The cleaned and potentially labeled data is structured and saved.

**Output Data:**

*   `dataset/cleaned_reviews*.xlsx`: Excel files containing the processed reviews. The different filenames (`cleaned_reviews.xlsx`, `cleaned_reviews_zemberek.xlsx`, etc.) likely represent different stages or versions of the cleaning and labeling process.
*   `data_preparation/constants/`: JSON files containing keywords or rules used during the labeling phase.