import tweepy
from tweepy import OAuthHandler
import json
import re
import csv

consumer_key = 'DCvq1X9udDIAIxLaM3Tf7EsWi'
consumer_secret = 'G31xJMyTp3uHaEALR1NKjMmdpD3hwV2evWiToBGXFY55BZCQrS'
access_token = '31236647-YWCJlOQmsUOv55vEPP7GnnXvvy1YTS8Y75eumcffU'
access_secret = 'XV3xiBLxAJUBlK0ucHsOjNaJNid2q71npdQHgK11wm9Jl'


def process(tweet):
  text = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
  return text

def get_tweets(screen_name):
  #Twitter only allows access to a users most recent 3240 tweets with this method

  #authorize twitter, initialize tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  api = tweepy.API(auth)

  #initialize a list to hold all the tweepy Tweets
  alltweets = []

  #make initial request for most recent tweets (200 is the maximum allowed count)
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)

  #save most recent tweets
  alltweets.extend(new_tweets)

  #save the id of the oldest tweet less one
  oldest = alltweets[-1].id - 1

  #keep grabbing tweets until there are no tweets left to grab
  while len(new_tweets) > 0:
    print "getting tweets before %s" % (oldest)

    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    print "...%s tweets downloaded so far" % (len(alltweets))

  #transform the tweepy tweets into a 2D array that will populate the csv
  filtered = []
  for tweet in alltweets:
    if not tweet.text.encode("utf-8").startswith("RT"):
      filtered.append(tweet)

  outtweets = [process(tweet.text.encode("utf-8")) for tweet in filtered]

  #write the csv
  save_tweets = open(screen_name+"_tweets.txt", 'w')
  for tweet in outtweets:
    save_tweets.write(tweet+"\n")

  save_tweets.close()

def main():
  get_tweets("realDonaldTrump")

main()
