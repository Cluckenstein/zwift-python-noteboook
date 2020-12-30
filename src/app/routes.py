#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:40:35 2020

@author: maximilianreihn
"""

from flask import render_template, request, make_response, send_from_directory
from app import app
import json
import os 
from worker.calc import training
from worker.workout_parser import parse



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    import os 
    print(os.getcwd())
    return render_template('index.html', title='ZWIFT')



@app.route('/ploter/', methods=['GET', 'POST'])
def ploter():
    name = request.form.get('name')
    description = request.form.get('description')
    ftp = int(request.form.get('ftp'))
    string = request.form.get('string')

    fig = parse(name, description, ftp, string)

    #resp = make_response(json.dumps(plot))
    return fig


@app.route('/generator/', methods=['GET', 'POST'])
def generator():
    name = request.form.get('name')
    description = request.form.get('description')
    ftp = int(request.form.get('ftp'))
    string = request.form.get('string')

    tag = request.form.get('generate')
    gen = bool(request.form.get('generate'))

    fig = parse(name, description, ftp, string, tag = tag, generate = True)

    #resp = make_response(json.dumps(plot))
    return fig


@app.route('/zwo_download/<filename>')
def zwo_download(filename):
    return send_from_directory('/src/zwo_files', filename)