# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:52:15 2016

@author: avl
"""
#import datetime

with open('malwaredomains-raw','r') as f:
    lines = f.read().splitlines()
    date = lines[-1].split()[-1]
    #d = datetime.datetime.strptime(lines[-1].split()[-1], "%Y%m%d")
    #print d
    
    with open('malwaredomains-raw-recent','w') as f2:
        cpt = -1
        line = lines[cpt]
        data = ''
        while (line.split()[-1] == date):
            if len(line.split()) == 4:
                line = line.replace('\t',' ')
                line = line[2:]
                data += line + "\n"
            cpt -= 1
            line = lines[cpt]
        f2.write(data)

