import os
import time
import sqlite3
import nltk
import datetime
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
twit_name = os.getenv('TWIT_NAME')
twit_pass = os.getenv('TWIT_PASS')
twit_user = os.getenv('TWIT_USER')

# Set up Firefox options for headless browsing
firefox_options = Options()
firefox_options.add_argument("--headless")  # Comment this line if you want to see the browser GUI

# download sentiment analysis dataset
# only have to do this once and can remove after
nltk.download('vader_lexicon')
nltk.download('punkt')


def open_twitter():
    print("Attempting to open twitter via headless browser")
    driver = webdriver.Firefox(service=s, options=firefox_options)
    # comment out the driver above and uncomment the driver below to use a browser with GUI
    # driver = webdriver.Firefox(service=s)
    # extra step variable for bot check
    botCheck = 'There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you.'
    # open twitter
    driver.get('https://twitter.com/login')
    time.sleep(5)  # Wait for the page to load
    # Click on the "Use phone / email / username" link
    username_field = driver.find_element(By.XPATH,
                                         '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_field.click()
    # Enter your username
    username_field.send_keys(twit_name)
    # Click on the "Log in" button
    login_button = driver.find_element(By.XPATH,
                                       '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    login_button.click()
    print("Successfully entered username")
    time.sleep(5)  # Wait for the page to load


    # twitter notices unusual login activity. This is a extra middle step login using your handle. Using try incase it doesn't notice unusual activity
    try:
        # Find the element using XPath
        element = driver.find_element(By.XPATH,
                                      '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/span/span')
        # Get the text from the element
        text = element.text
        # Print the captured string
        print("Captured String:", text)
        if text == botCheck:
            bot_field = driver.find_element(By.XPATH,
                                            '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            bot_field.send_keys(twit_user)
            bot_field_button = driver.find_element(By.XPATH,
                                                   '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span')
            bot_field_button.click()

    # no activity check login using these xpaths
    except Exception as e:
        print("An error occurred:", str(e))
        print("no check")
        password_field = driver.find_element(By.CSS_SELECTOR, '.r-homxoj')
        password_field.send_keys(twit_pass)
        password_button = driver.find_element(By.XPATH,
                                              '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span')
        password_button.click()
        print("successfuly entered password. open_twitter() is complete")
        return driver

    # 3rd step input password. Different xpath unusual activity vs not
    password_field2 = driver.find_element(By.XPATH,
                                          '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_field2.send_keys(twit_pass)
    password_button2 = driver.find_element(By.XPATH,
                                           '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    password_button2.click()
    print("successfuly entered password. open_twitter() is complete")
    # chaning zoom level will allow us to inspect more elements
    zoom_level = 0.5  # 50% zoom level
    # Execute JavaScript to zoom out the browser
    driver.execute_script(f"document.body.style.zoom = '{zoom_level}'")
    return driver


def search_twitter(driver, search_query):
    # click on search
    search_field = driver.find_element(By.XPATH,
                                       '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    # enter search query
    search_field.send_keys(search_query)
    search_field.send_keys(Keys.RETURN)
    # Wait for the page to load (you may need to adjust the wait time)
    time.sleep(5)
    # # Click on the user profile link. Finds the path via handle
    # user_profile_link = driver.find_element(By.XPATH, "//span[contains(text(), '" + search_query + "')]")
    # user_profile_link.click()
    # driver.implicitly_wait(5)


# down
def scroll(driver):
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_DOWN)


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")


def scrub_tweet(search_query, num_scrolls):
    # create driver, login to twitter
    driver = open_twitter()
    # Wait for the page to load
    driver.implicitly_wait(5)
    # use search bar
    search_twitter(driver, search_query)
    # Wait for the page to load
    driver.implicitly_wait(5)
    # Find and capture initial tweets
    tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
    captured_tweets = []
    for tweet_element in tweet_elements:
        try:
            tweet_text_element = tweet_element.find_element(By.XPATH, ".//div[@lang='en']")
            tweet_text = tweet_text_element.text
            captured_tweets.append(tweet_text)
        except NoSuchElementException:
            pass

    # Scroll and capture more tweets
    for _ in range(num_scrolls):
        # Scroll to the bottom of the page
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(5)  # Wait for the page to load after scrolling

        # Wait for the newly loaded tweets to appear
        driver.implicitly_wait(5)

        # Find and capture newly loaded tweets
        tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
        for tweet_element in tweet_elements:
            try:
                tweet_text_element = tweet_element.find_element(By.XPATH, ".//div[@lang='en']")
                tweet_text = tweet_text_element.text
                if tweet_text not in captured_tweets:
                    captured_tweets.append(tweet_text)
            except NoSuchElementException:
                pass
    print(captured_tweets)
    return captured_tweets


def tweet_exists(cursor, tweet):
    # Check if the tweet already exists in the data_table
    cursor.execute("SELECT COUNT(*) FROM data_table WHERE string_data = ?", (tweet,))
    count = cursor.fetchone()[0]
    return count > 0


def store_sentiment(tweets):
    print("attempting sentiment storage")
    # establish a connection to database
    conn = sqlite3.connect('budlight.db') #my database was in root directory
    # create a cursor object to interact with the database by executing SQL queries and fetches
    c = conn.cursor()
    # create an instance of the SentimentIntensityAnalyster class from NLTK library
    sid = SentimentIntensityAnalyzer()
    date_without_time = datetime.today().strftime('%Y-%m-%d')
    # Process each tweet and store in the database
    for tweet in tweets:
        if not tweet_exists(c,tweet): # let's make sure we aren't trying to store duplicates
            # Perform sentiment analysis
            sentiment_score = sid.polarity_scores(tweet)['compound']
            # Store the tweet, sentiment score and date in the data table
            c.execute("INSERT INTO data_table (string_data, sentiment_score, date_column) VALUES (?, ?, ?)",
                    (tweet, sentiment_score, date_without_time))
        else:
            print(f"Skipping tweet: '{tweet}' - Already exists in the database.")
    # Commit the changes to the database
    conn.commit()
    # Close the cursor and connection
    c.close()
    conn.close()


# In order to create our driver lets first create a service object
s = Service(GeckoDriverManager().install())
# call scrub_tweet to capture tweets in an array and pass it as a parameter to store_sentiment
# calculate the sentiment for each tweet, capture the date, and store the three in sqlite database
store_sentiment(scrub_tweet('#budlight', 5))

# the following just prints the contents of your database for testing
conn = sqlite3.connect('budlight.db')
c = conn.cursor()
c.execute("SELECT id, string_data, sentiment_score, date_column FROM data_table")
rows = c.fetchall()
# Print the data to the console
if len(rows) == 0:
        print("The data_table is empty.")
for row in rows:
    id_, string_data, sentiment_score, date_column = row
    print(f"ID: {id_}, String Data: {string_data}, Sentiment Score: {sentiment_score}, Date: {date_column}")

# Close the cursor and connection
c.close()
conn.close()
