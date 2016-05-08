# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 18:17:33 2016

@author: wy
"""
import json
import logging

import tornado.web as web
import tornado.gen as gen
import requests as rq
import pymongo


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                )
#from .user_data import DataSet
#
#dataset = DataSet(os.path.join(os.path.dirname(os.path.abspath(__file__)),"biliuser_data.pkl"))
#dataset.load()
#print("data loaded")
#def get_data(user_id = 423895):
#    if user_id in dataset.user_data_set:
#        return dataset.user_data_set.get(user_id)
#    try:
#        #print("clawing user_id %d"%user_id)
#        response = rq.get("http://space.bilibili.com/ajax/member/GetInfo?mid=%d"%user_id)
#        if 200 != response.status_code:
#            return None
#        
#        data = response.json()["data"]
#        dataset.add_data(user_id,data)
#        dataset.add_edges_from([(user_id,to) for to in data["attentions"] if to is not None])
#        dataset.save()
#        
#        #print("got user %s"%str(data["name"]))
#        return data
#    except:
#        return None

conn = pymongo.MongoClient("mongodb")
db = conn.bilidb

dataset = db.bilidata
dataset.create_index("mid", unique=True)

def get_data(user_id = 423895):
    res = dataset.find_one({"mid":user_id})
    if  res is not None:
        return res
    try:
        logging.debug("Crawling user_id %d"%user_id)
        response = rq.get("http://space.bilibili.com/ajax/member/GetInfo?mid=%d"%user_id)
        if 200 != response.status_code:
            return None
        
        data = response.json()["data"]
        data["mid"] = int(data["mid"])
        dataset.insert_one(data)
        
        logging.debug("got user %s"%str(data["name"]))
        return data
    except:
        return None
        
        



class RelationshipJsonHandler(web.RequestHandler):
#    def get(self):
#        #TODO:add real data
#        nodes = [{"name":"1"},{"name":"2"},{"name":"3"}]
#        edges = [{"source":1,"target":2},{"source":1,"target":0},{"source":0,"target":2}]
#        data = {"nodes":nodes,"edges":edges}
#        
#        self.write(json.dumps(data))
    def get(self):
        user_id = self.get_argument("user_id",default=None)
        if user_id:
            user_id = int(user_id)
            user_list = []
            user_res = get_data(user_id)
            assert(user_res is not None)
            user_list.append(user_res)
            attentions = [get_data(int(x)) for x in user_res["attentions"]]
            user_list.extend(attentions)
            
            nodes = [{"name":user["name"], "image":user["face"]} for user in user_list if user is not None]
            edges = [{"source":0,"target":x} for x in range(1,len(nodes))]
            
            data = {"nodes":nodes,"edges":edges}       
            self.write(json.dumps(data))
        
            