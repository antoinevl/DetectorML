# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:30:31 2016

@author: avl
"""

import url_extractor as ue
from pymongo import MongoClient
from pprint import pprint
import time


t = time.time()
print("Starting extraction...")

vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls


# Insert benign urls

benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
with open(benign_urls_addr, 'r') as f:
    cpt_benign = 0
    analysed_urls = f.read().splitlines()
    n = len(analysed_urls)
    for u in analysed_urls:
        cpt_benign += 1
        s1 = ''
        if cpt_benign%50 == 0:
            s1 = "\n Time elapsed: "+str(time.time() - t)+"\n"            
        s =s1+str(cpt_benign)+ " - "
        print s,
        analysed_url = ue.URL(u)
        ue.insert_url(analysed_url.url_name, analysed_url.code,'', 'Benign', analysed_url.static_features(), analysed_url.dynamic_features(), db_urls)
        #time.sleep(0)
#update_feature(url_name, 'line_count', 'static', 999999, urls)
#del_feature(analysed_url.url_name, 'feat2', 'dynamic', urls)

# Insert malicious urls


print "\n--------------------------------------------------------"
print "Database"
for document in db_urls.find():
    print "--------------------------------------------------------\n"
    pprint(document)
    print ""