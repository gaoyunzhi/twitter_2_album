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

prefix = 'https://m.twitter.cn/statuses/show?id='

def getWid(path):
	index = path.find('?')
	if index > -1:
		path = path[:index]
	return path.split('/')[-1]

def getCap(json, path, cap_limit):
	text = json['text']
	b = BeautifulSoup(text, features="lxml")
	for elm in b.find_all('a'):
		if not elm.get('href'):
			continue
		md = '[%s](%s)' % (elm.text, elm['href'])
		elm.replaceWith(BeautifulSoup(md, features='lxml').find('p'))
	suffix = ' [%s](%s)' % (json['user']['screen_name'], path)	
	return cutCaption(
		BeautifulSoup(str(b).replace('<br/>', '\n'), features='lxml').text.strip(), 
		suffix, cap_limit)

def getImages(json, image_limit):
	raw = [x['url'] for x in json['pics']]
	return pic_cut.getCutImages(raw, image_limit)

def get(path, cap_limit = 1000, text_limit = 4000, img_limit = 9):
	wid = getWid(path)
	try:
		json = yaml.load(cached_url.get(prefix + wid), Loader=yaml.FullLoader)
	except:
		return [], ''
	json = json['data']
	imgs = getImages(json, img_limit)
	cap = getCap(json, path, cap_limit if imgs else text_limit)
	return imgs, cap

	

