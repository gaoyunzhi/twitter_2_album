#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'twitter_2_album'

import math
import os
import cached_url
import re
import yaml
from telegram_util import cutCaption
import pic_cut
from bs4 import BeautifulSoup
import tweepy

prefix = 'https://m.twitter.cn/statuses/show?id='

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
auth = tweepy.OAuthHandler(CREDENTIALS['twitter_consumer_key'], CREDENTIALS['twitter_consumer_secret'])
auth.set_access_token(CREDENTIALS['twitter_access_token'], CREDENTIALS['twitter_access_secret'])
twitterApi = tweepy.API(auth)

def getTid(path):
	index = path.find('?')
	if index > -1:
		path = path[:index]
	return path.split('/')[-1]

def getCap(status, path, cap_limit):
	text = list(status.text)
	for x in status.entities.get('media', []):
		for pos in range(x['indices'][0], x['indices'][1]):
			text[pos] = ''
	suffix = ' [%s](%s)' % (status.user.name, path)	
	return cutCaption(''.join(text), suffix, cap_limit)

def getImages(status, image_limit):
	# TODO: support video as well...
	raw = [x['media_url'] for x in status.entities.get('media', []) 
		if x['type'] == 'photo']
	return pic_cut.getCutImages(raw, image_limit)

def get(path, cap_limit = 1000, text_limit = 4000, img_limit = 9):
	tid = getTid(path)
	status = twitterApi.get_status(tid)
	imgs = getImages(status, img_limit)
	cap = getCap(status, path, cap_limit if imgs else text_limit)
	return imgs, cap
