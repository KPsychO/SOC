import requests
from bs4 import BeautifulSoup
import argparse
import json
from ratelimit import limits, sleep_and_retry


# Global vars
_PERIOD = 5
_CALLS = 2
_BASE_URL = "https://old.reddit.com"
_BASE_URL_USER = _BASE_URL + "/user/"
_ITEMS_PER_PAGE = 25


@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def make_request(url):  # makes a request using the session configured previously
    res = requests.get(url)
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
        return -1


def process_user_data(
    user_data, users_list, users_all, subreddit
):  # Creates the URL for a user profile from a given username and scraps its karma, posts and comments in the subreddit
    for user in users_list:
        if user not in users_all:
            users_all.append(user)
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
                    "comments": comments
                }
            )


def process_comment_data(comment_data, comments, post_url):
    for comment in comments:
        # Comment URL
        if "data-permalink" in comment.attrs:
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
                    "author": author
                }
            )


def process_post_data(post_data, comment_data, posts_list):
    for post in posts_list:
        post_url = _BASE_URL + post
        html = make_request(post_url)
        siteTable = html.find("div", attrs={"id": "siteTable"})

        if siteTable != None:
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
                        "author": author
                    }
                )

                # Comments
                commentarea = html.find("div", attrs={"class": "commentarea"})
                comments_sitetable = commentarea.find(
                    "div", attrs={"class": "sitetable"}
                )
                things = comments_sitetable.findAll("div", attrs={"class": "thing"})

                process_comment_data(comment_data, things, post_url)


def save_file(file, data):  # Saves the given data in json format to the given file
    with open(file + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

def process_page(user_data, post_data, comment_data, page_url, users_all):
    print(" Scrapping subreddit: " + page_url)
    print("---------------------------------------------------------------------------------")
    html = make_request(page_url)

    siteTable = html.find("div", attrs={"id": "siteTable"})
    if siteTable != None:
        things = siteTable.findAll("div", attrs={"class": "thing"})

        users = []
        posts = []

        for thing in things:
            if "data-permalink" in thing.attrs:
                posts.append(thing["data-permalink"])

            if "data-author" in thing.attrs:
                users.append(thing["data-author"])

        users = list(dict.fromkeys(users))
        posts = list(dict.fromkeys(posts))

        print(" Obtaining user data")
        process_user_data(user_data, users, users_all, _subreddit)

        print(" Obtaining posts data")
        process_post_data(post_data, comment_data, posts)

        return things[-1]['data-fullname']
    else:
        print("[ERROR]: Page: " + page_url + " didn´t have a div with id siteTable (?)")


parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--type", help="Category of scrapping for the given subreddit: ['', 'new', 'rising', 'top']", default="new"
)
parser.add_argument(
    "-s", "--subreddit", help="Subreddit to scrap: spain, europe, spicypillows...", default="spain"
)
parser.add_argument(
    "-n", "--number", help="Number of pages to scrap from the given subreddit and category", default=5
)
parser.add_argument(
    "-o",
    "--output",
    help="Choose the output file name, will have the following format: user_FILENAME.json", default="data"
)

args = parser.parse_args()

_type = args.type
_subreddit = args.subreddit
_output_file = args.output
_number_of_pages = args.number

print("Reddit Scrapper")
print(" Outputting data to: " + _output_file +"_data_type.json")
print(
    "---------------------------------------------------------------------------------"
)

user_data = []
post_data = []
comment_data = []

users_all = []

page_url = _BASE_URL + "/r/" + _subreddit + "/" + _type + "/"
print("Page 1 out of " + str(_number_of_pages))
last_post_id = process_page(user_data, post_data, comment_data, page_url, users_all)
print(last_post_id)

pages_processed = 1
while pages_processed < int(_number_of_pages):
    print("Page " + str(pages_processed+1) + " out of " + str(_number_of_pages))
    page_url = _BASE_URL + "/r/" + _subreddit + "/" + _type + "/" + "?count=" + str(pages_processed * _ITEMS_PER_PAGE) + "&after=" + last_post_id
    process_page(user_data, post_data, comment_data, page_url, users_all)
    pages_processed += 1


print(" Saving data to: user_" + _output_file + ".json...")
save_file("user_" + _output_file, user_data)
print(" Saving posts to: post_" + _output_file + ".json...")
save_file("post_" + _output_file, post_data)
print(" Saving comments to: comment_" + _output_file + ".json...")
save_file("comment_" + _output_file, comment_data)
