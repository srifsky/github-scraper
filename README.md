# GitHub Repository Scraper

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)

A Python-based GitHub repository scraper that uses the GitHub API to fetch repositories based on search queries and filters, with enhanced terminal visuals using `rich`.

## Features
- Fetch repositories by search query
- Filter results by language, stars, and forks
- Save results in CSV, JSON, SQLite, or Excel formats
- Enhanced terminal visuals with progress bars and tables

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/github-scraper.git
    cd github-scraper
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    Create a `.env` file in the project root and add your GitHub Personal Access Token.

## Usage
Run the script and follow the prompts:
    ```bash
    python github_scraper.py
    ``` 

## Examples

### Search for AI repositories:

- **Query**: ai  
- **Filter**: Language: Python  
- **Sort by**: stars  
- **Order**: desc  
- **Save format**: CSV  

#### Example Output:
```plaintext
Fetching pages: 100%|██████████| 3/3 [00:05<00:00,  1.20s/it]
Saved CSV to data/github_api_results.csv
```

### Visual Example:
![Terminal Demo](assets/demo.gif)

## Requirements
- Python 3.7 or higher

## Contributing
Feel free to submit issues or pull requests for new features or improvements.

## Future Enhancements
- Add support for fetching repository contributors and their stats.
- Include a web-based dashboard using Streamlit or Dash for interactive analysis.
- Expand filtering options (e.g., by creation date, issue count).

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International Public License. See the `LICENSE` file for details.
