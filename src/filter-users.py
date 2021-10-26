import argparse
import logging
from pathlib import Path
import json
from typing import List

# get args

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--target', type=str, required=True)
args = arg_parser.parse_args()

# configure logger

logger = logging.getLogger('filter-users')
logging.basicConfig(level=logging.INFO)

# load files

target_path = Path(args.target).resolve()
users: List[dict] = []

if target_path.exists():
    logger.info('loading...')

    file_paths = list(target_path.iterdir())
    file_count = len(file_paths)

    for index, file_path in enumerate(file_paths):
        with file_path.open("r") as file:
            user = json.loads(file.read())
            users.append(user)

        logger.info('loaded ({index}/{file_count}) {path}'.format(
            path=file_path,
            index=index + 1,
            file_count=file_count,
        ))

else:
    logger.error('not found {path}'.format(path=target_path))

# filter


def is_protected(user: dict) -> bool:
    protected = user.get('protected')
    return isinstance(protected, bool) and protected


def is_screen_name(user: dict, screen_name: str) -> bool:
    user_screen_name = user.get('screen_name')
    is_str = isinstance(user_screen_name, str)
    return is_str and screen_name == user_screen_name


public_users = filter(lambda u: not is_protected(u), users)

filter_result = list(public_users)

logger.info('filtered ({original} -> {filtered})'.format(
    original=len(users),
    filtered=len(filter_result),
))

# save

output_path = target_path.joinpath('filtered.json')

with output_path.open(mode='w', encoding='utf-8') as file:
    data = json.dumps(filter_result, ensure_ascii=False)
    file.write(data)

logger.info('saved {output_path}'.format(output_path=output_path))
