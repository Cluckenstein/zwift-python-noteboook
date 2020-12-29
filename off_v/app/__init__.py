#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:38:29 2020

@author: maximilianreihn
"""


from flask import Flask

app = Flask(__name__)

from app import routes