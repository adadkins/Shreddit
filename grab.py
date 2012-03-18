#!/usr/bin/env python2

import sys
import json # from json import loads, dumps
from urllib2 import urlopen, HTTPError
from time import sleep

f = open('user.json', 'r')
user = json.load(f)['user']
f.close()

sub_section = 'comments'
after = ''

init_url = 'http://www.reddit.com/user/{user}/comments/.json?after=%s'.format(user=user)
next_url = init_url % after

try:
    http = urlopen(next_url)
except HTTPError:
    raise HTTPError("You seem to have given an invalid user")

try:
    reddit = json.load(http)
except ValueError:
    raise ValueError("Failed to decode json.")

datum = []
while True:
    after = reddit['data']['after']
    children = reddit['data']['children']

    # This bit fills datum with the id (for removal) and the date (for saving recent posts)
    for child in children:
        child_data = child['data']
        if 'id' in child_data:
            datum.append({
                'id': child_data[u'id'],
                'created': child_data['created'],
                'body': child_data['body'],
                'subreddit': child_data['subreddit']})

    if after == None:
        break

    next_url = init_url % after
    http = urlopen(next_url)
    reddit = json.load(http)
    sleep(1) # don't want to hammer reddit to hard

f = open('data.json', 'w')
json.dump(datum, f)
f.close()
