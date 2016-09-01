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

# Make sure that phantomjs is launched by the command: phantomjs  --webdriver 28042

def predict(url_name):
    features_name_file = "Dumps/feat_names.pkl"
    clf = joblib.load("Dumps/clf_rforest.pkl")
    X_to_predict = url_to_X(url_name, features_name_file)
    prediction =  clf.predict(X_to_predict)[0]
    if prediction == 0:
        return "benign"
    else:
        return "malicious"

def predict_urls(l):
    n = len(l)
    cpt = 0
    times = []
    sys.stdout.write("Prediction: ")
    for u in l:
        t0 = time.time()
        predict(u)
        cpt += 1
        sys.stdout.write("\rPrediction: "+str(cpt*100/n)+"%    ")
        t1 = time.time()
        t = t1-t0
        times.append(t)
    return times
    
def stat_predict_urls(times):
    t_total = sum(times)
    average_time = t_total/len(times)
    print "Average time: "+average_time+"."
    plt.figure() 
    plt.hist(times,10)
    plt.ylabel("# URLs")
    plt.xlabel("Time (seconds)")
    
    
def test_predict():
    url_name = "http://fahd.com"
    print predict(url_name)

def test_predict_urls():
    benign_urls_addr = '/home/avl/MSc-project/Crawler/alexa-top500'
    malicious_urls_addr = '/home/avl/MSc-project/Crawler/mwlist_all'
    burls = urls_from_crawler(benign_urls_addr)
    mfields = get_fields_from_malicious_file(malicious_urls_addr)
    murls = [f['url_name'] for f in mfields]
    urls = burls+murls
    print "Start...\n"
    predict_urls(urls)



if __name__=='__main__':
#    test_predict()
    test_predict_urls()
