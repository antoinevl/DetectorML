# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:52:15 2016

@author: avl
"""
#import datetime
import urllib2

# Previous version of crawler: from a textfile. New one fetches an url. 
#
#def crawl():
#    with open('/home/avl/MSc-project/Crawler/malwaredomains-raw','r') as f:
#        lines = f.read().splitlines()
#        date = lines[-1].split()[-1]
#        #d = datetime.datetime.strptime(lines[-1].split()[-1], "%Y%m%d")
#        #print d
#        
#        with open('/home/avl/MSc-project/Crawler/malwaredomains-raw-recent','w') as f2:
#            cpt = -1
#            line = lines[cpt]
#            data = ''
#            while (line.split()[-1] == date):
#                if len(line.split()) == 4:
#                    line = line.replace('\t',' ')
#                    line = line[2:]
#                    data += "http://"+line+"\n"
#                cpt -= 1
#                line = lines[cpt]
#            f2.write(data)

def crawl_mwd():
    print '\nStart crawling malwaredomains...'
    resp = urllib2.urlopen('http://mirror1.malwaredomains.com/files/domains.txt')
    lines = resp.read().splitlines()
    date = lines[-1].split()[-1]
    
    
    with open('/home/avl/MSc-project/Crawler/malwaredomains-raw-recent','r') as f:
        stored_urls = f.read().splitlines()
            
    cpt = -1
    count = 0
    line = lines[cpt]
    data = ''
    while (line.split()[-1] == date):
        if len(line.split()) == 4:
            line = line.replace('\t',' ')
            line = line[2:]
            sline = line.split()
            sline.insert(1, 'None')
            line = ' '.join(sline)            
            
            new_url = "http://"+line
            if not new_url in stored_urls:
                data += new_url+"\n"
                count += 1
        cpt -= 1
        line = lines[cpt]
        
    with open('/home/avl/MSc-project/Crawler/malwaredomains-raw-recent','a') as f:
        f.write(data)
    
    print str(count)+' URL(s) have been added to malwaredomains-raw-recent'
    print 'Crawling done.'

def crawl_mwdl():
    print '\nStart crawling malwaredomains...'
    resp = urllib2.urlopen('https://www.malwaredomainlist.com/hostslist/mdl.xml')
    html = resp.read()
    
    with open('/home/avl/MSc-project/Crawler/malwaredomainlist-recent','r') as f:
        stored_urls = f.read().splitlines()   
    
    data = ''
    count = 0
    malicious_src = 'malwaredomainlist'
    start_item = 0
    end_item = html.find('</item>', start_item)
    while end_item <= html.find('</item>', end_item+1):
        start_item = html.find('<item>', end_item) + len('<item>')
        # Get the date
        start_date = html.find(' ', start_item)+2
        end_date = html.find('_', start_date)
        date = html[start_date:end_date].replace('/','')
        day = date[6:8]
        month = date[4:6]
        year = date[2:4]
        date = day+month+year        
        # Get the url    
        start_host = html.find('<description>Host: ', end_date) + len('<description>Host: ')
        end_host = html.find(',', start_host)
        host_url = 'http://'+html[start_host:end_host]
        # Get the IP
        start_ip = html.find('IP address: ', end_host) + len('IP address: ')
        end_ip = html.find(',', start_ip)
        ip = html[start_ip:end_ip]
        # Get the type
        start_type = html.find('Description: ', end_ip) + len('Description: ')
        end_type = html.find('</', start_type)
        malicious_type = html[start_type:end_type].replace(' ','_')
        
        end_item = html.find('</item>', end_type)
        
        #
        new_url = host_url+' '+ip+' '+malicious_type+' '+malicious_src+' '+date
        if not new_url in stored_urls:
            data += new_url+"\n"
            count += 1
        
    with open('/home/avl/MSc-project/Crawler/malwaredomainlist-recent','a') as f:
        f.write(data)
         
    print str(count)+' URL(s) have been added to malwaredomainlist-recent'
    print 'Crawling done.'

def crawl():
    print "--------------------------------------------------------\nCrawl:"
    
    crawl_mwd()
    crawl_mwdl()
    with open('/home/avl/MSc-project/Crawler/malwaredomains-raw-recent','r') as f:
        l1 = f.read()
    with open('/home/avl/MSc-project/Crawler/malwaredomainlist-recent','r') as f:
        l2 = f.read()
    with open('/home/avl/MSc-project/Crawler/mwlist_all','w') as f:
        f.write(l1+l2)
        
    print "--------------------------------------------------------\n"
    
#if __name__ == '__main__':
#    crawl()