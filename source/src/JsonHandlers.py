# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 18:17:33 2016

@author: wy
"""
import json
import logging
import zlib
from copy import deepcopy

from tornado.concurrent import return_future 
from tornado import web
from tornado import gen

import requests as rq
import pymongo

from .comment import fetch_comment



logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                )


conn = pymongo.MongoClient("mongodb")
db = conn.bilidb

dataset = db.bilidata
dataset.create_index("mid", unique=True)
dataset.create_index(u"crc32_int")

comments = db.comments
comments.create_index(u"aid")
comments.create_index(u"crc")
comments.create_index(u"comment_id",unique=True)

def get_data(user_id = 423895):
    res = dataset.find_one({"mid":user_id})
    if  res is not None:
        return res
    try:
        logging.debug("Crawling user_id %d"%user_id)
        response = rq.get("http://app.bilibili.com/x/v2/space?build=4040&vmid=%d"%user_id)
        if 200 != response.status_code:
            return None
        
        data = response.json()["data"]["card"]
        data["mid"] = int(data["mid"])
        crc32 = zlib.crc32(b'%d'%data["mid"])
        data[u"crc32"] = u"%x"%crc32
        data[u"crc32_int"] = crc32
        dataset.insert_one(data)
        
        logging.debug("got user %s"%str(data["name"]))
        return data
    except:
        return None
        

        
@return_future        
def get_relationship_data(user_id,callback):
    user_id = int(user_id)
    user_list = []
    user_res = get_data(user_id)
    assert(user_res is not None)
    user_list.append(user_res)
    if user_res["attentions"]:
        attentions = [get_data(int(x)) for x in user_res["attentions"]]
        user_list.extend(attentions)

    callback(user_list)


class RelationshipJsonHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.get_argument("user_id",default=None)
        if user_id:
            user_id = int(user_id)
            user_list = yield get_relationship_data(user_id)
            
            nodes = [{"name":user["name"], "image":user["face"]} for user in user_list if user is not None]
            edges = [{"source":0,"target":x} for x in range(1,len(nodes))]
            
            data = {"nodes":nodes,"edges":edges}       
            self.write(json.dumps(data))
        self.finish()
        
class SexDistributionJsonHandler(web.RequestHandler):
    def get(self):
        query_strings = [u'男', u'女', u'保密']
        total_num = dataset.count()
        result = [(u'不可描述',total_num)]
        result += [(name,dataset.find({'sex':name}).count()) for name in query_strings]
        data = {"data":result}
        self.write(json.dumps(data))
        
        
        
@return_future       
def get_comments(aid,update_flag,callback):
    res = comments.find({"aid":aid},{"_id":0})
    comment_list = []
    if 0 == res.count() or 1 == int(update_flag):
        try:
            logging.debug("Fetching aid %d"%aid)
            comment_list = fetch_comment(aid)
            comments.insert_many(deepcopy(comment_list))
            logging.debug("Fetched aid %d"%aid)
        except:
            logging.debug("Error when fetching aid %d"%aid)
    else:
        comment_list = [x for x in res]

    callback(comment_list)
            
      
        
        
        
class CommentJsonHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        aid = self.get_argument("aid",default=None)
        update_flag = self.get_argument("update",default=0)
        if aid:
            aid = int(aid)
            result = yield get_comments(aid, update_flag)
            self.write(json.dumps(result))
            
        self.finish()

json_handlers = [(r'/relationship_data', RelationshipJsonHandler),
                 (r'/sex_distribution_data', SexDistributionJsonHandler),
                 (r"/CommentJsonHandler",CommentJsonHandler)
                 ]








