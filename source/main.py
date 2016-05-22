# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 01:37:52 2016

@author: wy
"""
import os
import logging

import tornado.httpserver as httpserver
import tornado.ioloop as ioloop
import tornado.web as web

from tornado.options import define, options

import src.HandlerList as HandlerList
define("port", default=8000, help="run on the given port", type=int)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                )
                
                

        

handlers = []

handlers += HandlerList.handlers

template_path = os.path.join(os.path.dirname(__file__),"templates")
static_path = os.path.join(os.path.dirname(__file__),"static")

if __name__ == "__main__":
    options.parse_command_line()
    
    app = web.Application(
        handlers = handlers,
        template_path = template_path,
        static_path = static_path,
        debug=True,
    )
    logging.info("Server runing at %d"%options.port)
    server = httpserver.HTTPServer(app)
    server.listen(options.port)
    ioloop.IOLoop.instance().start()
    
    