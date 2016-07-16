# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:30:31 2016

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
# Variables
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls
benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
malicious_urls_addr = '/home/avl/MSc-project/Crawler/malwaredomains-raw-recent'

#print ue.add_field('http://google.co.uk', 'date', '20160628',db_urls)
#print ue.get_urls_db(db_urls)
#print ue.add_field_all('date', '20160628',db_urls)
#update_feature(url_name, 'line_count', 'static', 999999, urls)
#del_feature(analysed_url.url_name, 'feat2', 'dynamic', urls)

# Insert benign urls
def main_benign():
    t = time.time()
    print("Starting benign extraction...")
    with open(benign_urls_addr, 'r') as f:
        cpt_benign = 0
        analysed_urls = f.read().splitlines()
        for u in analysed_urls:
            cpt_benign += 1
            s1 = ''
            if cpt_benign%50 == 0:
                s1 = "\n Time elapsed: "+str(time.time() - t)+"\n"            
            s =s1+str(cpt_benign)+ " - "
            print s,
            analysed_url = ue.URL(u, 'firefox')
            result = ue.insert_url(analysed_url.url_name, analysed_url.code,'', 'Benign', analysed_url.static_features(), analysed_url.dynamic_features(), db_urls)
    return result

# Insert malicious urls
def main_malicious():
    t = time.time()
    print("Starting malicious extraction...")
    with open(malicious_urls_addr, 'r') as f:
        cpt_malicious = 0
        lines = f.read().splitlines()
        
        # u = URL ;
        # ip = IP
        # t = malicious type ; 
        # src = malicious source ; 
        # d = date ; 
        # p_b64 = page encode in base64
        for line in lines:
            u = line.split()[0]
            ip = line.split()[1]
            t = line.split()[2]
            src = line.split()[3]
            d = line.split()[4]
            cpt_malicious += 1
            
            analysed_url = ue.URL(u, 'firefox')
            # If malicious page already in the database:           
            try:
                p_b64 = ue.get_field_from_url(u, 'page_b64', db_urls)
                analysed_url.set_page(base64.b64decode(p_b64))
                c = ue.get_field_from_url(u, 'code', db_urls)
                analysed_url.set_code(base64.b64decode(c))
            except:
                p_b64 = base64.b64encode(analysed_url.page)
                c = analysed_url.code
                        
            result = ue.insert_url(analysed_url.url_name, analysed_url.code,'', 'Malicious', analysed_url.static_features(), analysed_url.dynamic_features(), db_urls)
            ue.add_field(u, 'code', c, db_urls) 
            ue.add_field(u, 'ip', ip, db_urls)
            ue.add_field(u, 'page-b64', p_b64, db_urls)            
            ue.add_field(u, 'malicious-type', t, db_urls)
            ue.add_field(u, 'malicious-source', src, db_urls)
            ue.add_field(u, 'date', d, db_urls)
            
    return result

def print_db():
    print "\n--------------------------------------------------------"
    print "Database"
    for document in db_urls.find():
        print "--------------------------------------------------------\n"
        pprint(document)
        print ""

def print_count(b, m):
    print "\n--------------------------------------------------------"
    print "Count:"
    print "> Benign items:    "+str(b)
    print "> Malicious items: "+str(m)
    print "--------------------------------------------------------\n"


#for document in db_urls.find():
#    print ue.get_field_from_url(document['url'], 'type', db_urls)


## Here we go!

## Crawl
mwc.crawl_mwd()
#axc.crawl()

## Extract
#main_benign()
#main_malicious()
#ue.sanitize_db(db_urls)
#print_db()
c_benign = ue.count('Benign', db_urls)
c_malicious = ue.count('Malicious', db_urls)
print_count(c_benign, c_malicious)

#print_db()

### Machine Learning
## Create dataset
        #ue.update_feature_all('feat1','static',1,db_urls)
        #ue.update_feature_all('feat1','dynamic',1,db_urls)

#dataset = ue.db_to_dataset(db_urls)

## Shuffle the dataset
#dataset = cls.shuffle_dataset(dataset)

## 10-cross-fold validation
#X_train, X_test, y_train, y_test = cross_validation.train_test_split(dataset['data'], dataset['target'], test_size=0.4, random_state=0)
#clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
#score = clf.score(X_test, y_test)

#print "Score: "+str(score)