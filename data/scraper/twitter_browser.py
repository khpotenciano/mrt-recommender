import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime
import re
import urllib.parse
from util import Util
from selenium_util import SeleniumUtil
from twitter_util import TwitterUtil

class TwitterBrowser:
    TWITTER_URL = "https://www.twitter.com"
    def __init__(self, *, headless=False):
        self._chrome_options = Options()
        if headless:
            self._chrome_options.add_argument("--headless")

    def open_twitter(self):
        self._driver = webdriver.Chrome(options=self._chrome_options)
        self._driver.get(url = TwitterBrowser.TWITTER_URL)

    def close_twitter(self):
        self._driver.quit()

    def login(self, *, username, password):
        login_button = self._driver.find_element_by_xpath("//a[@data-testid='loginButton']")
        login_button.click()
        time.sleep(1)
        username_obj = self._driver.find_element_by_name("session[username_or_email]")
        password_obj = self._driver.find_element_by_name("session[password]")
        username_obj.send_keys(username)
        password_obj.send_keys(password)
        login_button = self._driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']")
        login_button.click()
        time.sleep(1)
    def get_query_term(self, account,from_date,to_date,text):
        query_term = ""
        if Util.valid_value(account,str) and Util.valid_value(from_date, datetime.datetime) and Util.valid_value(text, str) and Util.valid_value(to_date, datetime.datetime):
            if text != None:
                query_term += f"{text} "
            if account != None:
                query_term += f"(from:{account}) "
            if to_date != None:
                query_term += f" until:{to_date.strftime('%Y-%m-%d')} "
            if from_date != None:
                query_term += f" since:{from_date.strftime('%Y-%m-%d')}"
            query_term = f"q={urllib.parse.quote(query_term)}&src=typed_query"
            return query_term

    def search(self, *, account="",from_date=None,to_date=None,text=None):
        query_term = self.get_query_term(account,from_date,to_date,text)
        self._driver.get(f"{TwitterBrowser.TWITTER_URL}/search?{query_term}")

    def get_possible_links(self):
        articles = []
        prev_len = 0
        while True:
            new_articles = self._driver.find_elements_by_xpath("//article/*//a[@dir='auto']")
            if prev_len == len(new_articles):
                break;
            else:
                articles += SeleniumUtil.get_links(new_articles)
                prev_len = len(new_articles)
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        return articles

    def visit_link(self, link):
        self._driver.get(link)
        time.sleep(4)

    def get_selenium_driver(self):
        return self._driver

    def get_tweet_details(self):
        article = self._driver.find_element_by_tag_name("article")
        captions = []
        for caption in article.find_elements_by_tag_name("span"):
            stripped_caption = caption.text.strip()
            if stripped_caption:
                captions.append(stripped_caption)
        datetime_index = TwitterUtil.get_date_index(captions)
        datetime = TwitterUtil.twitter_date_string_to_datetime(captions[datetime_index])
        caption = ' '.join(captions[0:(datetime_index-1)])

        return datetime, caption
