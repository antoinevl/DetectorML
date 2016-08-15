# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 17:10:45 2016

@author: avl
"""

import random

from sklearn import svm, cross_validation
from sklearn.metrics import confusion_matrix, roc_curve, auc, accuracy_score, f1_score, fbeta_score, precision_score, recall_score
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

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
    
def svm_prediction(X, y, X_to_predict):
    clf = svm.SVC() # also NuSVC and LinearSVC
    clf.fit(X, y)
    y_pred = clf.predict(X_to_predict)
    return y_pred

def svm_clf():
    return svm.SVC(kernel='linear', C=1)

def cross_validation_scores(X, y, clf): 
    y_pred = cross_validation.cross_val_predict(clf, X, y, cv=5)  # better than cross_val_score: less restricting
    y_true = y
    
    basic_metrics = metrics_from_confusion_matrix(y_true, y_pred)

    # TODO find a way to store this: XML, mongodb, logs...
    print "TP: %0.2f" % basic_metrics['TP']
    print "FP: %0.2f" % basic_metrics['FP']
    print "FN: %0.2f" % basic_metrics['FN']
    print "TN: %0.2f" % basic_metrics['TN']
    print "NPP: %0.2f" % basic_metrics['NPP']
    print "Specificity: %0.2f" % basic_metrics['specificity']
    print "Precision/PPP (basic): %0.2f" % basic_metrics['PPP']
    print "Precision/PPP (predefined):  %0.2f" % precision_score(y_true, y_pred) 
    print "Sensitivity/recall (basic): %0.2f" % basic_metrics['sensitivity']
    print "Sensitivity/recall (predefined):  %0.2f" % recall_score(y_true, y_pred)
    print "Accuracy (basic):  %0.2f" % basic_metrics['accuracy']
    print "Accuracy (predefined):  %0.2f" % accuracy_score(y_true, y_pred)
    print "F1 score (basic):  %0.2f" % basic_metrics['F1']
    print "F1 score (predefined):  %0.2f" % f1_score(y_true, y_pred)
    print "F2 score (basic):  %0.2f" % basic_metrics['F2']
    print "F2 score (predefined):  %0.2f" % fbeta_score(y_true, y_pred, 2)   
    
    # Plot the ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(1)
    plt.plot(fpr, tpr,label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()    


def metrics_from_confusion_matrix(y_true, y_pred):
    output = {}
    cm = confusion_matrix(y_true, y_pred)
    n = len(y_true)

    TP = float(cm[0][0])
    FN = float(cm[0][1])
    FP = float(cm[1][0])
    TN = float(cm[1][1])

    try:
        assert((TP+TN+FP+FN == n))
    except:
         print "Error in 'metrics_from_confusion_matrix'. Size matters..."   
    
    output['TP'] = TP/n
    output['FP'] = FP/n
    output['FN'] = FN/n
    output['TN'] = TN/n
    output['sensitivity'] = TP / (TP + FN)
    output['recall'] = TP / (TP + FN) # Same as sensitivity
    output['specificity'] = TN / (TN + FP)
    output['PPP'] = TP / (TP + FP)
    output['precision'] = TP / (TP + FP) # Same as PPP
    output['NPP'] = TN / (TN + FN)
    output['accuracy'] = (TP + TN) / n
    output['F1'] = 2*TP/(2*TP + FP + FN)
    output['F2'] = 5*output['precision']*output['recall']/(4*output['precision']+output['recall'])
    

    return output
    