#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:40:35 2020

@author: maximilianreihn
"""

from flask import render_template, request, make_response
from app import app
import json
import os 
from worker.calc import training





@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='ZWIFT')



@app.route('/tester/', methods=['GET', 'POST'])
def tester():
    data = request.form.get('key')
    ftp = int(request.form.get('ftp'))
    print(type(ftp), ftp)

    e = training('neeeeew', 'beschreibung', ftp= ftp, offline = False)
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

    #resp = make_response(json.dumps(plot))
    return plot