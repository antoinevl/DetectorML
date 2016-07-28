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

# Returns a list of all the urls in the collection
def get_all_urls_db(collection):
    urls = []
    items = collection.find()
    for item in items:
        urls.append(item['url'])
    return urls

# Returns whether a url is in db or not
def is_in_db(url_name, collection):
    return (url_name in get_all_urls_db(collection))

# Returns whether an url stored in the db needs to be added new features
def has_new_features_to_add(url_name, collection):
    u = URL(url_name)
    feat_names_url = u.get_feature_names()
    feat_names_db = get_feature_names(url_name, collection)
    return sorted(feat_names_url['All']) == sorted(feat_names_db['All'])

# Returns collection of feature names for an url in the db
def get_feature_names(url_name, collection):
    items = collection.find()
    for item in items:
        if item['url']==url_name:
            names = {'Static':[],'Dynamic':[], 'All':[]}
            for i in item['static_features'][0]:
                names['Static'].append(i)
            for i in item['dynamic_features'][0]:
                names['Dynamic'].append(i)
            names['All'] = np.concatenate((names['Static'], names['Dynamic']))
    return names

# Returns whether a certain field has a certain value for a certain url
def check_field_value_in_url(url_name, field_name, value, collection):
    return get_field_from_url(url_name, field_name, collection)==value

# Returns the value of a certain field from a certain url
def get_field_from_url(url_name, field_name, collection):
    items = collection.find()
    value = -1    
    for item in items:
        if item['url'] == url_name :
            value = item[field_name]
    return value

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
        features_in_db = get_feature_names(url.name, collection)
        features_in_URL = url.get_feature_names()
        
        features_to_remove_from_db = {'Static':[],'Dynamic':[], 'All':[]}
        for sf in features_in_db:
            if not sf in features_in_URL['Static']:
                features_to_remove_from_db['Static'].append(sf)   
        for df in d_features:
            if not df in features_in_URL['Dynamic']:
                features_to_remove_from_db['Dynamic'].append(df)        
        # Remove these features from the db
        for 
        
        
        update_field(url.name, 'last_modified', today_dmy(), collection)
    
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
        
    print "Feature '"+feature_name+"' updated."
    return result

# Updates a dictionnary of features
def update_dict_features(url_name, dico, feature_type, collection):
    for i in dico:
        update_feature(url_name, i, feature_type, dico[i], collection)
    
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

# Returns whether a feature is present in the db or not for a certain url
def is_feature_in_db(url_name, feature_name, feature_type, collection):
    # what type of feature to update
    if (feature_type == 'static'):
        s = 'static_features'
    elif (feature_type == 'dynamic'):
        s = 'dynamic_features'
    else:
        print "Error in 'is_feature_in_db': did not indicate if static or dynamic feature."    
    check = 0
    items = collection.find()
    for item in items:
        if feature_name in item[s][0]:
            check += 1
    return (check > 0)

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
    items = collection.find()
    for item in items:
        del_url(item['url'], collection)
        
def update_field(url_name, field_name, field_value, collection):
	result = collection.update_one(
		{"url": url_name},
    		{"$set": {field_name: field_value}})
	return result