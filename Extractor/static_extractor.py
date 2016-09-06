# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:59:38 2016

@author: avl
"""
import re

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

def keyword_count(page, keyword):
    return len(re.findall(keyword, page))
    #return page.count(keyword)

def percentage_whitespace(page):
    return page.count(' ')
    
def most_frequent_word(page):
    dico = {}
    words = page.split()
    for word in words:
        if not(word in dico):
            c = page.count(word)
            dico[word] = c
    try:
        result = max(dico, key=dico.get)
    except:
        result = 'None'
    else:
        return result


if __name__=="__main__":
    s = "s+=(eval(crappnviwevalrnio+"
    print keyword_count(s,"eval")