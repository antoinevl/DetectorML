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

import Classifier.classification as cls

from sklearn import cross_validation
from sklearn import svm

from Crawler.crawler import urls_from_crawler
from Extractor.new_url_processing import is_in_db
from Extractor.new_url_processing import has_new_features_to_add
from Extractor.url import URL

from Extractor.new_url_processing import get_feature_names as get_feature_names_url
from Extractor.new_url_processing import check_field_value_in_url



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
    urls_to_analyse = urls_from_crawler(benign_urls_addr)
    
    for u in urls_to_analyse():
        check = 1
        if is_in_db(u, db_urls):
            url = URL(u)
            check = has_new_features_to_add(url, db_urls)   # check = 0 if no new features
                                                            #         1 else
            if check == True:
                if is_in_db(u, db):
                    RELOAD = not(check_field_value_in_url(u, 'user_agent', UA, db_urls) and check_field_value_in_url(u, 'method', METHOD, db_urls)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA)
                    update_url_in_db(to_recompute = RELOAD, url, db)
                else:
                    url.process(method = METHOD, user_agent = UA)
                    add_url_in_db(url, db)

def test1():
    print is_in_db('http://www.google.co.uk/', db_urls)
    print is_in_db('http://www.google.co.uk', db_urls)
    print is_in_db('http://google.co.uk/', db_urls)
    print is_in_db('http://google.co.uk', db_urls)

def test2():
    u = 'http://google.co.uk'
    pprint(get_feature_names_url(u, db_urls))

if __name__=='__main__':
    test2()