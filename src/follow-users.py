import argparse
import configparser
from typing import List
import tweepy
import time
import logging
from pathlib import Path
import json

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--config',
    type=str,
    required=True,
)
arg_parser.add_argument(
    '--target',
    type=str,
    required=True,
)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('follow-users')
logging.basicConfig(level=logging.INFO)

# load configure

config_parser = configparser.ConfigParser()
config_parser.read(args.config)
tw_conf = config_parser['Twitter']

# load target

target_path = Path(args.target).resolve()

if not target_path.exists():
    logger.error('not found {path}'.format(path=target_path))
    exit(1)

users: List[dict] = []

with target_path.open('r') as file:
    for user in json.loads(file.read()):
        users.append(user)

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

# follow users

user_count = len(users)

for index, user in enumerate(users):
    logger.info('following... ({index}/{user_count}) @{screen_name}'.format(
        index=index + 1,
        user_count=user_count,
        screen_name=user.get('screen_name'),
    ))
    tw_client.create_friendship(user_id=user.get('id_str'))
    # このスリープが必要かどうか...一応...
    time.sleep(3)
