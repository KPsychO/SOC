import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import argparse
import json
from ratelimit import limits, sleep_and_retry


# Global vars
_PERIOD = 5
_CALLS = 2
_BASE_URL = "https://old.reddit.com"
_BASE_URL_USER = _BASE_URL + "/user/"

# Configure a requests session to implement retries in case of an invalid server response
ses = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
ses.mount("https://", HTTPAdapter(max_retries=retries))


@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def make_request(url):  # makes a request using the session configured previously
    res = ses.get(url)
    return BeautifulSoup(res.text, "html.parser")


def obtain_user_posts_comments(
    posts, comments, html, subreddit
):  # Proces a given html to scrap a user posts and comments in a given subredit
    siteTable = html.find("div", attrs={"id": "siteTable"})
    if siteTable != None:
        things = siteTable.findAll("div", attrs={"class": "thing"})

        for thing in things:
            if thing["data-subreddit"] == subreddit:
                if thing["data-type"] == "link":
                    posts.append(_BASE_URL + thing["data-permalink"])
                elif thing["data-type"] == "comment":
                    comments.append(_BASE_URL + thing["data-permalink"])


def obtain_user_karma(
    html,
):  # Extracts the total user karma (post+comments karma) from a given html

    side = html.find("div", attrs={"class": "side"})
    if side != None:
        post_karma = side.find("span", attrs={"class": "karma"}).text
        comment_karma = side.find("span", attrs={"class": "karma comment-karma"}).text
        karma = int(post_karma.replace(",", "")) + int(comment_karma.replace(",", ""))
        return karma
    else:
        print("[DEBUG]: User account is NSFW, therefore, can´t be scrapped")
        return -1


def process_user_data(
    user_data, users_list, subreddit
):  # Creates the URL for a user profile from a given username and scraps its karma, posts and comments in the subreddit
    for user in users_list:
        user_url = _BASE_URL_USER + user
        html = make_request(user_url)

        # Karma
        karma = obtain_user_karma(html)

        # Posts & Comments
        posts = []
        comments = []
        obtain_user_posts_comments(posts, comments, html, subreddit)
        user_data.append(
            {
                "username": user,
                "karma": karma,
                "posts": posts,
                "comments": comments,
            }
        )


def process_comment_data(comment_data, comments, post_url):
    for comment in comments:
        # Comment URL
        comment_url = _BASE_URL + comment["data-permalink"]

        # Text
        text = comment.find("div", attrs={"class": "usertext-body"}).text

        # Date
        date = comment.find("time")["title"]

        # Author
        if "data-author" in comment.attrs:
            author = comment["data-author"]
        else:
            author = "Deleted Account"

        comment_data.append(
            {
                "comment": comment_url,
                "text": text,
                "date": date,
                "post": post_url,
                "author": author,
            }
        )


def process_post_data(post_data, comment_data, posts_list):
    for post in posts_list:
        post_url = _BASE_URL + post
        html = make_request(post_url)
        siteTable = html.find("div", attrs={"id": "siteTable"})
        entry = siteTable.find("div", attrs={"class": "entry"})

        if entry != None:
            # Title
            title = entry.find("a", attrs={"class": "title"}).text

            # Date
            date = entry.find("time")["title"]

            # Description
            usertext = entry.find("div", attrs={"class": "usertext"})
            if usertext != None:
                desc = usertext.find("div", attrs={"class": "md"}).text
            else:
                desc = ""

            # Author
            author_class = entry.find("a", attrs={"class": "author"})
            if author_class != None:
                author = author_class.text
            else:
                author = "Deleted Account"

            post_data.append(
                {
                    "post": post_url,
                    "title": title,
                    "date": date,
                    "description": desc,
                    "author": author,
                }
            )

            # Comments
            commentarea = html.find("div", attrs={"class": "commentarea"})
            comments_sitetable = commentarea.find("div", attrs={"class": "sitetable"})
            things = comments_sitetable.findAll("div", attrs={"class": "thing"})

            process_comment_data(comment_data, things, post_url)


def save_file(file, data):  # Saves the given data in json format to the given file
    with open(file + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--type", help="Type of scrapping: ['', 'new', 'rising', 'top']"
)
parser.add_argument(
    "-s", "--subreddit", help="Subreddit to scrap: spain, europe, spicypillows..."
)
parser.add_argument(
    "-o",
    "--output",
    help="Choose the output file name, will have the following format: user_FILENAME.json",
)

args = parser.parse_args()

_type = args.type
_subreddit = args.subreddit
_output_file = args.output

print("Reddit Scrapper")
print(" Scrapping subreddit: " + _BASE_URL + "/r/" + _subreddit + "/" + _type + "/")
print(" Outputting data to: data_type" + _output_file + ".json")
print(
    "---------------------------------------------------------------------------------"
)

html = make_request(_BASE_URL + "/r/" + _subreddit + "/" + _type + "/")

siteTable = html.find("div", attrs={"id": "siteTable"})
things = siteTable.findAll("div", attrs={"class": "thing"})

users = []
posts = []
for thing in things:
    if "data-permalink" in thing.attrs:
        posts.append(thing["data-permalink"])
    else:
        print("[DEBUG]: tag (data-permalink) not found -> ???")

    if "data-author" in thing.attrs:
        users.append(thing["data-author"])
    else:
        print("[DEBUG]: tag (data-author) not found -> User account was deleted")

users = list(dict.fromkeys(users))
posts = list(dict.fromkeys(posts))

# print(" Obtaining user data")
# user_data = []
# process_user_data(user_data, users, _subreddit)
# print(" Saving data to: user_" + _output_file + ".json...")
# save_file("user_" + _output_file, user_data)

print(" Obtaining posts data")
post_data = []
comment_data = []
process_post_data(post_data, comment_data, posts)
print(" Saving posts to: post_" + _output_file + ".json...")
save_file("post_" + _output_file, post_data)
print(" Saving comments to: comment_" + _output_file + ".json...")
save_file("comment_" + _output_file, comment_data)
