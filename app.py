#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import datetime

_url = 'http://eponyms.ossus.ch/XML/eponyms.json'
_author = 'ajyee'
_lang = 'en'
_target = 'eponyms-2.json'


class EponymAntique:
	
	def __init__(self, js):
		self.__dict__ = js
	
	@property
	def document(self):
		aa = self.added.split('/')
		added = datetime.date(int(aa[2]), int(aa[0]), int(aa[1]))
		main = {
			'type': 'main',
			'author': _author,
			'date': added.isoformat(),
			'localized': {
				_lang: {
					'title': self.name,
					'text': self.desc,
				}
			}
		}
		if self.id:
			main['_id'] = self.id
		if self.modified is not None:
			md = self.added.split('/')
			mod = datetime.date(int(md[2]), int(md[0]), int(md[1]))
			main['dateUpdated'] = mod.isoformat()
		if self.tags is not None and len(self.tags) > 0:
			main['tags'] = [t.lower() for t in self.tags]
		return main


def download():
	ret = requests.get(_url)
	return ret.json()


def convert(antiques):
	docs = [e.document for e in antiques]
	doc = {
		'date': datetime.date.today().isoformat(),
		'documents': docs,
	}
	return doc


def export(doc, to):
	with open(to, 'w', encoding='utf-8') as h:
		json.dump(doc, h)


def run():
	antiques = download()
	eponyms = []
	for atq in antiques:
		ep = EponymAntique(atq)
		eponyms.append(ep)
	docs = convert(eponyms)
	export(docs, _target)


if '__main__' == __name__:
	run()
