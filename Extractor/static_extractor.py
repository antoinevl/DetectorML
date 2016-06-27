# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:59:38 2016

@author: avl
"""

def line_count(page):
    lines = page.splitlines()
    return len(lines)

def letter_count(page):
    lines = page.splitlines()
    letter_count = 0
    for line in lines:
    	letter_count += len(line)
    return letter_count

def word_count(page):
    lines = page.splitlines()
    word_count = 0
    for line in lines:
    	word_count += len(line.split())
    return word_count