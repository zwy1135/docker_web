# -*- coding: utf-8 -*-
"""
Created on Sat May 28 21:09:48 2016

@author: wy
"""

import requests as rq
 
address = "192.168.99.100"
existed=0

for i in range(existed,8000000):
    res = rq.get("http://%s/CommentJsonHandler?aid=%d"%(address,i))
    if res.status_code != 200:
        print("error occuring.")
        print(res.text)
        continue
    
    print("got comment for cid = %d"%i)
    
        
