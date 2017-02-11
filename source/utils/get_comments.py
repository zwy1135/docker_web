# -*- coding: utf-8 -*-
"""
Created on Sat May 28 21:09:48 2016

@author: wy
"""

import requests as rq
 
address = "127.0.0.1"
existed=161698
continue_err_count = 0
for i in range(existed,8000000):
    res = rq.get("http://%s/CommentJsonHandler?aid=%d"%(address,i))
    if res.status_code != 200:
        print("error occuring. cid = %d"%i)
        print(res.text)
        continue_err_count += 1
        if continue_err_count > 1000:
            break
        continue
    else:
        continue_err_count = 0
    
    print("got comment for cid = %d"%i)
    
        
