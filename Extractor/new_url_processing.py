# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:50:08 2016

@author: avl
"""




# process
# Update url
# Refactor Add url
# Logs
# Tests
#
# Selenium
# New features
# Re-Crawling
# Machine Learning part
# 
#
#
#


import numpy as np
from Extractor.url import URL

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

# Returns collection of feature names for an url
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
def update_url_in_db(to_recompute = False, url, db):
    if to_recompute == True:
        add_url_in_db()
    return 1
    
def add_url_in_db(url, db):
    result = []
    url_name = url.name
    dic_collection = collection.find_one({"url":url_name})
    if (dic_collection != None):
        print("URL: "+url_name+" already stored in the collection.")
    elif (dic_collection == None) and (code != 200):
        print("URL: "+url_name+" not available (code "+str(code)+"). Won't be stored into the database.")
    else:
        s = {
                "url": url_name,
                "description": description,
                "type": url_type,
                "method":url.method,
                "user_agent": url.user_agent,
                "date": today_dmy(),
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
    update_date(url,collection)
    result = collection.update_one(
        {"url": url},
        {"$set": {s: new_value}})
        
    print "Feature: "+feature_name+" updated."
    return result


def today_dmy():
    return date.today().strftime('%d%m%y')