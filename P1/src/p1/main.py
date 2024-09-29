import requests
from bs4 import BeautifulSoup
import time
import re

def scrap_posts(posts, thing):
    top_matter = thing.find("div", attrs={"class": "top-matter"})
    title_all = top_matter.find("a", attrs={"class": "title"})
    title = title_all.text
    desc = ""
    tagline = top_matter.find("p", attrs={"class": "tagline"})
    date = tagline.find("time")["title"]

    pattern = re.compile("/r/spain/.*")
    if pattern.match(title_all["href"]):
        url_post = "https://old.reddit.com" + title_all["href"]

        time.sleep(1)
        res_post = requests.get(url_post)
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

def scrap_comments(comments, thing):
    parent = thing.find("p", attrs={"class": "parent"})
    if parent != None:
        title = parent.find("a", attrs={"class": "title"})
        post = title["href"]

        entry = thing.find("div", attrs={"class": "entry"})

        tagline = entry.find("p", attrs={"class": "tagline"})
        date = tagline.find("time")["title"]

        usertext_body = entry.find(
            "div", attrs={"class": "usertext-body"}
        )

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

def obtain_users_list_from_url(users, base_url):
    res = requests.get(base_url)
    html = BeautifulSoup(res.text, "html.parser")
    siteTable = html.find("div", attrs={"id": "siteTable"})
    posts = siteTable.findAll("div", attrs={"class": "link"})
    for post in posts:
        user = post.find("a", attrs={"class": "author"})
        if user != None:
            users.append(user.text)

def obtain_user_karma(karma, html):
    side = html.find("div", attrs={"class": "side"})
    if side != None:
        post_karma = side.find("span", attrs={"class": "karma"}).text
        comment_karma = side.find("span", attrs={"class": "comment-karma"}).text
        karma = int(post_karma.replace(",", "")) + int(comment_karma.replace(",", ""))


base_url = "https://old.reddit.com/r/spain/new/"

users = []
obtain_users_list_from_url(users, base_url)
print(users)


users = list(dict.fromkeys(users))
data = []
for user in users:
    user_url = "https://old.reddit.com/user/" + user
    time.sleep(1)
    res = requests.get(user_url)
    html = BeautifulSoup(res.text, "html.parser")

    # Karma
    karma = 0
    obtain_user_karma(karma, html)

    # Posts & Comments
    posts = []
    comments = []
    
    siteTable = html.find("div", attrs={"id": "siteTable"})

    if siteTable != None:
        things = siteTable.findAll("div", attrs={"class": "thing"})

        for thing in things:
            if thing["data-subreddit"] == "spain":
                if thing["data-type"] == "link":
                    scrap_posts(posts, thing)
                elif thing["data-type"] == "comment":
                    scrap_comments(comments, thing)

    data.append(
        {"username": user, "karma": karma, "posts": posts, "comments": comments}
    )

print(data)
