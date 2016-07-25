# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:39:49 2016

@author: avl
"""

import base64
import Extractor.url_extractor as ue
from pymongo import MongoClient
from pprint import pprint
import time
import Crawler.mw_crawl as mwc
import Crawler.alexa_crawl as axc
from Crawler import crawler
import Classifier.classification as cls

from sklearn import cross_validation
from sklearn import svm

# Variables
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls
benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
malicious_urls_addr = '/home/avl/MSc-project/Crawler/malwaredomains-raw-recent'


def main_benign():
    
    METHOD = 'Selenium'
    UA = 'firefox'        
    urls_to_analyse = crawler.urls_from_crawler(benign_urls_addr)
    
    for u in urls_to_analyse():
        check = 1
        if is_in_db(u, db):
            check = has_new_features_to_add(url) # check = 0 if no new features
                                                 #         1 else
            if check == 1:
                if is_in_db(u, db):
                    url = URL_from_db(u) # url of type URL
                    RELOAD = not(has_ua_in_db(url, UA, db) and has_method_in_db(url, METHOD, db)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA)
                    update_url(url, db)
                else:
                    url = URL(u)
                    url.process(method = METHOD, user_agent = UA)
                    add_url(url, db)