#!/usr/bin/env python

import urllib2

url_name = 'http://www.google.com/'

resp = urllib2.urlopen(url_name)
page = resp.read()


# Extract Javascript between tokens <script></script>
script_token_start = "<script>"
script_token_end = "</script>"

javascript = []
ind_start = 0
while (page.find(script_token_start, ind_start)!=-1):
	ind_start = page.find(script_token_start, ind_start) + len(script_token_start)
	ind_end = page.find(script_token_end, ind_start)
	javascript.append(page[ind_start:ind_end])
	ind_start = ind_end

# Extract static features
static_features = {}

lines = page.splitlines()
static_features['line_count'] = len(lines)

letter_count = 0
for line in lines:
	letter_count += len(line)
static_features['letter_count'] = letter_count

word_count = 0
for line in lines:
	word_count += len(line.split())
static_features['word_count'] = word_count

# Extract dynamic features
dynamic_features = {}
dynamic_features['feat1'] = 0
dynamic_features['feat2'] = 0

# Save in database
from pymongo import MongoClient
client = MongoClient()
db = client.projectDB
urls = db.urls

def insert_url(url_name, description, url_type, static_features_dic, dynamic_features_dic, collection):
	if len(collection.find_one({"url":url_name}))>2:
		print("URL: "+url_name+" already stored in the collection.")
	else:
		s = {
			"url": url_name,
			"description": description,
			"type": url_type,
			"static_features": [{
				"line_count": static_features['line_count'],
				"word_count": static_features['word_count'],
				"letter_count": static_features['letter_count']
			}],
			"dynamic_features": [{
				"feat1": 0,
				"feat2": 0
			}]
		     }

		result = collection.insert_one(s)
		print("URL added to the collection.")
		return result

insert_url(url_name, 'Test', 'Benign', static_features, dynamic_features, urls)
