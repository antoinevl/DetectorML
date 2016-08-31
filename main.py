# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:39:49 2016

@author: avl
"""

import signal

from pymongo import MongoClient
from pprint import pprint
import time
import Crawler.mw_crawl as mwc
import Crawler.alexa_crawl as axc

from Classifier.classification import svm_clf,cross_validation_scores, dtree_clf

from sklearn import cross_validation
from sklearn import svm
from sklearn.externals import joblib

from Crawler.crawler import urls_from_crawler
from Crawler.crawler import get_fields_from_malicious_file
from Crawler.mw_crawl import crawl as malicious_crawl

from Extractor.url_processing import is_in_db
from Extractor.url_processing import has_new_features_to_add
from Extractor.url import URL

from Extractor.url_processing import get_feature_names_url
from Extractor.url_processing import check_field_value_in_url
from Extractor.url_processing import del_all_urls, del_malicious_urls
from Extractor.url_processing import del_url
from Extractor.url_processing import add_url_in_db
from Extractor.url_processing import update_url_in_db
from Extractor.url_processing import is_feature_in_db
from Extractor.url_processing import update_field
from Extractor.url_processing import get_all_urls_db
from Extractor.url_processing import get_benign_urls_db
from Extractor.url_processing import get_malicious_urls_db
from Extractor.url_processing import sanitize_db
from Extractor.url_processing import count_type as count_db
from Extractor.url_processing import get_field_from_url
from Extractor.url_processing import db_to_arranged_urls

import matplotlib.pyplot as plt
import numpy as np

################################## MAIN #####################################

t0 = time.time()

# Variables
vm_url = '146.169.47.251'
db_port = 27017
client = MongoClient(vm_url, db_port)
db = client.projectDB
db_urls = db.urls
benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
malicious_urls_addr = '/home/avl/MSc-project/Crawler/mwlist_all'

# Statistic variables
setup_t = time.time()-t0

# Handler for the timeout
def handler(signum, frame):
    print "Crawling time deseperately too long... Let's crawl another one."
    raise Exception("Timeout")
signal.signal(signal.SIGALRM, handler)

def main_benign():    
    
    METHOD = 'Selenium' # 'Selenium' or 'urllib2'
    UA = 'firefox' # 'firefox' or None       
    urls_to_analyse = urls_from_crawler(benign_urls_addr)
    
    cpt_benign = 0    
    print("Starting benign extraction...")
    
    urls_list = get_all_urls_db(db_urls)       
    
    for u in urls_to_analyse:
        ## Statistic variables / printing
        ##> Counting and printing
        cpt_benign += 1      
        s = str(cpt_benign)+ " - "
        print s,
        ##> Time
        t_crawl_start = time.time()
        
        
        # Set handler and timeout
        signal.alarm(20)
        try: 
            # Now we start doing the real stuff        
            url = URL(u, url_type = 'Benign')
    
            check_url_in_list = u in urls_list
            if check_url_in_list:
                check = has_new_features_to_add(u, db_urls)   # check = 0 if no new features
                                                                #         1 else
                if check == True:
                    RELOAD = not(check_field_value_in_url(u, 'user_agent', UA, db_urls) and check_field_value_in_url(u, 'method', METHOD, db_urls)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA, collection = db_urls)
                    update_url_in_db(url, db_urls, to_recompute = RELOAD)
                else:
                    print "URL '"+u+"' already stored and not modified."
            else:
                url.process(method = METHOD, user_agent = UA)
                add_url_in_db(url, db_urls)
                
                ## Statistics
                crawl_time = time.time()-t_crawl_start
                update_field(url.name, 'stat_crawling_time', crawl_time, db_urls)
        except Exception, exc:
            print exc
            
def main_malicious():
    METHOD = 'Selenium' # 'Selenium' or 'urllib2'
    UA = 'firefox' # 'firefox' or None      
    malicious_fields_lines = get_fields_from_malicious_file(malicious_urls_addr)
    
    cpt_malicious = 0    
    print("Starting malicious extraction...")
     
    urls_list = get_all_urls_db(db_urls)  
    
    
    for l in malicious_fields_lines:

        u = l['url_name']
        
        ## Statistic variables / printing
        ##> Counting and printing
        cpt_malicious += 1      
        s = str(cpt_malicious)+ " - "
        print s,
        ##> Time
        t_crawl_start = time.time()
        
        # Set handler and timeout
        signal.alarm(20)
        try:        
            # Now we start doing the real stuff 
            url = URL(u, url_type = 'Malicious')   
            check_url_in_list = u in urls_list
            if check_url_in_list:
                check = has_new_features_to_add(u, db_urls)     # check = 0 if no new features
                                                                #         1 else
                if check == True:
                    RELOAD = not(check_field_value_in_url(u, 'user_agent', UA, db_urls) and check_field_value_in_url(u, 'method', METHOD, db_urls)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA, collection = db_urls)
                    update_url_in_db(url, db_urls, to_recompute = RELOAD)
                else:
                    print "URL '"+u+"' already stored and not modified."
            else:
                url.process(method = METHOD, user_agent = UA)
                add_url_in_db(url, db_urls)
                update_field(url.name, 'malicious_type', l['malicious_type'], db_urls)
                update_field(url.name, 'malicious_src', l['malicious_src'], db_urls)
                update_field(url.name, 'ip', l['ip'], db_urls)
                urls_list.append(u)
                 
                ## Statistics
                crawl_time = time.time()-t_crawl_start
                update_field(url.name, 'stat_crawling_time', crawl_time, db_urls)
                
        except Exception, exc:
            print exc
        
################################# PRINT #####################################
def print_db():
    print "\n--------------------------------------------------------"
    print "Database"
    for document in db_urls.find():
        print "--------------------------------------------------------\n"
        pprint(document)
        print ""

def print_count():
    c_benign = count_db('Benign', db_urls)
    c_malicious = count_db('Malicious', db_urls)
    print "--------------------------------------------------------"
    print "Count in database:\n"
    print "> Benign items:    "+str(c_benign)
    print "> Malicious items: "+str(c_malicious)
    print "--------------------------------------------------------\n"

################################# STATS #####################################    
def plot_distribution_crawling_times():
    x_benign_urls = get_benign_urls_db(db_urls)
    x_malicious_urls = get_malicious_urls_db(db_urls)
    
    y_benign = []
    y_malicious = []
    
    
    for i in range(len(x_benign_urls)):
        y_benign.append(get_field_from_url(x_benign_urls[len(x_benign_urls)-i-1],'stat_crawling_time',db_urls))
    
    for i in range(len(x_malicious_urls)):
        y_malicious.append(get_field_from_url(x_malicious_urls[len(x_malicious_urls)-i-1],'stat_crawling_time',db_urls))
    
    y_benign.sort()
    y_malicious.sort()
    
    print y_benign
    
    ind_max_benign = 0
    for i in xrange(len(y_benign)):
        if y_benign[i]>20 and ind_max_benign == 0:
            ind_max_benign = i
    
    ind_max_malicious = 0
    for i in xrange(len(y_malicious)):
        if y_malicious[i]>20 and ind_max_malicious == 0:
            ind_max_malicious = i    
    
    plt.figure(1)
    
    plt.title('Crawling times')    
    
    plt.subplot(211)
    plt.plot(y_benign[:ind_max_benign])
    plt.ylabel('Benign URLs')
    
    plt.subplot(212)
    plt.plot(y_malicious[:ind_max_malicious])
    plt.ylabel('Malicious URLs')   
    
    plt.show()

#plot_distribution_crawling_times()

def plot_hist_crawling_times():
    x_benign_urls = get_benign_urls_db(db_urls)
    x_malicious_urls = get_malicious_urls_db(db_urls)
    
    y_benign = []
    y_malicious = []
    
    
    for i in range(len(x_benign_urls)):
        y_benign.append(get_field_from_url(x_benign_urls[len(x_benign_urls)-i-1],'stat_crawling_time',db_urls))
    
    for i in range(len(x_malicious_urls)):
        y_malicious.append(get_field_from_url(x_malicious_urls[len(x_malicious_urls)-i-1],'stat_crawling_time',db_urls))
    
    y_benign.sort()
    y_malicious.sort()
    
    print y_benign
    
    ind_max_benign = 0
    for i in xrange(len(y_benign)):
        if y_benign[i]>20 and ind_max_benign == 0:
            ind_max_benign = i
    
    ind_max_malicious = 0
    for i in xrange(len(y_malicious)):
        if y_malicious[i]>20 and ind_max_malicious == 0:
            ind_max_malicious = i
    
    
    plt.figure(1)
    
    plt.title('Crawling times')    
    
    plt.subplot(211)
    plt.hist(y_benign[:ind_max_benign], 10)
    plt.ylabel('Benign URLs')
    
    plt.subplot(212)
    plt.hist(y_malicious[:ind_max_malicious], 10)
    plt.ylabel('Malicious URLs')   
    
    plt.show()
    
#plot_hist_crawling_times()    

################################# TESTS #####################################
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
    assert not is_feature_in_db('http://google import get_field_from_url.co.uk', 'blablablabla', 'static', db_urls)
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

def test_db_to_arranged_urls():
    res = db_to_arranged_urls(db_urls)
    print res['y']
    
    


#%
if __name__=='__main__':
    
    t_start = time.time()
#    del_all_urls(db_urls)
#    del_malicious_urls(db_urls)
    t = time.time()
#    malicious_crawl()
    t1 = time.time()
#    
#    # TODO implement sanitization of malicious urls
#    
#    main_benign()
    t2 = time.time()
#    main_malicious()
    t3 = time.time()    
#    sanitize_db(db_urls)
    t4 = time.time()
    print_count()
    
    
############################# ML ##############################################
    # Classifiers
    clf_svm = svm_clf()
    clf_dtree = dtree_clf() 
    
    # Load or compute X y
    to_reload_urls = False
    if to_reload_urls:
        arranged_urls = db_to_arranged_urls(db_urls)
        
        y = arranged_urls['y']
        X = arranged_urls['X']
        
        data = {'X':X, 'y':y}
        joblib.dump(data,"Dumps/data.pkl")
    else:
        data = joblib.load("Dumps/data.pkl")
        X = data['X']
        y = data['y']
    
    

    import csv
    
    with open("Dumps/X.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(X)
    
    with open("Dumps/y.csv", 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(y)
    

    
    
    
    t5 = time.time() 
    
    print "SVM Cross Validation:\n"     
    cross_validation_scores(X, y, clf_svm)
    
    t6 = time.time()
    
    print "Decision Tree Cross Validation:\n"     
    cross_validation_scores(X, y, clf_dtree)
    
    t7 = time.time()    
    
    print "\nSVM clf fitting...",
    clf_svm.fit(X,y)
    print "done.\n"
    
    t8 = time.time()
    
    print "Decision Tree clf fitting...",
    clf_dtree.fit(X,y)
    print "done.\n"
    
    joblib.dump(clf_svm,"Dumps/clf_svm.pkl")
    joblib.dump(clf_dtree,"Dumps/clf_dtree.pkl")
    
    t9 = time.time()
    print "Features gain:"
    f_names = joblib.load("Dumps/feat_names.pkl")
    clf_dtree = joblib.load("Dumps/clf_dtree.pkl")
    gains = clf_dtree.feature_importances_
    for i in xrange(len(f_names)):
        g = 100*gains[i]
        print("'"+f_names[i]+"': "),
        print("%.2f" % g)
        

###############################################################################    
#    print_db()
    
    print "\nSetup time: "+str(setup_t)+"."
    print "Time elapsed for 'del_all_urls': "+str(t-t_start)+"."
    print "Time elapsed for 'malicious_crawl': "+str(t1-t)+"."
    print "Time elapsed for 'main_benign': "+str(t2-t1)+"."
    print "Time elapsed for 'main_malicious': "+str(t3-t2)+"."
    print "Time elapsed for 'sanitize_db': "+str(t4-t3)+"."
    print "Time elapsed for 'db_to_arranged_urls': "+str(t5-t4)+"."
    print "Time elapsed for 'SVM cross_validation_scores': "+str(t6-t5)+"."
    print "Time elapsed for 'Decision Tree cross_validation_scores': "+str(t7-t6)+"."
    print "Time elapsed for 'SVM clf fitting time': "+str(t8-t7)+"."
    print "Time elapsed for 'Decision Tree clf fitting time': "+str(t9-t8)+"."
    

    
    