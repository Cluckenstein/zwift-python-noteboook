#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:37:11 2020

@author: maximilianreihn
"""

from calc import training
import os 
'''
print(os.getcwd())
e = training('neues Workout', 'hier entseht ein neues workout', offline = True)

e.add(600, [50,70])

e.add(45, 80)
e.add(45, 90)
e.add(45, 100)
e.add(45, 90)
e.add(45, 80)

e.interval(3, 60, 80, 240, 60)

for i in range(4):
    e.add(480, 65)

    e.add(45, 80)
    e.add(45, 90)
    e.add(45, 100)
    e.add(45, 90)
    e.add(45, 80)


e.add(600, [70,50])


e.text(13, 'das is eine test message')

# e.text(1, 'das is eine zweite test message', offset = 30)

e.plot()

e.generate('test2')
'''

e = training('neeeeew', 'beschreibung', ftp= 315, offline = True)
e.add(600, [50,70])

e.add(45, 80)
e.add(45, 90)
e.add(45, 100)
e.add(45, 90)
e.add(45, 80)

e.interval(3, 60, 80, 240, 60)

for i in range(4):
    e.add(480, 65)

    e.add(45, 80)
    e.add(45, 90)
    e.add(45, 100)
    e.add(45, 90)
    e.add(45, 80)

e.text(1, 'das is eine zweite test message', offset = 30)
e.add(600, [70,50])
plot = e.plot()