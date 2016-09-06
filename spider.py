# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 14:05:23 2016

@author: avl
"""

from detector import predict
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import json

def explore(url_name, depth):
    root = SpiderTree()
    root.name = url_name
    root.type = predict(url_name)
    if depth > 0:
        l = get_linked_urls(url_name)
        root.children = []
        for u in l:
            print u
            root.children.append(explore(u, depth-1))
    else:
        root.children = []
    return root

class SpiderTree(object):
    def _init_(self):
        self.name = None
        self.type = None
        self.children = None

def get_linked_urls(url_name):
    try:
        resp = urllib2.urlopen(url_name)
        page = resp.read()
        soup = BeautifulSoup(page)
        links = soup.find_all('a')
        l = []
        for tag in links:
            link = tag.get('href',None)
            if link is not None:
                if link[0] == '#':
                    pass
                elif link[0] == '/':
                    if len(link)>1 and link[1] == '/':
                        link = "http:"+link
                    else:
                        if url_name[-1]=='/':
                            link = url_name+link[1:]
                        else:
                            link = url_name+link
                    l.append(link) 
                
        # domain        
        domain = url_name
        domain = domain.replace("https://www3.","")
        domain = domain.replace("https://www.","")
        domain = domain.replace("https://","")
        domain = domain.replace("http://www3.","")
        domain = domain.replace("http://www.","")
        domain = domain.replace("http://","")
        if domain[-1] == "/":
            domain = domain[:-1]
    #    for u in l:
    #        if u.find(domain)!=-1:
    #            try:
    #                l = l.remove(u)
    #            except:
    #                pass
            
        for u in l:
            if u.find("http")==-1:
                try:
                    l = l.remove(u)
                except:
                    pass
    except:
        l=[]
    return l
    
def tree_tojson(tree):
    if tree.children == []:
        d = {"url": tree.name, "type": tree.type, "children": []}
    else:
        l_children = tree.children
        l_rec = []
        for child in l_children:
            l_rec.append(tree_tojson(child))
        d = {"name": tree.name, "type": tree.type, "children": l_rec}
    return d
    
       


if __name__=="__main__":
    url_name = "http://www.youporn.com/"
    get_linked_urls(url_name)
    tree = explore(url_name, 2)
    #print tree.children[0].children
    #print get_linked_urls(url_name)
    #print tree.children    
    with open("Graphs/tree.json","w") as f:
        json.dump(tree_tojson(tree),f)
        
    pprint(tree_tojson(tree))