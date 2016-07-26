# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:34:35 2016

@author: avl
"""


import urllib2
import static_extractor as se
import dynamic_extractor as de
import sys
import numpy as np
from datetime import date

class URL:
    #url_name = 'http://www.google.com/'
    #resp = urllib2.urlopen(url_name)
    #page = resp.read()

    def __init__(self, url):
        self.name = url
        self.page = None
    
    def set_page(self, p):
        self.page = p
    
    def set_code(self, c):
        self.code = c
                           
    script_token_start = "<script>"
    script_token_end = "</script>"

    def js_list(self):
        javascript = []
        ind_start = 0
        while (self.page.find(self.script_token_start, ind_start)!=-1):
        	ind_start = self.page.find(self.script_token_start, ind_start) + len(self.script_token_start)
        	ind_end = self.page.find(self.script_token_end, ind_start)
        	javascript.append(self.page[ind_start:ind_end])
        	ind_start = ind_end
        return javascript
    
    def js_all(self):
        return '\n'.join(self.js_list())
    
    def static_features(self):
        static_features = {}
        static_features['letter_count'] = se.letter_count(self.page)
        static_features['word_count'] = se.word_count(self.page)
        static_features['line_count'] = se.line_count(self.page)
        static_features['js_letter_count'] = se.letter_count(self.js_all())
        static_features['js_word_count'] = se.word_count(self.js_all())
        static_features['js_line_count'] = se.line_count(self.js_all())
        static_features['js_keyword_count'] = se.keyword_count(self.js_all(), 'eval')
        static_features['js_most_frequent_word'] = se.most_frequent_word(self.js_all())
        return static_features
        
    def dynamic_features(self):
        dynamic_features = {}
        dynamic_features['feat1'] = de.feature1(self.page)
        return dynamic_features

    def get_feature_names(self):
        s_feat = self.static_features()
        d_feat = self.dynamic_features()
        names = {'Static':[],'Dynamic':[], 'All':[]}
        for i in s_feat:
            names['Static'].append(i)
        for i in d_feat:
            names['Dynamic'].append(i)
        names['All'] = np.concatenate((names['Static'], names['Dynamic']))

    # Returns html and error code of the request
    def process(self, to_reload = True, user_agent, method):
        output = {}
        
        # Parameters
        if method == 'Selenium':
            if user_agent == 'firefox':
                print
            elif user_agent == None:
                print
            else:
                raise "Error in process_request. User agent: "+user_agent+" unknown."
        
        elif method == 'urllib2':
            if user_agent == 'firefox':
                req = urllib2.Request(self.name, headers={ 'User-Agent': 'Mozilla/5.0' })
            elif user_agent == None: 
                req = urllib2.Request(self.name)
            else:
                raise "Error in process_request. User agent: "+user_agent+" unknown."
            
            # Open and read    
            try:
                resp = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                output['code'] = e.code
                output['page'] = ''
            except urllib2.URLError as e:
                output['code'] = -1
                output['page'] = ''
            except:
                #print sys.exc_info()
                output['code'] = -2
                output['page'] = ''
            else:
                page = resp.read()
                output['page'] = page
                output['code'] = 200
                  
            
        else:
            raise "Error in process_request. Method: "+method+" unknown."
        
        self.page = output['page']
        self.user_agent = user_agent
        self.method = method
        
        return output  