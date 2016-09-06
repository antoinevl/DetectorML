import urllib2

def crawl():   
    # Create a file to store URLs
    f = open('alexa-top500','w')
    
    # Number of links
    links_total = 500
    links_per_page = 25
    number_pages = links_total/links_per_page
    if ((links_total%links_per_page) > 0):
    	number_pages += 1
    
    
    for ind in xrange(number_pages):
    
    	# Open Alexa webpage
    	url = 'http://www.alexa.com/topsites/countries;'+str(ind)+'/GB'
    	resp = urllib2.urlopen(url)
    	page = resp.read()
    
    	# Get the URLs on the page
    	end=0
    	for ind2 in xrange(links_per_page):
    		start = page.find('<a href="/siteinfo/',end) + len('<a href="/siteinfo/')
    		end = page.find('"',start)
    		link = "http://"+page[start:end]
    		f.write(link)
    		f.write("\n")
    
    f.close()
    

