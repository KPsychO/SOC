import requests
from bs4 import BeautifulSoup
import time
import re

base_url = "https://old.reddit.com/r/spain/new/"
# user_url = "https://old.reddit.com/user/" + user
# user_comments_url = "https://old.reddit.com/user/" + user + "/comments/"

# print("Processing posts from " + base_url + ", please wait...")

# res = requests.get(base_url)
# html = BeautifulSoup(res.text, "html.parser")

# siteTable = html.find("div", attrs={"id":"siteTable"})

# posts = siteTable.findAll("div", attrs={"class":"link"})

# users = []
# for post in posts:
#     # print(post)
#     user = post.find("a", attrs={"class":"author"})
#     if user != None:
#         # print(user.text)
#         users.append(user.text)

# print(users)
# print("Processing users, please wait...")

users = ['Vegetable-Read-4091', 'Inkinidas', 'nothereforthatlong', 'MeCagoEnPeronconga', 'bimbochungo', 'DiegoDGD', 'pabloquest', 'nothereforthatlong', 'afonsoeans', 'theclash8', 'AdAstra6767', 'NeoTheMan24', 'birrakilmister', 'dcarrero', 'paniniconqueso', 'Pacman_242', 'frurtainspeese', 'DiegoDGD', 'paniniconqueso', 'chthroka', 'advocado20', 'rex-ac']

#users = ['theclash8']

for user in users:
    print("Scrapping " + user + "...")
    user_url = "https://old.reddit.com/user/" + user
    # print(user_url)
    time.sleep(1)
    print(user_url)
    res = requests.get(user_url)
    html = BeautifulSoup(res.text, "html.parser")

    # print(html)

    # Karma
    side = html.find("div", attrs={"class":"side"})

    if side != None:
        post_karma = side.find("span", attrs={"class":"karma"}).text
        comment_karma = side.find("span", attrs={"class":"comment-karma"}).text

        karma = int(post_karma.replace(',','')) + int(comment_karma.replace(',',''))

        print(karma)
    else:
        print("[ERROR]: No se pudo acceder a: " + user_url)

    # Posts & Comments
    if side != None:
        siteTable = html.find("div", attrs={"id":"siteTable"})
        posts = []
        comments = []

        if siteTable != None:
            things = siteTable.findAll("div", attrs={"class":"thing"})
            
            for thing in things:
                if thing['data-subreddit'] == "spain":
                    if thing['data-type'] == "link":
                        top_matter = thing.find("div", attrs={"class":"top-matter"})
                        title_all = top_matter.find("a", attrs={"class":"title"})
                        title = title_all.text
                        desc = ""

                        pattern = re.compile("\/r\/spain\/.*")
                        if pattern.match(title_all['href']):
                            url_post = "https://old.reddit.com" + title_all['href']
                            tagline = top_matter.find("p", attrs={"class":"tagline"})
                            date = tagline.find("time")['title']

                            time.sleep(1)
                            print(url_post)
                            res_post = requests.get(url_post)
                            html_post = BeautifulSoup(res_post.text, "html.parser")

                            expando = html_post.find("div", attrs={"class": ["expando"]})
                            if expando != None:
                                md = expando.find("div", attrs={"class":"md"})
                                if md != None:
                                    desc = md.text
                        
                        posts.append(
                            {
                                "title" : title,
                                "post_url": url_post,
                                "date": date,
                                "desc": desc,
                                "author": user
                            }
                        )

                    elif thing['data-type'] == "comment":
                        print("Comentario!")
                    else:
                        print("[ERROR]: No es ni post ni comentario")

        print(posts)

