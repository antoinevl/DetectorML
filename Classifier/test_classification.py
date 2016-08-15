# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 12:46:55 2016

@author: avl
"""
from classification import svm_prediction, cross_validation_scores, svm_clf
from plot_svm import plot_svm
from sklearn import datasets
from sklearn.preprocessing import label_binarize

from pprint import pprint

# Variables
#X = [[0, 0, 2566, 75], [1, 6, 26, 75], [0, 0, 256, 45], [0, 1, 2656, 415], [1, 0, 6, 99], [2, 0, 286, 45], [0, 5, 96, 54], [1, 3, 633, 62], [0, 1, 744, 89], [1, 2, 62, 81]]
#y = [0, 0, 1, 0, 1, 0, 1, 1, 0, 0]
#X_to_predict = [[0, 1, 22, 555]]
iris = datasets.load_iris()
X = iris.data
y = iris.target
y[:] = [x if x != 2 else 0 for x in y]


#X = [[0, 0, 2566, 75], [1, 6, 26, 75], [0, 0, 256, 45], [0, 1, 2656, 415], [1, 0, 6, 99], [2, 0, 286, 45], [0, 5, 96, 54], [1, 3, 633, 62], [0, 1, 744, 89], [1, 2, 62, 81]]
#y = [0, 0, 1, 0, 1, 0, 1, 1, 0, 0]


clf = svm_clf()

def test_SVM():
    y_pred = svm_prediction(X, y, X_to_predict)
    pprint(y_pred)

def test_plot_SVM():
    # plot_svm(X, y)
    return 1

def test_cross_validation_SVM():
    cross_validation_scores(X, y, clf)
    
if __name__ == '__main__':
    test_cross_validation_SVM()
    
    