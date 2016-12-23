# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 00:07:42 2016

@author: wy
"""
from __future__ import print_function

import requests as rq


user_id = 0

while True:
    try:
        rq.get("http://127.0.0.1/relationship_data?user_id=%d"%user_id)
        print("got user %d"%user_id)
    except rq.ConnectionError:
        print("failed to get user %d"%user_id)
    user_id += 1

