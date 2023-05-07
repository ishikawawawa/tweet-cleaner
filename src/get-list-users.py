import argparse
import configparser
from typing import List
import tweepy
import time
import logging
from pathlib import Path
import json
from tweepy.user import User

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--config',
    type=str,
    required=True,
)
arg_parser.add_argument(
    '--list-id',
    type=str,
    required=True,
)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('get-list-users')
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

# get following

users: List[User] = []

for user in tweepy.Cursor(
        tw_client.get_list_members,
        list_id=args.list_id,
        count=5000,
).items():
    users.append(user)

logger.info('got users ({number})'.format(number=len(users)))

# save users

now = time.strftime("%Y%m%d%H%M%S")

output_path = Path('output/get-list-users-{screen_name}-{now}'.format(
    screen_name=me.screen_name,
    now=now,
))

if not output_path.exists():
    output_path.mkdir(parents=True)

for user in users:
    filename = "{user_name}.json".format(user_name=user.id)
    filepath = output_path.joinpath(filename)

    with filepath.open(mode='w', encoding='utf-8') as file:
        data = json.dumps(user._json, sort_keys=False, ensure_ascii=False)
        file.write(data)

logger.info('saved followings {filepath}'.format(filepath=output_path))
