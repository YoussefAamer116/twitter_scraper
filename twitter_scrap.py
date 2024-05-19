from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# List of Twitter accounts to scrape
twitter_accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox",
]

# The ticker symbol pattern to search for
ticker_symbol = re.compile(r'\$[A-Z]{3,4}')
# Time interval in minutes for scraping
time_interval = 15

# Set up the Selenium WebDriver
options = Options()
options.headless = True  
# take the driver path from .env file
chromedriver_path = os.getenv('CHROMEDRIVER_PATH')

# Path to ChromeDriver on Windows
service = Service(chromedriver_path)  
driver = webdriver.Chrome(service=service, options=options)

def get_tweets(url, max_scrolls=10):
    """Get tweets from the Twitter account page."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

    tweets = set()
    scrolls = 0

    while scrolls < max_scrolls:
        # Extract tweets
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article div[lang]')
        for tweet in tweet_elements:
            tweets.add(tweet.text)
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for new tweets to load
        
        scrolls += 1
    
    return list(tweets)

def ticker_mentions_to_dict(tweets, ticker_symbol):
    """Return dictionary that counts the number of times each ticker symbol pattern is mentioned in the tweets."""
    symbol_counts = {}
    
    for tweet in tweets:
        # find all ticker symbols in tweet
        found_symbols = ticker_symbol.findall(tweet)
        
        if found_symbols:
            for symbol in found_symbols:
                if symbol in symbol_counts:
                    symbol_counts[symbol] += 1
                else:
                    symbol_counts[symbol] = 1

    return symbol_counts

def scrape_twitter_accounts(accounts, ticker_symbol, interval):
    """Scrape the Twitter accounts at specified intervals."""
    try:
        while True:
            # dictionary to hold aggregated counts of ticker symbols across all accounts
            aggregated_counts = {}
            # iterate on all accounts
            for account in accounts:
                # getting the text from each account's tweets
                tweets = get_tweets(account)
                # get times of symbol ticker dictionary 
                symbol_counts = ticker_mentions_to_dict(tweets, ticker_symbol)

                for symbol, count in symbol_counts.items():
                    if symbol in aggregated_counts:
                        aggregated_counts[symbol] += count
                    else:
                        aggregated_counts[symbol] = count
            
            for symbol, count in aggregated_counts.items():
                # print the aggregated counts of each ticker symbol
                print(f'"{symbol}" was mentioned {count} times in the last "{interval}" minutes. ')
            
            print(f"Waiting for {interval} minutes before the next scraping session...")
            
            time.sleep(interval * 60)
    
    except KeyboardInterrupt:
        print("Scraping interrupted by user.")
    
    finally:
        driver.quit()

# Run the scraping function
scrape_twitter_accounts(twitter_accounts, ticker_symbol, time_interval)
