import tweepy
import configparser
import pathlib


def twitter_client_from_conf(config_file_path: str) -> tweepy.API:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)
    tw_conf = config_parser['Twitter']
    tw_auth = tweepy.OAuthHandler(
        consumer_key=tw_conf['CONSUMER_TOKEN'],
        consumer_secret=tw_conf['CONSUMER_TOKEN_SECRET'],
    )
    tw_auth.set_access_token(
        key=tw_conf['ACCESS_TOKEN'],
        secret=tw_conf['ACCESS_TOKEN_SECRET'],
    )
    tw_client = tweepy.API(auth=tw_auth)
    return tw_client


def complete_directory(dir_path: str) -> pathlib.Path:
    path = pathlib.Path(dir_path)

    if not path.exists():
        path.mkdir(parents=True)

    return path
