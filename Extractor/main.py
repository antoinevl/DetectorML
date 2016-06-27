# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:30:31 2016

@author: avl
"""

import url_extractor as ue
from pymongo import MongoClient
from pprint import pprint


analysed_url = ue.URL('http://google.co.uk/')
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls

ue.insert_url(analysed_url.url_name, 'Test', 'Benign', analysed_url.static_features(), analysed_url.dynamic_features(), db_urls)
#update_feature(url_name, 'line_count', 'static', 999999, urls)
#del_feature(analysed_url.url_name, 'feat2', 'dynamic', urls)

print "\n--------------------------------------------------------"
print "Database"
for document in db_urls.find():
    print "--------------------------------------------------------\n"
    pprint(document)
    print ""