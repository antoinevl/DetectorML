#!/usr/bin/env python
import urllib2
import static_extractor as se
import dynamic_extractor as de

class URL:
    #url_name = 'http://www.google.com/'
    #resp = urllib2.urlopen(url_name)
    #page = resp.read()

    def __init__(self, url):
        self.url_name = url
        self.page = process_request(url)['page']
        self.code = process_request(url)['code']
                               
    script_token_start = "<script>"
    script_token_end = "</script>"

    def js(self):
        javascript = []
        ind_start = 0
        while (self.page.find(self.script_token_start, ind_start)!=-1):
        	ind_start = self.page.find(self.script_token_start, ind_start) + len(self.script_token_start)
        	ind_end = self.page.find(self.script_token_end, ind_start)
        	javascript.append(self.page[ind_start:ind_end])
        	ind_start = ind_end
        return javascript
    
    def static_features(self):
        static_features = {}
        static_features['letter_count'] = se.letter_count(self.page)
        static_features['word_count'] = se.word_count(self.page)
        static_features['line_count'] = se.line_count(self.page)
        return static_features
        
    def dynamic_features(self):
        dynamic_features = {}
        dynamic_features['feat1'] = de.feature1(self.page)
        return dynamic_features

def process_request(url):
    output = {}
    req = urllib2.Request(url)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        output['code'] = e.code
        output['page'] = ''
    except urllib2.URLError as e:
        output['code'] = -1
        output['page'] = ''
    except:
        output['code'] = -1
        output['page'] = ''
    else:
        page = resp.read()
        output['page'] = page
        output['code'] = 200
    return output  
    

def insert_url(url_name, code, description, url_type, static_features_dic, dynamic_features_dic, collection):
	dic_collection = collection.find_one({"url":url_name})
	if (dic_collection != None) and (code==200):
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
			type
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
	elif (dic_collection != None) and (code!=200):
         print("URL: "+url_name+" not available. Won't be stored into the database.")
	else:
		s = {
			"url": url_name,
			"description": description,
			"type": url_type,
			"static_features": [{
				"line_count": static_features_dic['line_count'],
				"word_count": static_features_dic['word_count'],
				"letter_count": static_features_dic['letter_count']
			}],
			"dynamic_features": [{
				"feat1": 0
			}]
		     }

		result = collection.insert_one(s)
		print("URL: "+url_name+" added to the collection.")
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


# delete a feature in the database
# feature_type is either 'static' or 'dynamic'
def del_feature(feature_name, feature_type, collection):
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

def add_field(url, field_name, field_value, collection):
	result = collection.update_one(
		{"url": url},
    		{"$set": {field_name: field_value}})
	return result
 
def add_field_all(field_name, field_value, collection):
    urls = get_all_urls_db(collection)
    for url in urls:
        add_field(url, field_name, field_value, collection)
    return 1
    
def del_field_all(url, field_name, collection):
    result = collection.update({}, {'$unset': {field_name:1}}, multi=True)
    return result
    
def get_all_urls_db(collection):
    urls = []
    items = collection.find()
    for item in items:
        urls.append(item['url'])
    return urls

def get_benign_urls_db(collection):
    urls = []
    items = collection.find()
    for item in items:
        if item['type']=='Benign':
            urls.append(item['url'])
    return urls
    
def get_malicious_urls_db(collection):
    urls = []
    items = collection.find()
    for item in items:
        if item['type']=='Malicious':
            urls.append(item['url'])
    return urls

def del_url(url_name, collection):
    collection.delete_many({'url':url_name})
    
# Deletes all urls with letter_count == 0
def sanitize_db(collection):
    items = collection.find()
    for item in items:
        if (item['static_features'][0]['letter_count']==0):
            del_url(item['url'], collection)

def count(url_type, collection):
    if url_type == 'Benign':
        return len(get_benign_urls_db(collection))
    if url_type == 'Malicious':
        return len(get_malicious_urls_db(collection))
            