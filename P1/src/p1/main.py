import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import argparse
import json

# Global vars
_BASE_URL = "https://old.reddit.com"
_BASE_URL_USER = _BASE_URL + "/user/"

# Configure a requests session to implement retries in case of an invalid server response
ses = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
ses.mount("https://", HTTPAdapter(max_retries=retries))


def make_request(url):  # makes a request using the session configured previously
    res = ses.get(url)
    return BeautifulSoup(res.text, "html.parser")


# def scrap_user_posts(
#     posts, thing, user
# ):  # Process data from the post published by the user on r/spain
#     top_matter = thing.find("div", attrs={"class": "top-matter"})
#     title_all = top_matter.find("a", attrs={"class": "title"})
#     title = title_all.text
#     desc = ""
#     tagline = top_matter.find("p", attrs={"class": "tagline"})
#     date = tagline.find("time")["title"]

#     pattern = re.compile("/r/spain/.*")
#     if pattern.match(title_all["href"]):
#         url_post = "https://old.reddit.com" + title_all["href"]

#         res_post = make_request(url_post)
#         html_post = BeautifulSoup(res_post.text, "html.parser")

#         expando = html_post.find("div", attrs={"class": "expando"})
#         if expando != None:
#             md = expando.find("div", attrs={"class": "md"})
#             if md != None:
#                 desc = md.text

#         posts.append(
#             {
#                 "title": title,
#                 "post_url": url_post,
#                 "date": date,
#                 "desc": desc,
#                 "author": user,
#             }
#         )


# def scrap_user_comments(
#     comments, thing, user
# ):  # Process data from the comments published by the user on r/spain
#     parent = thing.find("p", attrs={"class": "parent"})
#     if parent != None:
#         title = parent.find("a", attrs={"class": "title"})
#         post = title["href"]

#         entry = thing.find("div", attrs={"class": "entry"})
#         tagline = entry.find("p", attrs={"class": "tagline"})
#         date = tagline.find("time")["title"]

#         usertext_body = entry.find("div", attrs={"class": "usertext-body"})

#         if usertext_body != None:
#             md = usertext_body.find("div", attrs={"class": "md"})
#             if md != None:
#                 text = md.text

#                 comments.append(
#                     {
#                         "text": text,
#                         "date": date,
#                         "parent": post,
#                         "author": user,
#                     }
#                 )


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
            {"username": user, "karma": karma, "posts": posts, "comments": comments}
        )


def save_file(file, data):
    with open(file + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help = "Type of scrapping: ['', 'new', 'rising', 'top']")
parser.add_argument("-s", "--subreddit", help = "Subreddit to scrap: spain, europe, spicypillows...")
parser.add_argument("-o", "--output", help = "Choose the output file name, will have the following format: user_FILENAME.json")

args = parser.parse_args()

_type = args.type
_subreddit = args.subreddit
_output_file = args.output

print("Reddit Scrapper")
print(" Scrapping subreddit: " + _BASE_URL + "/r/" + _subreddit + "/" + _type + "/")
print(" Outputting data to: data_type" + _output_file + ".json")
print(
    "--------------------------------------------------------------------------------------"
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

user_data = []
process_user_data(user_data, users, _subreddit)
save_file("user_" + _output_file, user_data)
