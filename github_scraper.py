import os
import requests
import pandas as pd
import sqlite3
import json
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.progress import track
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up rich console
console = Console()

# GitHub API Base URL
BASE_URL = "https://api.github.com/search/repositories"

# Function to fetch repositories using GitHub API
def fetch_repositories(query, max_pages=1, filters=None):
    """
    Fetch repositories using GitHub API.
    
    :param query: Search query string
    :param max_pages: Maximum number of pages to scrape
    :param filters: Optional filters for the search
    :return: List of repository details
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        console.print("[bold red]Error: GITHUB_TOKEN not found in .env file.[/bold red]")
        return []
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repos = []
    for page in track(range(1, max_pages + 1), description="Fetching pages..."):
        params = {"q": query, "per_page": 30, "page": page}
        if filters:
            params.update(filters)
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            console.print(f"[bold red]Failed to fetch data: {response.status_code}, {response.text}[/bold red]")
            break
        
        data = response.json()
        for item in data.get("items", []):
            repos.append({
                "Name": item["name"],
                "Full Name": item["full_name"],
                "Description": item["description"],
                "Stars": item["stargazers_count"],
                "Forks": item["forks_count"],
                "Language": item["language"],
                "Topics": ", ".join(item.get("topics", [])),
                "URL": item["html_url"]
            })
    
    return repos

# Display results in a table
def display_summary(repositories):
    """
    Display a summary of the scraped data in a table.
    """
    if not repositories:
        console.print("[bold yellow]No repositories found.[/bold yellow]")
        return
    
    table = Table(title="GitHub Repository Summary")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Stars", style="green")
    table.add_column("Language", style="magenta")
    table.add_column("URL", style="blue")
    
    for repo in repositories[:5]:  # Show only the top 5 repositories
        table.add_row(repo["Name"], str(repo["Stars"]), repo["Language"], repo["URL"])
    
    console.print(table)

# Save results in selected formats
def save_results(repos, filename="github_api_results"):
    """
    Save repository data in user-selected formats.
    """
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    console.print("Choose the format to save the results:")
    console.print("[1] CSV\n[2] JSON\n[3] SQLite Database\n[4] Excel")
    format_choice = input("Enter your choice (1/2/3/4): ").strip()
    
    if format_choice == "1":
        csv_path = os.path.join(output_dir, f"{filename}.csv")
        pd.DataFrame(repos).to_csv(csv_path, index=False)
        console.print(f"[green]Saved CSV to {csv_path}[/green]")
    
    elif format_choice == "2":
        json_path = os.path.join(output_dir, f"{filename}.json")
        with open(json_path, "w") as json_file:
            json.dump(repos, json_file, indent=4)
        console.print(f"[green]Saved JSON to {json_path}[/green]")
    
    elif format_choice == "3":
        sqlite_path = os.path.join(output_dir, f"{filename}.db")
        conn = sqlite3.connect(sqlite_path)
        pd.DataFrame(repos).to_sql("repositories", conn, if_exists="replace", index=False)
        conn.close()
        console.print(f"[green]Saved SQLite database to {sqlite_path}[/green]")
    
    elif format_choice == "4":
        excel_path = os.path.join(output_dir, f"{filename}.xlsx")
        pd.DataFrame(repos).to_excel(excel_path, index=False, engine="openpyxl")
        console.print(f"[green]Saved Excel file to {excel_path}[/green]")
    else:
        console.print("[bold red]Invalid choice. No file saved.[/bold red]")

# Main script
if __name__ == "__main__":
    console.print("[bold blue]GitHub Repository Fetcher[/bold blue]")
    
    # Prompt for search query
    search_query = input("Enter your search query: ").strip()
    
    # Prompt for filters
    filter_choice = input("Do you want to apply filters? (yes/no): ").strip().lower()
    filters = {}
    
    if filter_choice == "yes":
        language = input("Filter by programming language (leave blank for none): ").strip()
        if language:
            filters["q"] = f"language:{language}"
        
        sort_by = input("Sort by (stars/forks): ").strip().lower()
        if sort_by in ["stars", "forks"]:
            filters["sort"] = sort_by
        
        order = input("Order (asc/desc): ").strip().lower()
        if order in ["asc", "desc"]:
            filters["order"] = order
    
    max_pages = int(input("How many pages to scrape? (e.g., 1, 2, 5): ").strip())
    
    repositories = fetch_repositories(search_query, max_pages=max_pages, filters=filters)
    
    display_summary(repositories)
    
    if repositories:
        save_results(repositories)
    else:
        console.print("[bold yellow]No repositories found or an error occurred.[/bold yellow]")
