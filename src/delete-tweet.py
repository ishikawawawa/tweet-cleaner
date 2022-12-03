import argparse
import logging
import tweepy
import tweepy.models
import utils

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config', type=str, required=True)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('delete-tweet')
logging.basicConfig(level=logging.INFO)

# init twitter client

tw_client = utils.twitter_client_from_conf(args.config)

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
