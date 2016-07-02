# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 17:10:45 2016

@author: avl
"""

import random

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
    
    