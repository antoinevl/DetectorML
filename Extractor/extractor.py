#!/usr/bin/env python

import urllib2

url_name = 'http://www.google.com/'

resp = urllib2.urlopen(url_name)
page = resp.read()


#--- Extract Javascript between tokens <script></script>
script_token_start = "<script>"
script_token_end = "</script>"

javascript = []
ind_start = 0
while (page.find(script_token_start, ind_start)!=-1):
	ind_start = page.find(script_token_start, ind_start) + len(script_token_start)
	ind_end = page.find(script_token_end, ind_start)
	javascript.append(page[ind_start:ind_end])
	ind_start = ind_end

#--- Extract static features
static_features = {}

#-- line count
lines = page.splitlines()
static_features['line_count'] = len(lines)

#-- letter count
letter_count = 0
for line in lines:
	letter_count += len(line)
static_features['letter_count'] = letter_count

#-- word count
word_count = 0
for line in lines:
	word_count += len(line.split())
static_features['word_count'] = word_count

#--- Extract dynamic features
dynamic_features = {}
dynamic_features['feat1'] = 0
dynamic_features['feat2'] = 0
dynamic_features['feat3'] = 2
dynamic_features['feat4'] = 2
dynamic_features['feat5'] = 2
dynamic_features['feat7'] = 2
dynamic_features['feat8'] = 2


#--- Save in database
from pymongo import MongoClient

def insert_url(url_name, description, url_type, static_features_dic, dynamic_features_dic, collection):
	dic_collection = collection.find_one({"url":url_name})
	if (dic_collection != None):
		print("URL: "+url_name+" already stored in the collection.")

		# Add features if they are not present in the database
		added_static_features = []
		added_dynamic_features = []		
		
		for feat in static_features_dic:
			list_static = dic_collection["static_features"]
			for i in xrange(len(list_static)):
				if not (feat in list_static[i]):
					update_feature(url_name, feat, 'static', static_features_dic[feat], collection)
					added_static_features.append(feat)

		for feat in dynamic_features_dic:
			list_dynamic = dic_collection["dynamic_features"]
			for i in xrange(len(list_dynamic)):
				if not (feat in list_dynamic[i]):
					update_feature(url_name, feat, 'dynamic', dynamic_features_dic[feat], collection)
					added_dynamic_features.append(feat)
			
		if len(added_static_features)>0:
			s = "Added static features: "
			for f in added_static_features:
				s += f
				s += ","
			s = s[:-1]+"."
			print s
		if len(added_dynamic_features)>0:
			s = "Added dynamic features: "
			for f in added_dynamic_features:
				s += f
				s += ","
			s = s[:-1]+"."
			print s
		if len(added_dynamic_features) == 0 and len(added_static_features) == 0:
			print "No new added features."
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

# update/add a feature of a certain URL in the database
# feature_type is either 'static' or 'dynamic'
def update_feature(url, feature_name, feature_type, new_value, collection):
	# what type of feature to update
	if (feature_type == 'static'):
		s = 'static_features.0.'
	elif (feature_type == 'dynamic'):
		s = 'dynamic_features.0.'
	else:
		print "Error in 'update_feature': did not indicate if static or dynamic feature."
	s += feature_name
	
	# update in mongodb
	result = collection.update_one(
		{"url": url},
    		{"$set": {s: new_value}})
	return result


# delete a feature of a certain URL in the database
# feature_type is either 'static' or 'dynamic'
def del_feature(url, feature_name, feature_type, collection):
	# what type of feature to delete
	if (feature_type == 'static'):
		s = 'static_features.0.'
	elif (feature_type == 'dynamic'):
		s = 'dynamic_features.0.'
	else:
		print "Error in 'del_feature': did not indicate if static or dynamic feature."
	s += feature_name
	
	# delete in mongodb
	result = collection.update({}, {'$unset': {s:1}}, multi=True)
	return result

# Process
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
urls = db.urls

insert_url(url_name, 'Test', 'Benign', static_features, dynamic_features, urls)
#update_feature(url_name, 'line_count', 'static', 999999, urls)
#del_feature(url_name, 'new_feature', 'static', urls)

for document in urls.find():
	print document

