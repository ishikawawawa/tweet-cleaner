import configparser
import tweepy
import os

config = configparser.ConfigParser()
config.read("./config.ini")

twitterConf = config["Twitter"]

auth = tweepy.OAuthHandler(twitterConf["CONSUMER_TOKEN"], twitterConf["CONSUMER_TOKEN_SECRET"])

authUrl = auth.get_authorization_url()
print("auth url : {}".format(authUrl))

print("waiting input pin")
pin = input().strip()

auth.get_access_token(pin)
print("access key : {}".format(auth.access_token))
print("access secret : {}".format(auth.access_token_secret))

auth.set_access_token(auth.access_token, auth.access_token_secret)
api = tweepy.API(auth)

me = api.me()
print("{}".format(me.name))