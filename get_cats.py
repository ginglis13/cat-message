#!/usr/bin/env python3
'''
get_cats.py

a script to get cat images, gifs, and vids from reddit
doing this so i can send them to my mom using an applescript

May 2019
ginglis
'''

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
        'CatsISUOTTATFO'
        ]

REDDIT_URL = 'https://reddit.com/r/{}/.json?sort=top'
GFYCAT = 'https://api.gfycat.com/v1/gfycats/{}'

# shout out cse-20289-sp19
headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}

'''Functions'''

def dl_content(url, source):
    title  = source[1]
    source = source[0]
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

    url      = url.format(subreddit)
    response = requests.get(url, headers=headers).json()
    data     = response['data']['children']
    images   = []

    for post in data:

        d = {}
        if post['data']['stickied']:
            continue

        url    = post['data']['url']
        title  = post['data']['title']
        source = post['data']['domain']

        d[url]=[source,title]

        images.append(d)

    img        = random.choice(images)
    img_url    = next(iter(img.keys()))
    img_source = next(iter(img.values()))
    img_title  = next(iter(img.values()))

    return dl_content(img_url, img_source)

def write_file(img_url, title):
    if img_url:
        if 'mp4' in img_url:
            ext = '.mp4'
        elif 'png' in img_url:
            ext = '.png'
        elif 'gif' in img_url:
            ext = '.gif'
        elif 'jpeg' in img_url:
            ext = '.jpeg'
        elif 'v.redd.it' in img_url:
            sys.stderr.write('The source of this file is v.redd.it. Unfortunately, reddit recognizes requests to this source as being from a script and blocks them. Apologies.\n')
            sys.exit()
        else:
            ext = '.jpg'

        # remove former cat file, necessary for applescript
        os.unlink('./cat*')

        fname = 'cat' + ext
        r = requests.get(img_url, stream=True)

        # Print title for text msg
        print('Title: {}'.format(title))

        with iopen(fname, 'wb') as file:
            file.write(r.content)
    else:
        sys.stderr.write('Something went wrong - no url\n')

'''Main Execution'''


img, title = handle_url()
write_file(img, title)
