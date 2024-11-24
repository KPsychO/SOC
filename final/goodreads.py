import requests
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
import os
from pathlib import Path


_PERIOD = 5
_CALLS = 2

_BASE_URL = "https://www.goodreads.com/"
_BASE_URL_YEARLY_AWARDS = _BASE_URL + "choiceawards/best-books-"
_YA_START_YEAR = 2011
# _BASE_URL_USER = _BASE_URL + "/user/"
# _ITEMS_PER_PAGE = 25


@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def make_request(url):  # makes a request using the session configured previously
    res = requests.get(url)
    html = BeautifulSoup(res.text, "html.parser")
    # [TODO]: Save html to cache file
    if create_cache(html):
        return True
    else:
        return False

def create_cache(html_gr):
    dir_cache = "cache/"
    Path("./" + dir_cache).mkdir(parents=True, exist_ok=True)
    cache_file = dir_cache + "/goodreads.html"
    file = open(cache_file, "w+")
    file.write(str(html_gr))
    return html_gr


def get_yearly_awards():
    print("goodreads::get_yearly_awards")


def process_goodreads():
    print("goodreads::process_goodreads")
    if make_request(_BASE_URL_YEARLY_AWARDS + "2012"):
        print("ok")
