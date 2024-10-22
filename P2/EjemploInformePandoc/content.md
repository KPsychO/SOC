# Metodología

## Datos

Se usa el dataset sobre tuits de Elon Musk, `elon_tweets_2012-2022.csv`. Se
investigan los términos "twitter" y "tesla", por ser compañías relevantes. Esto
se ha decidido tras hacer un análisis de distintos términos. Los resultados
están en la sección [Resultados](#resultados).

## Código

```
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from textblob import TextBlob

tknzr = nltk.tokenize.TweetTokenizer()


def preprocess(text):
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens

df = pd.read_csv("elon_tweets_2012-2022.csv")
df["tokens"] = df["tweet"].apply(preprocess)
df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
df["sentiment"] = df["tweet"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["month"] = df["created_at"].dt.to_period("M")


def select_token(token):
    return df[df["tokens"].apply(lambda x: token in x)]
```

\clearpage

```
def plotsdf[sdf['sentiment'] == 0.000000].index

```

# Resultados

![En esta gráfica se ve la evolución de menciones a "tesla" frente
a "twitter"](tesla_vs_twitter.png){height=6cm}

![En esta gráfica se ve la polaridad del sentimiento frente a la longitud del
tuit](sentiment.png){height=6cm}
