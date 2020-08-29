from twitter_browser import TwitterBrowser
from util import Util
from selenium_util import SeleniumUtil
from tweet import Tweet
import time

class TwitterScraper:
    def __init__(self,start_date=None,end_date=None):
        self._start_date = Util.string_to_date(start_date)
        self._end_date = Util.string_to_date(end_date)

        self.open_twitter_browser()

    def set_twitter_login(self,username,password):
        self._username = username
        self._password = password

    def open_twitter_browser(self):
        self._twitter_browser = TwitterBrowser()
        self._twitter_browser.open_twitter()

    def close_twitter_browser(self):
        self._twitter_browser.close_twitter()

    def login_to_twitter(self):
        self._twitter_browser.login(username=self._username, password=self._password)

    def set_account_search(self, account):

        self._account_search = account

    def search_dates(self,from_date,to_date):
        self._twitter_browser.search(account=self._account_search,from_date=from_date,to_date=to_date)
        time.sleep(5)
        datequery = f"{Util.date_to_string(from_date)} to {Util.date_to_string(to_date)}"
        for link in self._twitter_browser.get_possible_links():
            try:
                Tweet(link=link,datequery=datequery).save()
            except:
                print(f"Duplicate link {link}")

    def get_date_range(self):
        date_difference = self._end_date - self._start_date
        date_pairs = []
        for i in range(date_difference.days):
            from_date_delta = i
            to_date_delta = i + 1
            date_pairs.append({'from_date': Util.get_next_date(self._start_date, from_date_delta), 'to_date': Util.get_next_date(self._start_date, to_date_delta)})
        return date_pairs

    def start_link_fetching(self):
        for date_pair in self.get_date_range():
            date_range = f"{Util.date_to_string(date_pair['from_date'])} to {Util.date_to_string(date_pair['to_date'])}"
            print(f"{date_range} STARTED")
            self.search_dates(date_pair['from_date'], date_pair['to_date'])
            print(f"{date_range} DONE")


    def get_twitter_browser(self):
        return self._twitter_browser

    def visit_tweet_link(self, tweet):
        self._twitter_browser.visit_link(tweet.link)
        time.sleep(2)
        tweet.datetime, tweet.text = self._twitter_browser.get_tweet_details()
        tweet.save()
