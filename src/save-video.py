import argparse
import configparser
import tweepy
import logging
from pathlib import Path
import requests

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--config',
    type=str,
    required=True,
)
arg_parser.add_argument(
    '--id',
    type=str,
    required=True,
)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('get-following')
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

#

filename = "{id}.mp4".format(id=args.id)
output_dir = Path('output/{id}'.format(id=args.id))
file_path = output_dir.joinpath(filename)

if not output_dir.exists():
    output_dir.mkdir(parents=True)

# test

me = tw_client.verify_credentials()
logger.info('run {name}@{screen_name} ({user_id})'.format(
    name=me.name,
    screen_name=me.screen_name,
    user_id=me.id,
))

# get tweet

status = tw_client.get_status(args.id)

if 'media' in status.extended_entities:
    for media in status.extended_entities['media']:
        if (media['type'] == "video"):
            video_info = media['video_info']
            with file_path.open(mode='wb') as file:
                for variant in video_info['variants']:
                    if (variant['content_type'] == 'video/mp4'):
                        result = requests.get(variant['url'])
                        file.write(result.content)
