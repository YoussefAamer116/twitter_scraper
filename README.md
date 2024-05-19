# Twitter Scraper

This project scrapes tweets from specified Twitter accounts for stock symbols.

## Setup

### 1. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/YoussefAamer116/twitter_scraper.git
cd twitter_scraper
```

### 2. Create and Activate a Virtual Environment

Create and activate a virtual environment:

````bash
python -m venv venv
source venv/bin/activate

### 3. Install the Required Packages

Install the necessary packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
````

### 4. Create a `.env` File

Create a `.env` file in the project directory with the following content:

```plaintext
CHROMEDRIVER_PATH=path-to-your-chromedriver.exe
```

## Usage

Run the scraper:

```bash
python twitter_scrap.py
```

### Note

- Ensure that you have the correct path to `chromedriver.exe` in your `.env` file.
- This script runs indefinitely, scraping the specified Twitter accounts at the defined interval. Press `Ctrl+C` to stop the script.

## Output

The output will display the number of times each stock symbol was mentioned in the tweets for the specified time interval, in the format:

```
"$TSLA" was mentioned 10 times in the last 15 minutes.
```
