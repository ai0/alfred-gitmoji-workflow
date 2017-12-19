#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import json
import os.path
import re
import shutil
import urllib.parse
import urllib.request

import constants

image_url_prefix = 'https://emojipedia-us.s3.amazonaws.com/thumbs/240/apple/118/'


def get_gitmojis():
    with urllib.request.urlopen(constants.GITMOJIS_JSON_URL) as resp:
        return json.loads(resp.read())['gitmojis']


def get_emoji_image_url(emoji):
    req = urllib.request.Request(
        'https://emojipedia.org/search/?q=' + urllib.parse.quote(emoji))
    req.add_header('User-Agent', 'curl')
    with urllib.request.urlopen(req) as resp:
        find = re.search('<meta property="og:image" content="([^"]+)" />',
                         resp.read().decode('utf-8'))
        image_name = find.group(1).split('/')[-1]
        return image_url_prefix + image_name


def download_emoji_image():
    for emoji in get_gitmojis():
        emoji_image_path = './emojis/%s.png' % emoji['name']
        if not os.path.exists(emoji_image_path):
            emoji_image_url = get_emoji_image_url(emoji['emoji'])
            with urllib.request.urlopen(emoji_image_url) as emoji_image, open(
                    emoji_image_path, 'wb') as emoji_image_file:
                shutil.copyfileobj(emoji_image, emoji_image_file)


if __name__ == '__main__':
    download_emoji_image()
