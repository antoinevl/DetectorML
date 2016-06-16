#!/usr/bin/env python

import urllib2

url = 'http://www.google.com/'

resp = urllib2.urlopen(url)
page = resp.read()


# Extract Javascript between tokens <script></script>
script_token_start = "<script>"
script_token_end = "</script>"

javascript = []
ind_start = 0
while (page.find(script_token_start, ind_start)!=-1):
	ind_start = page.find(script_token_start, ind_start) + len(script_token_start)
	ind_end = page.find(script_token_end, ind_start)
	javascript.append(page[ind_start:ind_end])
	ind_start = ind_end

print(javascript[0])

# 
