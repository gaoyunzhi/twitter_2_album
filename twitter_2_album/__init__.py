#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'twitter_2_album'

import yaml
from telegram_util import AlbumResult as Result
from telegram_util import compactText
import tweepy
import json
import html

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

def getCap(status):
	text = list(status.full_text)
	for x in status.entities.get('media', []):
		for pos in range(x['indices'][0], x['indices'][1]):
			text[pos] = ''
	text = html.unescape(''.join(text))
	text = compactText(text)
	return text

def getEntities(status):
	try:
		return status.extended_entities
	except:
		return status.entities

def getImgs(status):
	if not status:
		return []
	# seems video is not returned in side the json, there is nothing we can do...
	return [x['media_url'] for x in getEntities(status).get('media', [])
		if x['type'] == 'photo']


def getQuoteImgs(status):
	try:
		status.quoted_status
	except:
		return []
	return getImgs(status.quoted_status)

def get(path):
	tid = getTid(path)
	status = twitterApi.get_status(tid, tweet_mode="extended")
	r = Result()
	r.imgs = getImgs(status) or getQuoteImgs(status)
	r.cap = getCap(status)
	return r
