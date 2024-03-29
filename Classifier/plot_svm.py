# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:17:50 2016

@author: avl
"""


# TODO: PCA

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

def plot_svm(X, y):
    # figure number
    fignum = 1
    
    # fit the model
    for name, penalty in (('unreg', 1), ('reg', 0.05)):
    
        clf = svm.SVC(kernel='linear', C=penalty)
        clf.fit(X, y)

        # get the separating hyperplane
        w = clf.coef_[0]
        a = -w[0] / w[1]
        xx = np.linspace(-5, 5)
        yy = a * xx - (clf.intercept_[0]) / w[1]
    
        # plot the parallels to the separating hyperplane that pass through the
        # support vectors
        margin = 1 / np.sqrt(np.sum(clf.coef_ ** 2))
        yy_down = yy + a * margin
        yy_up = yy - a * margin
    
        # plot the line, the points, and the nearest vectors to the plane
        plt.figure(fignum, figsize=(4, 3))
        plt.clf()
        plt.plot(xx, yy, 'k-')
        plt.plot(xx, yy_down, 'k--')
        plt.plot(xx, yy_up, 'k--')
    
        plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
                    facecolors='none', zorder=10)
        plt.scatter(X[:, 0], X[:, 1], c=y, zorder=10, cmap=plt.cm.Paired)
    
        plt.axis('tight')
        x_min = -4.8
        x_max = 4.2
        y_min = -6
        y_max = 6
    
        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
        Z = clf.predict(np.c_[XX.ravel(), YY.ravel()])
    
        # Put the result into a color plot
        Z = Z.reshape(XX.shape)
        plt.figure(fignum, figsize=(4, 3))
        plt.pcolormesh(XX, YY, Z, cmap=plt.cm.Paired)
    
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
    
        plt.xticks(())
        plt.yticks(())
        fignum = fignum + 1
    
    plt.show()