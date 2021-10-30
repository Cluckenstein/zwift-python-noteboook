#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:30:35 2021

@author: maximilianreihn
"""

from src.worker.workout_parser import parse

string = 'Ramp(60, 61, 65) \n '

parse('nwe', 'new', 315, string, tag = '', generate = False)