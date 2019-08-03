#!/usr/bin/env python3
'''
get_cats.py

a script to get cat images, gifs, and vids from reddit
doing this so i can send them to my mom using an applescript

May 2019
ginglis
'''

import glob
import requests
import random
import os
from io import open as iopen
import sys

'''Globals/Metadata'''

SUBREDDITS = [
        'cats',
        'catsstandingup',
        'catslaps',
        'catsareassholes',
        'chonkers',
        'bigcatgifs',
        'babybigcatgifs',
        'holdmycatnip',
        'CatsISUOTTATFO',
        'catsareliquid'
        ]

REDDIT_URL = 'https://reddit.com/r/{}/.json?sort=top'
GFYCAT = 'https://api.gfycat.com/v1/gfycats/{}'

# shout out cse-20289-sp19
headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cat-message'))}

'''Functions'''

def dl_content(url, source, title):
    if source == 'gfycat.com':
        gfy_url = url.split('/')[-1]

        r = requests.get(GFYCAT.format(gfy_url)).json()
        gfy_mp4url = r['gfyItem']['mp4Url']

        return gfy_mp4url, title

    elif source == 'i.imgur.com':
        img_url = url.replace('.gifv', '.mp4')
        return img_url, title

    else:
        return url, title

def handle_url(url=REDDIT_URL):
    subreddit = random.choice(SUBREDDITS)
    url       = url.format(subreddit)
    response  = requests.get(url, headers=headers).json()
    data      = response['data']['children']
    images    = []

    for post in data:
        if post['data']['stickied']:
            continue

        url    = post['data']['url']
        source = post['data']['domain']
        title  = post['data']['title']

        images.append((url, source, title))

    img_url, img_source, img_title = random.choice(images)
    return dl_content(img_url, img_source, img_title)

def write_file(img_url, title):
    if not img_url:
        sys.stderr.write('Something went wrong - no url\n')
        return

    if 'v.redd.it' in img_url:
        sys.stderr.write('''
        The source of this file is v.redd.it.
        Unfortunately, reddit recognizes requests to this source as being from a script and blocks them.
        Apologies.
        ''')
        return

    extension = '.jpg'
    for ext in ('mp4', 'png', 'gif', 'jpeg', 'jpg'):
        if ext in img_url:
            extension = '.' + ext

    # remove former cat file, necessary for applescript
    for cat_file in glob.glob('cat*'):
        os.unlink(cat_file)

    fname = 'cat' + extension
    r = requests.get(img_url, stream=True)

    # Print title for text msg
    print(title)

    with iopen(fname, 'wb') as file:
        file.write(r.content)

'''Main Execution'''

img, title = handle_url()
write_file(img, title)
