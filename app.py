import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import csv
import pickle
import os
import tweepy
import altair as alt
import plotly.express as px
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
# creating the authentication object, setting access token and creating the api object
auth = tweepy.OAuthHandler("Pa2F16xpTRf2y4rQq5VoaUGxT", "t9HdeGSqflPFitZN9X8Klh5knx8deV9UfvaOpvwo644CiBxrUz")
auth.set_access_token("3151860468-eeg9ZuRvU9sJ7KPxpOWdUVD1ZZwfOFsXMEiQT9Y", "sdvOMxx8keXbL7mBX94njYSBIk7zIbcBkaZI24aBeyL3p")
api = tweepy.API(auth, wait_on_rate_limit=True)

with open('model_pkl' , 'rb') as f:
    model = pickle.load(f)


st.title("Sentiment Analysis of tweets")
st.sidebar.title("Some of the options of US Airlines ")

st.markdown(
    "## Welcome to sentimental Analysis ")
st.sidebar.markdown("This is the description on making of Sentiment Analysis 🐦 ")

twitter_id = st.text_input("Please enter your twitter id", "@imVkohli")
 

@st.cache(persist=True)
def load_data():
    data = pd.read_csv("out.csv")
    #data['tweets'] = pd.to_datetime(data['tweets'])
    return data


data = load_data()
tweets=data['tweets']
#st.line_chart()
#print(len(data))
 
def get_tweets(user_name, tweet_count):
    tweets_list = []
    img_url = ""
    name = ""
    try:
        for tweet in api.user_timeline(
            id=user_name, count=tweet_count, tweet_mode="extended"
        ):
            tweets_dict = {}
            tweets_dict["date_created"] = tweet.created_at
            tweets_dict["tweet_id"] = tweet.id
            tweets_dict["tweet"] = tweet.full_text
            tweets_list.append(tweets_dict)
        img_url = tweet.user.profile_image_url
        name = tweet.user.name
        screen_name = tweet.user.screen_name
        desc = tweet.user.description
    except BaseException as e:
        st.exception(
            "Failed to retrieve the Tweets. Please check if the twitter handle is correct. "
        )
        sys.exit(1)
    return tweets_list, img_url, name, screen_name, desc

def sentiment(tweets):
    j=0
    sentiment=[]
    while j<n:
        ex1 = tweets[0][j]['tweet']
        s=model.predict([ex1])
        if(s[0]=="joy" or s[0]=="surprise"):
            emotion=1
        elif(s[0]=="neutral"):
            emotion=0
        else:
            emotion=-1
        #print(emotion)
        sentiment.append(emotion)
        j=j+1
    return sentiment

n=200
tweets=get_tweets(twitter_id, n)
sentiments=sentiment(tweets)
i=0
tweets_data=[]
while i<n:
    #print(tweets[0][i]['tweet'])
    tweets_data.append(tweets[0][i]['tweet'])
    #print("\n")
    i=i+1

tweet_time=[]
i=0
import matplotlib
while i<n:
    tweet_time.append(tweets[0][i]['date_created'].date().month)
    i=i+1
#print(tweet_time)    
x =tweet_time
y = sentiments
data_to_show=[]
i=0
while i<n:
    data_to_show.append( [ y[i]])
    i=i+1
df = pd.DataFrame(data_to_show)
st.line_chart(df)           

#fig = px.bar(x,y,color=y,height=500)
#st.plotly_chart(fig)
fig = px.pie(values=y,names=x)
st.plotly_chart(fig) 
i=0 
positive=0
neutral=0
negative=0
for i in range(n):
    if(sentiments[i]==0):
        neutral+= 1

    elif sentiments[i]==1:
        positive+=1
    else:
        negative+=1
st.write("Positive: ")
st.write((positive*100)/n)
st.write("Neutral: ")
st.write((neutral*100)/n)
st.write("Negative: ")
st.write((negative*100)/n)
value=[(positive*100)/n,(neutral*100)/n,(negative*100)/n]
fig = px.pie(values=value,names=['Positive Tweets','Neutral Tweets','Negative Tweets'])
st.plotly_chart(fig) 
st.header("Positive Tweets")
start=0 
#st.line_chart(data)
for i in data['sentiment']:
    if(i==1): 
        st.write(tweets_data[start])
    start =start+1

 




