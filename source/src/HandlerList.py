# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 18:26:46 2016

@author: wy
"""
from .JsonHandlers import json_handlers
from .HtmlHandlers import html_handlers


handlers = []

handlers += json_handlers
handlers += html_handlers

