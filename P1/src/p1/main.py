import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import re

# Configure a requests session to implement retries in case of an invalid server response
ses = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
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


def process_post_comment_data_from_userList(
    posts, comments, html, user, subreddit
):  # Proces a given html to scrap a user posts and comments in a given subredit
    siteTable = html.find("div", attrs={"id": "siteTable"})
    if siteTable != None:
        things = siteTable.findAll("div", attrs={"class": "thing"})

        for thing in things:
            if thing["data-subreddit"] == subreddit:
                if thing["data-type"] == "link":
                    # scrap_user_posts(posts, thing, user)
                    posts.append(thing['data-permalink'])
                elif thing["data-type"] == "comment":
                    # scrap_user_comments(comments, thing, user)
                    comments.append(thing['data-permalink'])


def obtain_user_karma(
    karma, html
):  # Extracts the total user karma (post+comments karma) from a given html
    side = html.find("div", attrs={"class": "side"})
    if side != None:
        post_karma = side.find("span", attrs={"class": "karma"}).text
        comment_karma = side.find("span", attrs={"class": "comment-karma"}).text
        karma = int(post_karma.replace(",", "")) + int(comment_karma.replace(",", ""))


def process_user_data(
    user_data_json, base_url_user, users_list, subreddit
):  # Creates the URL for a user profile from a given username and scraps itś karma, posts and comments in r/spain
    for user in users_list:
        user_url = base_url_user + user
        html = make_request(user_url)

        # Karma
        karma = 0
        obtain_user_karma(karma, html)

        # Posts & Comments
        posts = []
        comments = []
        process_post_comment_data_from_userList(posts, comments, html, user, subreddit)
        user_data_json.append(
            {"username": user, "karma": karma, "posts": posts, "comments": comments}
        )


base_url = "https://old.reddit.com/r/spain/new/"
base_url_user = "https://old.reddit.com/user/"
subreddit = "spain"

html = make_request(base_url)

siteTable = html.find("div", attrs={"id": "siteTable"})
things = siteTable.findAll("div", attrs={"class": "thing"})

users = []
posts = []
for thing in things:
    # print(thing)
    # print(thing['data-permalink'])
    # print(thing['data-author'])
    
    # COMPROBAR QUE LA CLAVE EXISTE
    posts.append(thing['data-permalink'])
    users.append(thing['data-author'])

user_data_json = []
process_user_data(user_data_json, base_url_user, users, subreddit)
print(user_data_json)