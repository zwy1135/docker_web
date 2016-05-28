# -*- coding: utf-8 -*-
"""
Created on Wed May 25 23:06:59 2016

@author: wy
"""

import zlib
import logging

import pymongo

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                )

conn = pymongo.MongoClient("192.168.99.100")
db = conn.bilidb

rainbow_table = db.rainbow_table
rainbow_table.create_index(u"key", unique=True)
try:
    if False:
        res = rainbow_table.find({u"crc32_int":None})
        for item in res:
            item[u"crc32_int"] = int(item[u"crc32"], 16)
            rainbow_table.replace_one({u"_id":item[u"_id"]}, item)
            print("update key = %d"%item[u"key"])


    for i in range(rainbow_table.count(),30000000):
        try:
            crc32 = zlib.crc32(b'%d'%i)
            res = {u"key":i,u"crc32":u"%x"%crc32,u"crc32_int":crc32}
            rainbow_table.insert_one(res)
            #logging.debug("insert key %d and crc32 %x"%(i,crc32))
            print("insert key %d and crc32 %x"%(i,crc32))
        except pymongo.errors.DuplicateKeyError:
            logging.debug("key %d has existed")
finally:
    conn.close()
        
