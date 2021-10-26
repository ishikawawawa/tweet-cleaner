import argparse
import configparser
import tweepy
import logging
from pathlib import Path

# section/option names

SECTION_TWITTER = 'Twitter'
OPTION_CONSUMER_TOKEN = 'CONSUMER_TOKEN'
OPTION_CONSUMER_TOKEN_SECRET = 'CONSUMER_TOKEN_SECRET'
OPTION_ACCESS_TOKEN = 'ACCESS_TOKEN'
OPTION_ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config', type=str, required=True)
args = arg_parser.parse_args()

# configure loogger

logger = logging.getLogger('auth')
logging.basicConfig(level=logging.INFO)

# load configure

config_parser = configparser.ConfigParser()
config_parser.read(args.config)
tw_conf = config_parser[SECTION_TWITTER]

# init

consumer_key = tw_conf[OPTION_CONSUMER_TOKEN]
consumer_secret = tw_conf[OPTION_CONSUMER_TOKEN_SECRET]

auth = tweepy.OAuthHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
)

# auth

auth_url = auth.get_authorization_url()
logger.info('auth url : {auth_url}'.format(auth_url=auth_url))
logger.info('waiting pin code')
pin = input().strip()

auth.get_access_token(pin)

# test

access_token = auth.access_token
access_token_secret = auth.access_token_secret

auth.set_access_token(
    key=access_token,
    secret=access_token_secret,
)

tw_client = tweepy.API(auth=auth)

me = tw_client.verify_credentials()

logger.info('logged in {name}@{screen_name} ({user_id})'.format(
    name=me.name,
    screen_name=me.screen_name,
    user_id=me.id,
))

# save tokens

filename = 'config.{screen_name}.ini'.format(screen_name=me.screen_name)
base_path = Path('config')
output_path = base_path.joinpath(filename)

if not base_path.exists():
    base_path.mkdir()

output_config = configparser.RawConfigParser()
output_config.add_section(SECTION_TWITTER)
output_config.set(
    section=SECTION_TWITTER,
    option=OPTION_CONSUMER_TOKEN,
    value=consumer_key,
)
output_config.set(
    section=SECTION_TWITTER,
    option=OPTION_CONSUMER_TOKEN_SECRET,
    value=consumer_secret,
)
output_config.set(
    section=SECTION_TWITTER,
    option=OPTION_ACCESS_TOKEN,
    value=access_token,
)
output_config.set(
    section=SECTION_TWITTER,
    option=OPTION_ACCESS_TOKEN_SECRET,
    value=access_token_secret,
)

with output_path.open(mode='w', encoding='utf-8') as file:
    output_config.write(file)
