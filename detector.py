# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:52:50 2016

@author: avl
"""

from sklearn.externals import joblib
from Extractor.url_processing import url_to_X
from pprint import pprint

url_name = "http://fahd.com"

def predict(url_name):
    features_name_file = "feat_names.pkl"
    clf = joblib.load("clf_svm.pkl")
    X_to_predict = url_to_X(url_name, features_name_file)
    prediction =  clf.predict(X_to_predict)[0]
    print "'"+url_name+"' is",
    if prediction == 0:
        print "benign."
    else:
        print "malicious."

