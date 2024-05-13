#import libraries
import pandas as pd
import requests
import ssl
from bs4 import BeautifulSoup

# Header for metadata
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

# Function to get all the URLs to scrape from a search URL
def get_all_anchor_tags(url):
    page = requests.get(url, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, features="lxml")
    link_list = []
    for tag in soup.find_all('a'):
        link = tag.get("href")
        searchd = "/in/buy/projects/page/"
        if link and link.find(searchd) != -1:
            new_link = "https://housing.com" + link
            link_list.append(new_link)
    return link_list

# Function to scrape the URL
# Scrape the url
# Scrape the url
def extract_data(url):
    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:  # Check if the request was successful
            soup = BeautifulSoup(page.content, 'html.parser')
            print(soup)  # Print the entire content of the page for debugging
            
            result = {}
            
            # Extract flat type
            flat_type_tag = soup.find('h1', class_='css-10rvbm3')
            flat_type = flat_type_tag.text.strip() if flat_type_tag else "Flat type not mentioned"
            result['Flat type'] = flat_type
            
            # Extract other information
            sections = soup.find_all('section', class_='css-13dph6')
            for section in sections:
                keys = [div.text.strip() for div in section.find_all('div', class_='css-r74jsk')]
                values = [div.text.strip() for div in section.find_all('div', class_='css-3o6ku8')]
                for key, value in zip(keys, values):
                    result[key] = value
            
            # Extract tables if any
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['th', 'td'])
                    if len(cols) >= 2:
                        key = cols[0].text.strip()
                        value = cols[1].text.strip()
                        result[key] = value
            
            # Extract about information
            about_tag = soup.find('div', class_='about-text css-1d1e0rh')
            if about_tag:
                result['About'] = about_tag.text.strip()
            
            # Extract special highlights
            special_highlights_tag = soup.find('div', class_="css-1o20zr1")
            if special_highlights_tag:
                highlights = [highlight.text.strip() for highlight in special_highlights_tag.find_all('div', class_="highlight css-1byt3mr")]
                result['Special Highlights'] = ', '.join(highlights)
            
            df = pd.DataFrame(result, index=[0])
            return df
        else:
            print(f"Failed to retrieve data from {url}. Status code: {page.status_code}")
            return pd.DataFrame()  # Return an empty DataFrame if the request fails
    except Exception as e:
        print("Error occurred while extracting data from:", url, e)
        return pd.DataFrame()  # Return an empty DataFrame if extraction fails
# Return an empty DataFrame if extraction fails

# URL to scrape
url = "https://housing.com/rent/property-for-rent-in-pune?gclid=CjwKCAjwrvyxBhAbEiwAEg_KgtDZUkm8GKxQucaiLbqIy7dk4pDvUlECB_7PPQGhmHq7GgZxfvAWqhoCZ8IQAvD_BwE"

# Scrape the URL
try:
    df = extract_data(url)
    print("Data extracted successfully:")
    #print(df)
    #structured_df = pd.json_normalize(df.to_dict(orient='records'))
    #print("Structured DataFrame:")
    #print(structured_df)
except Exception as e:
    print("Error occurred while processing:", e)
