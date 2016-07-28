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
from Extractor.new_url_processing import del_all_urls
from Extractor.new_url_processing import del_url
from Extractor.new_url_processing import add_url_in_db
from Extractor.new_url_processing import update_url_in_db
from Extractor.new_url_processing import is_feature_in_db

#################################### MAIN #####################################
# Variables
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls
benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
malicious_urls_addr = '/home/avl/MSc-project/Crawler/malwaredomains-raw-recent'


def main_benign():
    METHOD = 'urllib2' # 'Selenium' or 'urllib2'
    UA = 'firefox' # 'firefox' or None       
    urls_to_analyse = urls_from_crawler(benign_urls_addr)
    
    t = time.time()
    cpt_benign = 0    
    print("Starting benign extraction...")
    
    for u in urls_to_analyse:
        
        cpt_benign += 1
        s1 = ''
        if cpt_benign%50 == 0:
            s1 = "\n Time elapsed: "+str(time.time() - t)+"\n"            
        s =s1+str(cpt_benign)+ " - "
        print s,
        
        url = URL(u, url_type = 'Benign')
        check = 1
        if is_in_db(u, db_urls):
            check = has_new_features_to_add(url, db_urls)   # check = 0 if no new features
                                                            #         1 else
            if check == True:
                if is_in_db(u, db):
                    RELOAD = not(check_field_value_in_url(u, 'user_agent', UA, db_urls) and check_field_value_in_url(u, 'method', METHOD, db_urls)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA)
                    update_url_in_db(url, db_urls, to_recompute = RELOAD)
                else:
                    url.process(method = METHOD, user_agent = UA)
                    add_url_in_db(url, db_urls)
            else:
                print "URL: "+u+" already stored and not modified."
        else:
            url.process(method = METHOD, user_agent = UA)
            add_url_in_db(url, db_urls)
        
                
################################### PRINT #####################################
def print_db():
    print "\n--------------------------------------------------------"
    print "Database"
    for document in db_urls.find():
        print "--------------------------------------------------------\n"
        pprint(document)
        print ""

def print_count(b, m):
    print "--------------------------------------------------------"
    print "Count in database:\n"
    print "> Benign items:    "+str(b)
    print "> Malicious items: "+str(m)
    print "--------------------------------------------------------\n"

def print_features():
    print "--------------------------------------------------------"
    print "Features:\n"
    print ">",
    feats = ue.features_names(db_urls)['Dynamic']
    for f in feats:
        print " "+f,
    print "\n--------------------------------------------------------\n"


################################### TESTS #####################################
def test1():
    print is_in_db('http://www.google.co.uk/', db_urls)
    print is_in_db('http://www.google.co.uk', db_urls)
    print is_in_db('http://google.co.uk/', db_urls)
    print is_in_db('http://google.co.uk', db_urls)

def test2():
    u = 'http://google.co.uk'
    pprint(get_feature_names_url(u, db_urls))

def test_add_url():
    url_name = 'http://google.co.uk'
    METHOD = 'urllib2'
    UA = 'firefox'
    url = URL(url_name, url_type = 'Benign')
    url.process(method = METHOD, user_agent = UA)
    add_url_in_db(url, db_urls)
    print_db()
    del_url(url_name, db_urls)

def test_is_feature_in_db():
    url_name = 'http://google.co.uk'
    METHOD = 'urllib2'
    UA = 'firefox'
    url = URL(url_name, url_type = 'Benign')
    url.process(method = METHOD, user_agent = UA)
    add_url_in_db(url, db_urls)
    assert is_feature_in_db('http://google.co.uk', 'letter_count', 'static', db_urls)
    del_url(url_name, db_urls)   
    
def test_is_not_feature_in_db():
    url_name = 'http://google.co.uk'
    METHOD = 'urllib2'
    UA = 'firefox'
    url = URL(url_name, url_type = 'Benign')
    url.process(method = METHOD, user_agent = UA)
    add_url_in_db(url, db_urls)
    assert not is_feature_in_db('http://google.co.uk', 'blablablabla', 'static', db_urls)
    del_url(url_name, db_urls)

def test_update():
    url_name = 'http://google.co.uk'
    METHOD = 'urllib2'
    UA = 'firefox'
    url = URL(url_name, url_type = 'Benign')
    url.process(method = METHOD, user_agent = UA)
    update_url_in_db(url, db_urls, to_recompute = False)
    print_db()
    del_url(url_name, db_urls)

def test_del():
    url_name = 'http://google.co.uk'
    METHOD = 'urllib2'
    UA = 'firefox'
    url = URL(url_name, url_type = 'Benign')
    url.process(method = METHOD, user_agent = UA)
    # add_url_in_db(url, db_urls)
    update_url_in_db(url, db_urls, to_recompute = False)

if __name__=='__main__':
    #del_all_urls(db_urls)
    main_benign()
    #print_db()