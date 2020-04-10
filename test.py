#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twitter_2_album
import yaml
from telegram.ext import Updater
import album_sender

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(-1001198682178)

def test(url, rotate=False):
	r = twitter_2_album.get(url)
	album_sender.send(chat, url, r, rotate = rotate)
	
if __name__=='__main__':
	test('https://twitter.com/iingwen/status/1248561211119034369?s=21')