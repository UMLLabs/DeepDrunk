import tweepy
from tweepy import OAuthHandler
import json
import re
import csv
import getopt
import sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['handle=', 'api_key_file='])
    except getopt.GetoptError as error:
        print error
        sys.exit(2)
    handle = None
    api_key_file = None

    for opt, arg in opts:
        if opt == '--handle':
            handle = arg
        elif opt == '--api_key_file':
            api_key_file = arg
        else:
            print "Option {} is not valid!".format(opt)

    api_file = open(api_key_file)

    lines = api_file.readlines()
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_secret = None

    for line in lines:
        split_line = line.split('=')

        if split_line[0].strip() == 'consumer_key':
            consumer_key = split_line[1].strip()
        elif split_line[0].strip() == 'consumer_secret':
            consumer_secret = split_line[1].strip()
        elif split_line[0].strip() == 'access_token':
            access_token = split_line[1].strip()
        elif split_line[0].strip() == 'access_secret':
            access_secret = split_line[1].strip()

    get_tweets(handle, consumer_key, consumer_secret, access_token, access_secret)
def process(tweet):
  text = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
  return text

def get_tweets(screen_name, consumer_key, consumer_secret, access_token, access_secret):
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

if __name__ == '__main__':
    main()
