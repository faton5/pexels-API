import requests
import json
import time

# Function to load already downloaded items
def load_downloaded_items():
    try:
        with open('downloaded_items.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save downloaded items
def save_downloaded_items(downloaded_items):
    with open('downloaded_items.json', 'w') as f:
        json.dump(downloaded_items, f)

# Function to download an item
def download_item(item_url, item_id, item_type, download_path):
    item_response = requests.get(item_url)
    with open(f'{download_path}\\{item_id}.{item_type}', 'wb') as f:  # <-- Replace with your download path
        f.write(item_response.content)

# Function to handle the response from the API
def handle_response(response, download_option, downloaded_items, item_type, download_path):
    data = response.json()
    for item in data[item_type]:
        if item['id'] not in downloaded_items:
            item_file = item['src']['original']
            item_url = item_file

            if download_option.lower() == 'yes':
                download_item(item_url, item['id'], item_type, download_path)

            downloaded_items.append(item['id'])
            save_downloaded_items(downloaded_items)

# Ask the user for their API key
while True:
    api_key = input("Please enter your API key: ")

    # Your API key
    headers = {
        'Authorization': api_key
    }

    # Verify API key
    response = requests.get('https://api.pexels.com/v1/search', headers=headers)
    if response.status_code == 401:
        print("Invalid API key. Please check your API key and try again.")
    else:
        break

# Ask the user what they want to download
download_option = input("Do you want to download items? (yes/no): ")
item_type_option = input("What type of items do you want to search for? (photos/videos/both): ")
pages_option = int(input("How many pages do you want to search? (Enter a number): "))
download_path = input("Please enter your download path: ")

# Search for space
params = {
    'query': 'YOUR_QUERY',  # <-- Replace with your query
    'per_page': '15',
}

downloaded_items = load_downloaded_items()

request_count = 0
total_request_count = 0

while True:  # Infinite loop
    for page in range(1, pages_option + 1):  # Go through the specified number of pages
        if request_count >= 200:
            print("Reached the hourly limit of 200 requests. Waiting for one hour.")
            time.sleep(3600)  # Pause for one hour
            request_count = 0  # Reset the request count

        if total_request_count >= 200000:
            print("Reached the monthly limit of 200,000 requests. Stopping the script.")
            break

        params['page'] = page

        if item_type_option in ['photos', 'both']:
            response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)
            request_count += 1
            total_request_count += 1

            if response.status_code == 200:
                handle_response(response, download_option, downloaded_items, 'photos', download_path)

        if item_type_option in ['videos', 'both']:
            response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
            request_count += 1
            total_request_count += 1

            if response.status_code == 200:
                handle_response(response, download_option, downloaded_items, 'videos', download_path)