import argparse
import logging
from pathlib import Path
import requests
import utils

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

# init twitter client

tw_client = utils.twitter_client_from_conf(args.config)

#

filename = "{id}.mp4".format(id=args.id)
output_dir = Path('output/{id}'.format(id=args.id))
file_path = output_dir.joinpath(filename)

utils.complete_directory(output_dir)

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
