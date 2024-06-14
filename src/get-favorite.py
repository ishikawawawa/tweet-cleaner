import argparse
import configparser
from typing import List
import tweepy
import time
import logging
from pathlib import Path
import json
from tweepy.user import User
from tweepy.tweet import Tweet

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--config',
    type=str,
    required=True,
)
arg_parser.add_argument(
    '--screenname',
    type=str,
    required=True,
)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('get-favorite')
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

# test

me = tw_client.verify_credentials()
logger.info('run {name}@{screen_name} ({user_id})'.format(
    name=me.name,
    screen_name=me.screen_name,
    user_id=me.id,
))

# get favorite

screen_name = args.screenname
favorites = tw_client.get_favorites(screen_name=screen_name, count=200).items()

logger.info('got favorites ({number})'.format(number=len(favorites)))

# save favorites

now = time.strftime("%Y%m%d%H%M%S")

output_path = Path('output/{now}'.format(now=now))

if not output_path.exists():
    output_path.mkdir(parents=True)

for favorite in favorites:
    filename = "{id}.json".format(id=favorite.id)
    filepath = output_path.joinpath(filename)

    with filepath.open(mode='w', encoding='utf-8') as file:
        data = json.dumps(favorite._json, sort_keys=False, ensure_ascii=False)
        file.write(data)

logger.info('saved favorites {filepath}'.format(filepath=output_path))
