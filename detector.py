# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:52:50 2016

@author: avl
"""

from sklearn.externals import joblib
from Extractor.url_processing import url_to_X
from pprint import pprint

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

if __name__=='__main__':
    url_name = "http://fahd.com"
    print predict(url_name)
