# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 17:10:45 2016

@author: avl
"""

import random

from sklearn import s
from sklearn.metrics import roc_curve, accuracy_score, f1_score, fbeta_score, precision_score, recall_score

def shuffle_dataset(dataset):
    ds = dataset
    data = dataset['data']
    target = dataset['target']

    arr = []
    for i in xrange(len(data)):
        item = {}
        item['sample'] = data[i]
        item['target'] = target[i]
        arr.append(item)
        
    random.shuffle(arr)
    t = []
    d = []
    for i in xrange(len(arr)):
        t.append(arr[i]['target'])
        d.append(arr[i]['sample'])
    ds['target'] = t
    ds['data'] = d
    
    return ds
    
def svm_prediciton(X, y, X_to_predict):
    clf = svm.SVC() # also NuSVC and LinearSVC
    clf.fit(X, y)
    y_pred = clf.predict(X_to_predict)
    return y_pred

def classification_metrics(y_true, y_pred):
    roc = roc_curve(y_true, y_pred)
    print "Accuracy score: "+accuracy_score(y_true, y_pred)
    print "F1 score: "+f1_score(y_true, y_pred)
    print "F2 score: "+fbeta_score(y_true, y_pred, 2)
    print "Precision score: "+precision_score(y_true, y_pred)
    print "Recall score: "+recall_score(y_true, y_pred)
    
    
    