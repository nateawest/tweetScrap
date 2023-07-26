# tweetScrap
Python based twitter bot that uses selenium library and headless browser to scrap tweets based on #hashtag, do sentiment analyssis using nltk library, and store tweet and sentiment into sqlite db 

Overview

This repository caontains a Python-based Twitter bot that leverages Selenium to automate twitter. The application can login to twitter, navigate a #hashtag or @handle search, scroll through a page, and capture tweets. Sentiment analysis of the tweets is done using NLTK library, and tweets with their corresponding sentiment scores are stored into a sqlite3 database in the same directory.

Installation

Clone this repository to your local machine using the following command: git clone https://github.com/nateawest/tweetScrap.git
Change into the project directory: cd tweetScrap
install requirements: pip install -r requirements.txt
Download the appropriate WebDriver for your browser and ensure it is added to your system's PATH. I used firefox because it has a headless browser if you want to use a different browser you'll need to make changes to the driver within main

Configuration
Before running the tweetScrap you'll need to create a .env file to store your twitter username, password and handle. You'll also need to create a sqlite3 database in your root directory or elsewhere and modify the path. I run this bot using windows task schedular.

Contributing

If you would like to contribute to this project, you can follow these steps:

    Fork the repository on GitHub.

    Create a new branch with a descriptive name for your feature or bug fix:

    git checkout -b my-new-feature

Make the necessary changes and commit your code.

Push your changes to your forked repository.

Submit a pull request, explaining the changes you have made and why they should be merged.
