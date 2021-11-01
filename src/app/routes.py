#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:40:35 2020

@author: maximilianreihn
"""

from flask import render_template, request, make_response, send_from_directory, redirect, url_for
from src.app import app
import json
import os 
from src.worker.calc import training
from src.worker.workout_parser import parse



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return redirect(url_for('workout'))

@app.route('/workout', methods=['GET', 'POST'])
@app.route('/workout/', methods=['GET', 'POST'])
def workout():
    return render_template('zwift_page/index.html')


@app.route('/ploter/', methods=['GET', 'POST'])
def ploter():
    name = request.form.get('name')
    description = request.form.get('description')
    ftp = request.form.get('ftp')
    string = request.form.get('string')
    if ftp != '':
        try:
            ftp = int(ftp)
        except:
            ftp = None

    fig = parse(name, description, ftp, string)

    #resp = make_response(json.dumps(plot))
    return fig


@app.route('/generator/', methods=['GET', 'POST'])
def generator():
    name = request.form.get('name')
    description = request.form.get('description')
    ftp = request.form.get('ftp')
    string = request.form.get('string')
    if ftp != '':
        try:
            ftp = int(ftp)
        except:
            ftp = None

    tag = request.form.get('generate')
    gen = bool(request.form.get('generate'))

    fig = parse(name, description, ftp, string, tag = tag, generate = True)

    #resp = make_response(json.dumps(plot))
    return fig


@app.route('/zwo_download/<filename>')
def zwo_download(filename):
    print(request.url)
    return send_from_directory('/src/zwo_files', filename)
