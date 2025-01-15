# DARAZ FLASH SALE SCRAPER: UNVEILING EXCLUSIVE DEALS

## Overview
This project is designed to scrape data from Daraz's flash sales and uncover exclusive deals and discounts. By leveraging web scraping tools, it enables insightful analysis of the deals offered during flash sales.

## Features
- **Data Acquisition**: Efficiently scrape product details, discounts, and other information from Daraz using Playwright and BeautifulSoup.
- **Insightful Analysis**: Extract and analyze exclusive deals to gain meaningful insights into flash sale trends and offerings.

## Tech Stack
- **Programming Language**: Python
- **Libraries Used**:
  - [Playwright](https://playwright.dev/python/): For automated browser interactions and navigation.
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): For parsing HTML and extracting relevant data.
  - [Pandas](https://pandas.pydata.org/): For data manipulation and storage.
  - [TQDM](https://tqdm.github.io/): For progress tracking.

## How It Works
1. **Setup and Navigation**: Navigate to Daraz's flash sale page using Playwright.
2. **Data Scraping**: Extract product details, including names, links, discounted prices, original prices, discounts, and ratings.
3. **Storage**: Save the scraped data into a structured format (CSV) for further analysis.

## Output
The script outputs a CSV file named `product_data_<date>.csv`, containing details such as:
- Product Name
- Discounted Price
- Original Price
- Discount Percentage
- Number of Products Sold
- Ratings and Reviews

## Getting Started
### Prerequisites
- Python 3.7+
- Install the required libraries:
  ```bash
  pip install playwright beautifulsoup4 pandas tqdm
  ```
- Install Playwright browsers:
  ```bash
  playwright install
  ```

## Future Work
- Implement functionality to scrape flash sale data for a specific period to track trends over time.
- Use the collected data for comprehensive analysis, including:
  - Identifying top-performing products.
  - Analyzing discount patterns.
  - Generating visual reports for business insights.


