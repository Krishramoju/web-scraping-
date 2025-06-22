import requests
from bs4 import BeautifulSoup
import csv

def scrape_github_trending():
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Send HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all repository articles
        repos = soup.find_all('article', class_='Box-row', limit=5)
        
        # Prepare data for CSV
        data = []
        for repo in repos:
            # Get repository name
            name_element = repo.find('h2', class_='h3')
            name = name_element.get_text(strip=True).replace('/', '').strip()
            
            # Get repository URL
            relative_url = name_element.find('a')['href']
            url = f"https://github.com{relative_url}"
            
            data.append([name, url])
        
        # Write to CSV file
        with open('github_trending.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['repository name', 'link'])
            writer.writerows(data)
            
        print("Successfully scraped and saved top 5 trending repositories to github_trending.csv")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_github_trending()
