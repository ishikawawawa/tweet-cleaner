import tweepy
import configparser
import logging
import logging.config

logging.config.fileConfig("./logging.conf")

config = configparser.ConfigParser()
config.read("./config.ini")
twitterConf = config["Twitter"]

auth = tweepy.OAuthHandler(twitterConf["CONSUMER_TOKEN"], twitterConf["CONSUMER_TOKEN_SECRET"])
auth.set_access_token(twitterConf["ACCESS_TOKEN"], twitterConf["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)

me = api.me()
logging.info("run @{} ({})".format(me.name, me.id))

for follower in tweepy.Cursor(api.followers_ids, user_id=me.id, stringify_ids=True).items():
    api.create_block(user_id=follower)
    api.destroy_block(user_id=follower)
    api.create_friendship(user_id=follower)
