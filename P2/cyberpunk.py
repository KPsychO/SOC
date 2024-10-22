import matplotlib.pyplot as plt
import nltk
import pandas as pd
from textblob import TextBlob
import click

tknzr = nltk.tokenize.TweetTokenizer()

def preprocess(text):
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens


df = pd.read_csv("cyberpunk.csv")
df["tokens"] = df["text"].apply(preprocess)
df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["day"] = df["created_at"].dt.to_period("D")
print(df)

def select_token(token):
    return df[df["tokens"].apply(lambda x: token in x)]

def plot_time_density(df, keyword, label):
    twits = select_token(keyword)
    time_density = twits["day"].value_counts()
    time_density.sort_index().plot(kind="line", label=label)

def plot_count(df, param):
    count = df.groupby(["day"])[param].value_counts().sort_index()
    count.plot(kind="line", label=param, fontsize=6)

def plot_sentiment(df):
    sdf = df["sentiment"].value_counts().rename_axis('sentiment').reset_index(name='count')
    sdf = sdf.drop([0])
    sdf.plot.scatter(x="count", y="sentiment")

def plot_sources(df):
    sdf = df["source"].value_counts().rename_axis('source').reset_index(name='count')
    sdf = sdf.drop(sdf[sdf['count'] < 20].index)
    print(sdf)
    sdf.plot.bar(x="source", y="count", fontsize=6)


# plot_time_density(df, "bad", "bad")
# plot_time_density(df, "good", "good")

# plt.legend()
# plt.savefig("bad_vs_good.png")

# plot_count(df, "retweet_count")

# plt.legend()
# plt.savefig("retweet_count.png")

# plot_sentiment(df)

# plt.legend()
# plt.savefig("sentiment.png")

plot_sources(df)

plt.legend()
plt.savefig("sources.png")