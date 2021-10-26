import argparse
import logging
import configparser
import tweepy
import tweepy.models

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config', type=str, required=True)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('delete-tweet')
logging.basicConfig(level=logging.INFO)

# load configure

config_parser = configparser.ConfigParser()
config_parser.read(args.config)
tw_conf = config_parser['Twitter']

# init twitter client

tw_auth = tweepy.OAuthHandler(
    consumer_key=tw_conf['CONSUMER_TOKEN'],
    consumer_secret=tw_conf['CONSUMER_TOKEN_SECRET'],
)
tw_auth.set_access_token(
    key=tw_conf['ACCESS_TOKEN'],
    secret=tw_conf['ACCESS_TOKEN_SECRET'],
)
tw_client = tweepy.API(auth=tw_auth)

# delete tweets

me = tw_client.verify_credentials()
logger.info('run {name}@{screen_name} ({user_id})'.format(
    name=me.name,
    screen_name=me.screen_name,
    user_id=me.id,
))

for status in tweepy.Cursor(
        tw_client.user_timeline,
        user_id=me.id,
        count=200,
).items():
    tw_client.destroy_status(status.id_str)
    logger.info('deleted : {text} ({tweet_id})'.format(
        text=status.text,
        tweet_id=status.id_str,
    ))
