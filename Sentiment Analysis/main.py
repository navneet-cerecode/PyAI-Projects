# LIBRARIES USED : textblob nltk
# Project on Natural Language Processing

from textblob import TextBlob

with open("myText.txt", "r") as f:
    text = f.read()

blob = TextBlob(text)
sentiment = blob.sentiment.polarity #-1 to 1
print(sentiment)

#Can be used for Twitter Analysis, Stock Predictions