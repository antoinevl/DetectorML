# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:50:08 2016

@author: avl
"""

# process
# Update url -----> Deleteeees
# Refactor Add url
# Logs
# Tests
#
# Selenium
# New features
# Re-Crawling
# Machine Learning part
# 

import numpy as np
from url import URL
from datetime import date
from base64 import b64encode
import time
from bson.json_util import dumps
#from pprint import pprint


# Return output of the form:
# {'features_names': <List of features names>,
#  'urls': [{'name': <String: url name>
#            'features_values': <List of features values>
#           }, 
#           { ... }, { ... }
#          ]
# }
def db_to_arranged_urls(collection):
    output = {}
    f_names = get_features_names(collection)
    len_f_names = len(f_names)
    output['features_names'] = f_names
    output['urls'] = []
    X = []
    y = []
    
    items = collection.find()
    for item in items:
        u = {}
        u['name'] = item['url']
        u['features_values'] = [0]*len_f_names
        
        sf_list = item['static_features'][0]
        df_list = item['dynamic_features'][0]        
        
        for sf in sf_list:
            try:
                u['features_values'][output['features_names'].index(sf)] = sf_list[sf]
            except:
                raise "Error in 'arranged_urls_from_db': no such feature exists."
                
        for df in df_list:
            try:
                u['features_values'][output['features_names'].index(df)] = df_list[df]
            except:
                raise "Error in 'arranged_urls_from_db': no such feature exists."
        if item['type'] == 'Malicious':
            u['target'] = 1 
        else:
            u['target'] = 0
        
        output['urls'].append(u)
        X.append(u['features_values'])
        y.append(u['target'])
        
    output['X'] = X
    output['y'] = y
    return output
    
def get_features_names(collection):
    items = collection.find()
    f_names = []
    for item in items:
        names = {'Static':[],'Dynamic':[], 'All':[]}
        for i in item['static_features'][0]:
            names['Static'].append(i)
        for i in item['dynamic_features'][0]:
            names['Dynamic'].append(i)
        features_names = np.concatenate((names['Static'], names['Dynamic']))
    for f in features_names:
        if not f in f_names:
            f_names.append(f)
    return f_names
    
def get_features_length(collection):
    return len(get_features_names(collection))


# Returns a list of all the urls in the collection
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
    
# Returns whether a url is in db or not
def is_in_db(url_name, collection):
    try:
        collection.find({"url":url_name}).limit(1).next()
    except:
        return False
    else:
        return True

# Returns whether an url stored in the db needs to be added new features
def has_new_features_to_add(url_name, collection):
    u = URL(url_name)
    feat_names_url = u.get_feature_names()
    feat_names_db = get_feature_names(url_name, collection)
    res = sorted(feat_names_url['All']) == sorted(feat_names_db['All'])
    return res

# Returns collection of feature names for an url in the db
def get_feature_names_url(url_name, collection):
    item = collection.find({"url":url_name}).limit(1).next()
    names = {'Static':[],'Dynamic':[], 'All':[]}
    for i in item['static_features'][0]:
        names['Static'].append(i)
    for i in item['dynamic_features'][0]:
        names['Dynamic'].append(i)
    names['All'] = np.concatenate((names['Static'], names['Dynamic']))
    return names

# Returns whether a certain field has a certain value for a certain url
def check_field_value_in_url(url_name, field_name, value, collection):
    try:
        collection.find({"url":url_name, field_name:value}).limit(1).next()
    except:
        return False
    else:
        return True


# Returns the value of a certain field from a certain url
def get_field_from_url(url_name, field_name, collection):
    try:
        item = collection.find({"url":url_name}).limit(1).next()
    except:
        raise "Error in 'get_field_from_url': no such url in the database."
    else:
        return item[field_name]

# Update fields of an url (of Class URL) in the db
# Updates existing fields if to_recompute == True
def update_url_in_db(url, collection, to_recompute = False):
    if to_recompute == True:
        add_url_in_db(url, collection)
    else:
        s_features = url.static_features()
        d_features = url.dynamic_features()
        s_features_to_add = {}
        d_features_to_add = {}
        
        # Get features that are not present in the db
        for sf in s_features:
            if not is_feature_in_db(url.name, sf, 'static', collection):
                s_features_to_add[sf] = s_features[sf]
        for df in d_features:
            if not is_feature_in_db(url.name, df, 'dynamic', collection):
                d_features_to_add[df] = d_features[df]

        # Update these features
        update_dict_features(url.name, s_features_to_add, 'static', collection)
        update_dict_features(url.name, d_features_to_add, 'dynamic', collection)
        
        # Get features that are present in the db but not in the URL class
        # in order to remove them from the db
        features_in_db = get_feature_names_url(url.name, collection)
        features_in_URL = url.get_feature_names()
        
        features_to_remove_from_db = {'Static':[],'Dynamic':[], 'All':[]}
        for sf in features_in_db['Static']:
            if not sf in features_in_URL['Static']:
                features_to_remove_from_db['Static'].append(sf)
        for df in features_in_db['Dynamic']:
            if not df in features_in_URL['Dynamic']:
                features_to_remove_from_db['Dynamic'].append(df)
                
        # Remove these features from the db
        del_list_features(url.name, features_to_remove_from_db['Static'], 'static', collection)
        del_list_features(url.name, features_to_remove_from_db['Dynamic'], 'dynamic', collection)
        
        update_field(url.name, 'last_modified', today_dmy(), collection)
        
        print "URL: "+url.name+" updated into the database."
    
def add_url_in_db(url, collection):
    result = []
    url_name = url.name
    url_type = url.type
    url_description = url.description
    url_code = url.code
    dic_collection = collection.find_one({"url":url_name})
    if (dic_collection != None):
        print("URL: "+url_name+" already stored in the collection.")
    elif (dic_collection == None) and (url_code != 200):
        print("URL: "+url_name+" not available (url_code "+str(url_code)+"). Won't be stored into the database.")
    else:
        s = {
                "url": url_name,
                "page_b64": b64encode(url.page),
                "description": url_description,
                "type": url_type,
                "code": url_code,
                "method":url.method,
                "user_agent": url.user_agent,
                "added_date": today_dmy(),
                "last_modified": today_dmy(),
                "static_features": [{
                }],
                "dynamic_features": [{
                }]
            }
        
        # Logs
        result.append(collection.insert_one(s))
        
        # Add features
        s_features = url.static_features()
        d_features = url.dynamic_features()
        # Static
        for sf in s_features:
            feature_name = sf
            feature_type = 'static'
            new_value = s_features[sf]      
            res = update_feature(url_name, feature_name, feature_type, new_value, collection)
            result.append(res) # Logs
        # Dynamic
        for df in d_features:
            feature_name = df
            feature_type = 'dynamic'
            new_value = d_features[df]      
            res = update_feature(url_name, feature_name, feature_type, new_value, collection) 
            result.append(res) # Logs
            
        print("URL: "+url_name+" added to the collection.")
    return result

# update/add a feature of a certain URL in the database
# feature_type is either 'static' or 'dynamic'
def update_feature(url_name, feature_name, feature_type, new_value, collection):
    # what type of feature to update
    if (feature_type == 'static'):
        s = 'static_features.0.'
    elif (feature_type == 'dynamic'):
        s = 'dynamic_features.0.'
    else:
        print "Error in 'update_feature': did not indicate if static or dynamic feature."
    s += feature_name
	
    # update in mongodb
    # update_date(url,collection)
    result = collection.update_one(
        {"url": url_name},
        {"$set": {s: new_value}})
        
    #print "Feature '"+feature_name+"' updated."
    return result

# Updates a dictionnary of features
def update_dict_features(url_name, dico, feature_type, collection):
    for i in dico:
        update_feature(url_name, i, feature_type, dico[i], collection)
    
# delete a feature in the database
# feature_type is either 'static' or 'dynamic'
def del_feature(url_name, feature_name, feature_type, collection):
	# what type of feature to delete
	if (feature_type == 'static'):
		s = 'static_features.0.'
	elif (feature_type == 'dynamic'):
		s = 'dynamic_features.0.'
	else:
		print "Error in 'del_feature': did not indicate if static or dynamic feature."
	s += feature_name
	
	# delete in mongodb
	result = collection.update({"url": url_name}, {'$unset': {s:1}}, multi=True)
	#result = collection.update({}, {'$unset': {s:1}}, multi=True)
	return result

# Deletes a dictionnary of features
def del_list_features(url_name, l, feature_type, collection):
    for i in l:
        del_feature(url_name, i, feature_type, collection)

# Returns whether a feature is present in the db or not for a certain url
def is_feature_in_db(url_name, feature_name, feature_type, collection):
    # what type of feature to update
    if (feature_type == 'static'):
        s = 'static_features'
    elif (feature_type == 'dynamic'):
        s = 'dynamic_features'
    else:
        print "Error in 'is_feature_in_db': did not indicate if static or dynamic feature."    

    try:
        item = collection.find({"url":url_name}).limit(1).next()
    except:
        raise "Error in 'is_feature_in_db': no such url in the database."
    else:
        if feature_name in item[s][0]:
            return True
        else:
            return False
    

# Outputs a string of the date
# Example: 101216 = 10th of December 2016
def today_dmy():
    return date.today().strftime('%d%m%y')
    
# Deletes all urls with letter_count == 0
def sanitize_db(collection):
    items = collection.find()
    for item in items:
        if (item['static_features'][0]['letter_count']==0):
            del_url(item['url'], collection)
            
# Deletes a certain url from the db        
def del_url(url_name, collection):
    collection.delete_many({'url':url_name})

# Deletes all the urls from the db
def del_all_urls(collection):
    collection.delete_many({})

# Updates a field of a url in the database
def update_field(url_name, field_name, field_value, collection):
	result = collection.update_one(
		{"url": url_name},
    		{"$set": {field_name: field_value}})
	return result
 
# Count urls in db that have type url_type
def count_type(url_type, collection):
    return collection.find({"type":url_type}).count()
