# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 14:05:23 2016

@author: avl
"""

from detector import predict

def explore(url_name, depth):
    root = SpiderTree()
    root.name = url_name
    root.type = predict(url_name)
    if depth > 0:
        root.children = get_linked_urls(url_name)
        for u in root.children:
            explore(u, depth-1)
    return root


def get_linked_urls(url_name):

    return 0

class SpiderTree(object):
    def _init_(self):
        self.name = None
        self.type = None
        self.children = None

if __name__ == "__main__":

    import urllib2
    from bs4 import BeautifulSoup
    url = 'http://www.google.co.in/'

    conn = urllib2.urlopen(url)
    html = conn.read()

    soup = BeautifulSoup(html)
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href',None)
        if link is not None:
            print link
