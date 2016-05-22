# -*- coding: utf-8 -*-
"""
Created on Sun May 22 18:52:56 2016

@author: wy
"""

import tornado.web as web

class UserRelationHandler(web.RequestHandler):
    def get(self):
        user_id = self.get_argument("user_id",default=None)
        self.render("user_relationship.html",title=u"用户关系",user_id=user_id)
        
class SexDistributionHandler(web.RequestHandler):
    def get(self):
        self.render("sex_distribution.html",title=u"性别分布")
    
        



html_handlers = [(r"/",UserRelationHandler),
                 (r'/sex_distribution',SexDistributionHandler),
                 ]


