def crawl_benign():
    METHOD = 'urllib2' # 'Selenium' or 'urllib2'
    UA = 'firefox' # 'firefox' or None       
    urls_to_analyse = urls_from_crawler(benign_urls_addr)
    
    t = time.time()
    cpt_benign = 0    
    print("Starting benign extraction...")
    
    for u in urls_to_analyse:
        
        cpt_benign += 1
        s1 = ''
        if cpt_benign%50 == 0:
            s1 = "\n Time elapsed: "+str(time.time() - t)+"\n"            
        s =s1+str(cpt_benign)+ " - "
        print s,
        
        url = URL(u, url_type = 'Benign')
        check = 1
        if is_in_db(u, db_urls):
            check = has_new_features_to_add(url, db_urls)   # check = 0 if no new features
                                                            #         1 else
            if check == True:
                if is_in_db(u, db):
                    RELOAD = not(check_field_value_in_url(u, 'user_agent', UA, db_urls) and check_field_value_in_url(u, 'method', METHOD, db_urls)) # reload page if different UA and Method
                    url.process(to_reload = RELOAD, method = METHOD, user_agent = UA)
                    update_url_in_db(url, db_urls, to_recompute = RELOAD)
                else:
                    url.process(method = METHOD, user_agent = UA)
                    add_url_in_db(url, db_urls)
            else:
                print "URL '"+u+"' already stored and not modified."
        else:
            url.process(method = METHOD, user_agent = UA)
            add_url_in_db(url, db_urls)
