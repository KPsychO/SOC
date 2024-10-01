import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import re

# Configure a requests session to implement retries in case of an invalid server response
ses = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
ses.mount("https://", HTTPAdapter(max_retries=retries))


def make_request(url):  # makes a request using the session configured previously
    return ses.get(url)


def scrap_user_posts(
    posts, thing, user
):  # Process data from the post published by the user on r/spain
    top_matter = thing.find("div", attrs={"class": "top-matter"})
    title_all = top_matter.find("a", attrs={"class": "title"})
    title = title_all.text
    desc = ""
    tagline = top_matter.find("p", attrs={"class": "tagline"})
    date = tagline.find("time")["title"]

    pattern = re.compile("/r/spain/.*")
    if pattern.match(title_all["href"]):
        url_post = "https://old.reddit.com" + title_all["href"]

        res_post = make_request(url_post)
        html_post = BeautifulSoup(res_post.text, "html.parser")

        expando = html_post.find("div", attrs={"class": "expando"})
        if expando != None:
            md = expando.find("div", attrs={"class": "md"})
            if md != None:
                desc = md.text

        posts.append(
            {
                "title": title,
                "post_url": url_post,
                "date": date,
                "desc": desc,
                "author": user,
            }
        )


def scrap_user_comments(
    comments, thing, user
):  # Process data from the comments published by the user on r/spain
    parent = thing.find("p", attrs={"class": "parent"})
    if parent != None:
        title = parent.find("a", attrs={"class": "title"})
        post = title["href"]

        entry = thing.find("div", attrs={"class": "entry"})
        tagline = entry.find("p", attrs={"class": "tagline"})
        date = tagline.find("time")["title"]

        usertext_body = entry.find("div", attrs={"class": "usertext-body"})

        if usertext_body != None:
            md = usertext_body.find("div", attrs={"class": "md"})
            if md != None:
                text = md.text

                comments.append(
                    {
                        "text": text,
                        "date": date,
                        "parent": post,
                        "author": user,
                    }
                )


def process_post_comment_data_from_userList(
    posts, comments, html, user, subreddit
):  # Proces a given html to scrap a user posts and comments in a given subredit
    siteTable = html.find("div", attrs={"id": "siteTable"})
    if siteTable != None:
        things = siteTable.findAll("div", attrs={"class": "thing"})

        for thing in things:
            if thing["data-subreddit"] == subreddit:
                if thing["data-type"] == "link":
                    scrap_user_posts(posts, thing, user)
                elif thing["data-type"] == "comment":
                    scrap_user_comments(comments, thing, user)


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
        res = make_request(user_url)
        html = BeautifulSoup(res.text, "html.parser")

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


def obtain_users_list_from_postList(
    users_list, posts
):  # Extracts a list of usernames from the html corresponding to posts passed
    for post in posts:
        user = post.find("a", attrs={"class": "author"})
        if user != None:
            users_list.append(user.text)
    users_list = list(dict.fromkeys(users_list))


def obtain_post_links_from_postList(
    posts_list, posts
):  # Extracts a list of post links from the html corresponding to posts passed
    for post in posts:
        top_matter = post.find("div", attrs={"class": "top-matter"})
        if top_matter != None:
            buttons = top_matter.find("ul", attrs={"class": "buttons"})
            if buttons != None:
                comments = buttons.find("a", attrs={"data-event-action": "comments"})
                posts_list.append(comments["href"])
    posts_list = list(dict.fromkeys(posts_list))


base_url = "https://old.reddit.com/r/spain/new/"
base_url_user = "https://old.reddit.com/user/"
subreddit = "spain"

res = make_request(base_url)
html = BeautifulSoup(res.text, "html.parser")
siteTable = html.find("div", attrs={"id": "siteTable"})
posts = siteTable.findAll("div", attrs={"class": "link"})

users_list = []
obtain_users_list_from_postList(users_list, posts)
print(users_list)

user_data_json = []
process_user_data(user_data_json, base_url_user, users_list, subreddit)
print(user_data_json)

posts_list = []
obtain_post_links_from_postList(posts_list, posts)
print(posts_list)
