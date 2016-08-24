# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:34:35 2016

@author: avl
"""


import urllib2, httplib

from bs4 import BeautifulSoup

from selenium import webdriver

from pprint import pprint
import static_extractor as se
import dynamic_extractor as de
#import sys
import numpy as np
#from datetime import date
import url_processing as up
from base64 import b64decode
#import time



class URL:
    #url_name = 'http://www.google.com/'
    #resp = urllib2.urlopen(url_name)
    #page = resp.read()

    def __init__(self, url_name, url_type = None, url_description = None):
        self.name = url_name
        self.type = url_type
        self.description = url_description
        self.page = ''
        self.code = 0
        self.static_features = {}
        self.dynamic_features = {}
    
    def set_page(self, p):
        self.page = p
    
    def set_code(self, c):
        self.code = c

    def js_list(page):
        script_token_start = "<script>"
        script_token_end = "</script>"
        javascript = []
        ind_start = 0
        while (page.find(script_token_start, ind_start)!=-1):
        	ind_start = page.find(script_token_start, ind_start) + len(script_token_start)
        	ind_end = page.find(script_token_end, ind_start)
        	javascript.append(page[ind_start:ind_end])
        	ind_start = ind_end
        return javascript
    
    def js_all(self, page):
        return '\n'.join(self.js_list(page))
    
    def static_features_pierre(self):
        s_feats = {}
        
        s_feats['js_total_letter_count'] = 0
        s_feats['js_max_letter_count'] = 0
        s_feats['js_min_letter_count'] = 0
    
        s_feats['js_total_word_count'] = 0
        s_feats['js_max_word_count'] = 0
        s_feats['js_min_word_count'] = 0
    
        s_feats['js_total_line_count'] = 0
        s_feats['js_max_line_count'] = 0
        s_feats['js_min_line_count'] = 0
            
        s_feats['js_total_eval_count'] = 0
        s_feats['js_total_unescape_count'] = 0
        s_feats['js_total_escape_count'] = 0
        
        s_feats['html_letter_count'] = 0
        s_feats['html_word_count'] = 0
        s_feats['html_line_count'] = 0
        
        return s_feats
    
    def dynamic_features_pierre(self):
        dynamic_features = {}
        #dynamic_features['feat1'] = de.feature1(self.page)
        return dynamic_features

    def get_feature_names(self):
        s_feat = self.static_features_pierre()
        d_feat = self.dynamic_features_pierre()
        names = {'Static':[],'Dynamic':[], 'All':[]}
        for i in s_feat:
            names['Static'].append(i)
        for i in d_feat:
            names['Dynamic'].append(i)
        names['All'] = np.concatenate((names['Static'], names['Dynamic']))
        return names

    # Returns html and error code of the request
    def process(self, user_agent = None, method = None, to_reload = True, collection = None):
        ###t = time.time()        
        
        # Case where user_agent and method are already instantiated
        if user_agent != None and method != None:
            self.user_agent = user_agent
            self.method = method
        
       ###print ">> process 1: "+str(time.time()-t)+"."       
        
        output = {}
        
        if to_reload == False:
            ###print ">> process 1.1a: "+str(time.time()-t)+"."
            if collection != None:
                ###print ">> process 1.1a.1: "+str(time.time()-t)+"."
                output['page'] = b64decode(up.get_field_from_url(self.name, 'page_b64', collection))
                ###print ">> process 1.1a.2: "+str(time.time()-t)+"."
                output['code'] = up.get_field_from_url(self.name, 'code', collection)
                ###print ">> process 1.1a.3: "+str(time.time()-t)+"."
            else:
                raise "Error in 'process': please specify collection name."
        else:
            # Parameters
            if method == 'Selenium':
                output = self.process_selenium(user_agent)
            elif method == 'urllib2':
                output = self.process_urllib2(user_agent)
            else:
                raise "Error in process_request. Method: "+method+" unknown."
        ###print ">> process 2: "+str(time.time()-t)+"."
                
        self.page = output['page']
        self.code = output['code']
        self.static_features = output['static_features']
        self.dynamic_features = output['dynamic_features']
        
        
        return output
        
    def process_urllib2(self, user_agent):
        output = {}        
        if user_agent == 'firefox':
            req = urllib2.Request(self.name, headers={ 'User-Agent': 'Mozilla/5.0' })
        elif user_agent == None: 
            req = urllib2.Request(self.name)
        else:
            raise "Error in 'process_request'. User agent '"+user_agent+"' unknown."
        
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
            try:
                page = resp.read()
            except httplib.IncompleteRead, e:
                output['code'] = -3
                output['page'] = ''
            else:
                output['page'] = page
                output['code'] = 200
                s_feats = self.static_features(page)
                d_feats = self.dynamic_features(page)
                # Add JS stuff
                output['static_features'] = s_feats
                output['dynamic_features'] = d_feats
        return output
        
    def process_selenium(self, user_agent):
        output = {}
        if user_agent == 'firefox':
            driver = webdriver.Firefox()
            req = urllib2.Request(self.name, headers={ 'User-Agent': 'Mozilla/5.0' })
        elif user_agent == None:
            raise "Error in process_selenium: select a user agent."
        elif user_agent == 'PhantomJS':
            driver = webdriver.PhantomJS() # Requires command: phantomjs  --webdriver 28042
            req = urllib2.Request(self.name, headers={ 'User-Agent': 'Mozilla/5.0' })
        else:
            raise "Error in process_selenium. User agent: "+user_agent+" unknown."
        
        driver.get(self.name)
        
        try:
            page = driver.page_source
        except:
            output['page'] = ""
            output['code'] = -5
            driver.quit()
        else:
            output['page'] = page
            s_feats = {}
            d_feats = {}
            
            # Get JS from webpage and add features
            js_script_list = []
            js_src_list = []
            js_src_content_list = []
            soup = BeautifulSoup(page, "html.parser")
            # Find all script tags 
            for n in soup.find_all('script'):
                # Check if the src attribute exists, and if it does grab the source URL
                if 'src' in n.attrs:
                    javascript_src = n['src']
                    js_src_list.append(javascript_src)
                    
                # Otherwise assume that the javascript is contained within the tags
                else:
                    javascript = n.text
                    js_script_list.append(javascript)
                    
            js_letter_count = []
            js_word_count = []
            js_line_count = []
            js_total_eval_count = 0
            js_total_unescape_count = 0
            js_total_escape_count = 0
            
            for s in js_src_list:
                try:
                    resp = urllib2.urlopen(s)
                except:
                    #print 'Warning: unknown url type.'
                    pass
                else:
                    script = resp.read()
                    js_src_content_list.append(script)
                    js_letter_count.append(se.letter_count(script))
                    js_word_count.append(se.word_count(script))
                    js_line_count.append(se.line_count(script))
                    js_total_eval_count += se.keyword_count(script, 'eval')
                    js_total_unescape_count += se.keyword_count(script, 'unescape')
                    js_total_escape_count += se.keyword_count(script, 'escape')
                
            for s in js_script_list:
                js_letter_count.append(se.letter_count(s))
                js_word_count.append(se.word_count(s))
                js_line_count.append(se.line_count(s))
                js_total_eval_count += se.keyword_count(s, 'eval')
                js_total_unescape_count += se.keyword_count(s, 'unescape')
                js_total_escape_count += se.keyword_count(s, 'escape')
                
            
            
            s_feats['js_scripts_count'] = len(js_src_list) + len(js_script_list)
            
            
            try:
                s_feats['js_total_letter_count'] = sum(js_letter_count)
                s_feats['js_max_letter_count'] = max(js_letter_count)
                s_feats['js_min_letter_count'] = min(js_letter_count)
            except:
                s_feats['js_total_letter_count'] = 0
                s_feats['js_max_letter_count'] = 0
                s_feats['js_min_letter_count'] = 0  
            
            try:
                s_feats['js_total_word_count'] = sum(js_word_count)
                s_feats['js_max_word_count'] = max(js_word_count)
                s_feats['js_min_word_count'] = min(js_word_count)
            except:
                s_feats['js_total_word_count'] = 0
                s_feats['js_max_word_count'] = 0
                s_feats['js_min_word_count'] = 0
            
            try:
                s_feats['js_total_line_count'] = sum(js_line_count)
                s_feats['js_max_line_count'] = max(js_line_count)
                s_feats['js_min_line_count'] = min(js_line_count)
            except:
                s_feats['js_total_line_count'] = 0
                s_feats['js_max_line_count'] = 0
                s_feats['js_min_line_count'] = 0
            
            s_feats['js_total_eval_count'] = js_total_eval_count
            s_feats['js_total_unescape_count'] = js_total_unescape_count
            s_feats['js_total_escape_count'] = js_total_escape_count
            
            s_feats['html_letter_count'] = se.letter_count(page)
            s_feats['html_word_count'] = se.word_count(page)
            s_feats['html_line_count'] = se.line_count(page)
            
            output['static_features'] = s_feats
            output['dynamic_features'] = d_feats
            
            driver.quit()
            
        
            
        # Get the http status code with urllib2 (not possible with selenium)
        # TODO find a method that outputs redirection status
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            output['code'] = e.code
        except urllib2.URLError as e:
            output['code'] = -1
        except:
            output['code'] = -2
        else:
            try:
                resp.read()
            except httplib.IncompleteRead, e:
                output['code'] = -3
            else:
                output['code'] = 200

        
        
        return output
        