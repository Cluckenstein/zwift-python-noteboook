#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:17:49 2020

@author: maximilianreihn
"""


from app import app 


app.run(hosr = '0.0.0.0.0', port = 5000, debug = True)