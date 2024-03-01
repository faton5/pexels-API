# Pexels API Script

This Python script uses the Pexels API to search for and download photos and videos.

## How it Works

1. The script starts by asking the user to enter their API key for Pexels. If the API key is not valid, the script prompts the user to enter a new key until a valid key is provided.

2. Next, the script asks the user if they want to download items. If the user answers "yes", the script will download the items found in the search.

3. The script then asks the user what type of items they want to search for (photos, videos, or both) and how many pages to search.

4. The script then performs the search using the Pexels API. For each page of results, the script checks if each item has already been downloaded by consulting a `downloaded_items.json` file. If an item has not already been downloaded and the user has chosen to download items, the script downloads the item.

5. Items are downloaded to the directory specified by the user when prompted to enter their download path.

6. The script continues to perform searches and download items until it has gone through the number of pages specified by the user, or until it hits the Pexels API request limit (200 requests per hour, 200,000 requests per month).

## Installation

This script requires the `requests`, `json`, and `time` Python packages. These dependencies can be installed using pip:

```bash
pip install -r requirements.txt
