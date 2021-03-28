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

for status in tweepy.Cursor(api.user_timeline, user_id = me.id, count = 200).items():
    api.destroy_status(status.id_str)
    logging.info("deleted : {} ({})".format(status.text, status.id_str))
