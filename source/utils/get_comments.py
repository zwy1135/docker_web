# -*- coding: utf-8 -*-
"""
Created on Sat May 28 21:09:48 2016

@author: wy
"""
import os

import requests as rq
 

existed_filenum = [0]
existed_filenum +=[int(x) for x in os.listdir()]

for i in range(max(existed_filenum),8000000):
    res = rq.get("http://comment.bilibili.com/%d.xml"%i)
    if res.status_code != 200:
        print("error occuring.")
        print(res.text)
        continue
    
    print("got comment for cid = %d"%i)
    with open("%d"%i,"w",encoding='utf-8') as f:
        f.write(res.text)
        
