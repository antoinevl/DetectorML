# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:35:10 2016

@author: avl
"""

def urls_from_crawler(s):
    with open(s, 'r') as f:
        return f.read().splitlines()