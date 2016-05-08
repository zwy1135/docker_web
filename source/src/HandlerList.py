# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 18:26:46 2016

@author: wy
"""
from .JsonHandlers import RelationshipJsonHandler


handlers = [(r'/relationship',RelationshipJsonHandler),
            ]