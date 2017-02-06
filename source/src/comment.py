# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 23:01:23 2017

@author: wy
"""

import xmltodict as xtd
import requests as rq

def fetch_comment(aid):
    aid = int(aid)
    res = rq.get("http://comment.bilibili.com/%d.xml"%aid)
    if res.status_code != 200:
        print("error occuring when trying %d."%aid)
        return []
    xmlstring = res.text
    parsed = xtd.parse(xmlstring)
    obj_list = parsed['i']['d']
    result = []
    for obj in obj_list:
        properties = obj['@p']
        text = obj['#text']
        #print(properties)
        time,mode,size,color,date,pool,crc,comment_id = properties.strip().split(',')
        result.append({
            "aid":aid,
            "time":float(time),
            "mode":int(mode),
            "size":int(size),
            "color":int(color),
            "date":int(date),
            "pool":int(pool),
            "crc":int(crc,16),
            "comment_id":int(comment_id),
            "text":text
                       })
    return result

