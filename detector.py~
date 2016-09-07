# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:52:50 2016

@author: avl
"""

from sklearn.externals import joblib
from Extractor.url_processing import url_to_X
import time
from Crawler.crawler import urls_from_crawler
from Crawler.crawler import get_fields_from_malicious_file
import sys
import matplotlib.pyplot as plt
import signal
from pprint import pprint

# Make sure that phantomjs is launched by the command: phantomjs  --webdriver 28042


# Handler for the timeout
def handler(signum, frame):
    raise Exception("Timeout")
signal.signal(signal.SIGALRM, handler)


def predict(url_name):
    features_name_file = "Dumps/feat_names.pkl"
    clf = joblib.load("Dumps/clf_rforest.pkl")
    X_to_predict = url_to_X(url_name, features_name_file)
    
    # Set handler and timeout
    prediction =  clf.predict(X_to_predict)[0]
    if prediction == 0:
        p = "Prediction: benign."
    else:
        p = "Prediciton: malicious."
        
    return p

def predict_proba(url_name):
    features_name_file = "Dumps/feat_names.pkl"
    clf = joblib.load("Dumps/clf_rforest.pkl")
    X_to_predict = url_to_X(url_name, features_name_file)
    
    # Set handler and timeout
    prediction =  clf.predict(X_to_predict)[0]
    prediction_proba =  clf.predict_proba(X_to_predict)[0]
    if prediction == 0:
        p = "Benign"
    else:
        p = "Malicious"
    
    h_proba = max(prediction_proba[0],prediction_proba[1])

    #pprint(prediction_proba)   
    return "Probability: "+str(h_proba*100)+"%."


def predict_urls(l):
    n = len(l)
    cpt = 0
    times = []
    sys.stdout.write("Prediction: ")
    for u in l:
        signal.alarm(20)
        try:
            t0 = time.time()
            predict(u)
            t1 = time.time()
        except Exception,exc:
            print exc
        else:
            cpt += 1
            sys.stdout.write("\rPrediction: "+str(cpt*100/n)+"%    ")
            t = t1-t0
            times.append(t)
        
    return times
    
def stat_predict_urls(times):
    t_total = sum(times)
    average_time = t_total/len(times)
    print "Average time: "+str(average_time)+"."
    plt.figure() 
    plt.hist(times,10)
    plt.ylabel("# URLs")
    plt.xlabel("Time (seconds)")
    
    
def test_predict():
    url_name = "http://fahd.com"
    print predict(url_name)

def test_predict_proba():
    url_name = "http://google.com"
    print predict(url_name)
    print predict_proba(url_name)

def test_predict_urls():
    benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
    malicious_urls_addr = '/home/avl/MSc-project/Crawler/mwlist_all'
    burls = urls_from_crawler(benign_urls_addr)
    mfields = get_fields_from_malicious_file(malicious_urls_addr)
    murls = [f['url_name'] for f in mfields]
    urls = burls+murls
    print "Start..."
    return predict_urls(urls)



if __name__=='__main__':
 #   test_predict()
    test_predict_proba()
