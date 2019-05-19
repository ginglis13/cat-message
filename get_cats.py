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
import pprint
import os
from io import open as iopen
from urllib.parse import urlsplit

'''Globals/Metadata'''

SUBREDDITS = [
        'cats',
        'catsstandingup',
        'catslaps',
        'catsareassholes',
        'chonkers',
        'bigcatgifs',
        'babybigcatgifs',
        'holdmycatnip'
        ]

REDDIT_URL = 'https://reddit.com/r/{}/.json'
GFYCAT = 'https://gfycat.com/cajax/get/{}'

headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}

'''Functions'''

def dl_content(url, source):
    if source == 'gfycat.com':
        gfy_url = url.split('/')[-1]

        r = requests.get(GFYCAT.format(gfy_url)).json()
        gfy_mp4url = r['gfyItem']['mp4Url']

        return gfy_mp4url

    elif source == 'i.imgur.com':
        img_url = url.replace('.gifv', '.mp4')
        return img_url

    else:
        return url

def handle_url(url=REDDIT_URL):

    url      = url.format(random.choice(SUBREDDITS))
    response = requests.get(url, headers=headers).json()
    data     = response['data']['children']
    images   = []

    for post in data:

        d = {}
        if post['data']['stickied'] == True:
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

    # Print title for text msg
    print("Title: {}".format(img_title[1]))

    #print('Using url: {}'.format(img_url))

    return dl_content(img_url, img_source)

def write_file(img_url):
    #print('img url: {}'.format(img_url))
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
            print('The source of this file is v.reddit. Unfortunately, reddit recognizes requests to this source as being from a script and blocks them. Apologies.')
        else:
            ext = '.jpg'

        fname = 'cat' + ext
        r = requests.get(img_url, stream=True)
        with iopen(fname, 'wb') as file:
            file.write(r.content)
    else:
        print('Something went wrong - no url')

'''Main Execution'''

# remove former cat file, necessary for applescript
os.popen('rm ~/projects/cat-message/cat*')

img = handle_url(REDDIT_URL)
write_file(img)
