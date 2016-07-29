# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:35:10 2016

@author: avl
"""

def urls_from_crawler(s):
    with open(s, 'r') as f:
        return f.read().splitlines()
        
def get_fields_from_malicious_line(line):
    output = {}
    output['url_name'] = line.split()[0]
    output['ip'] = line.split()[1]
    output['malicious_type'] = line.split()[2]
    output['malicious_src'] = line.split()[3]
    output['date'] = line.split()[4]
    return output
    
def get_fields_from_malicious_file(f):
    output = []
    lines = f.read().splitlines()
    for line in lines:
        output.append(get_fields_from_malicious_line(line))
    return output