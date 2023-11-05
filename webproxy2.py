import requests
import cachetools

# Define the URL of the web page you want to fetch
url = 'http://192.168.135.246:15200/index.html'  # Replace with the URL of the web page you want to fetch

# Create an in-memory cache with cachetools
cache = cachetools.LRUCache(maxsize=128)  # You can adjust the cache size as needed

# Define a function to fetch the web page and cache the response
def fetch_and_cache(url):
    if url in cache:
        return cache[url]
    else:
        response = requests.get(url)
        if response.status_code == 200:
            cache[url] = response.text
            return response.text
        else:
            print(f"Failed to fetch the web page. Status code: {response.status_code}")
            return None

# Fetch the web page and cache the response
page_content = fetch_and_cache(url)

if page_content:
    # Print the cached page content
    print(page_content)
