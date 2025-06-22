import requests
from bs4 import BeautifulSoup
import csv

URL = "https://github.com/trending"

def scrape_trending_repos():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for article in soup.select('article.Box-row')[:5]:  # Get top 5
        link = article.select_one('h2 a')
        repo_name = link.get_text(strip=True).replace(' ', '')
        repo_url = f"https://github.com{link['href']}"
        repos.append({'name': repo_name, 'url': repo_url})
    
    return repos

def save_to_csv(repos, filename='trending_repos.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['repository name', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for repo in repos:
            writer.writerow({
                'repository name': repo['name'],
                'link': repo['url']
            })

if __name__ == "__main__":
    trending_repos = scrape_trending_repos()
    save_to_csv(trending_repos)
    print("Successfully saved top 5 trending repositories to trending_repos.csv")
