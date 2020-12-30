from worker.calc import training
from datetime import date
import json


def parse(name, description, ftp, string, tag = '', generate = False):
    if name == '':
        name = 'new Workout'
    if description == '':
        description = 'new Description'
    if type(ftp) != int or ftp < 70 or ftp > 450:
        ftp = 300
    
    tr = training(name, description, ftp, offline = False)
    string = string.split('\n')
    string = [k for k in string if k != '']


    for block in string:
        if 'add' in block:
            params = [k.strip() for k in block[block.index('(')+1: block.index(')')].split(',')]
            if len(params) == 3:
                if params[1][0] == '[' and params [2][-1]:
                    params = [params[0], params[1]+','+params[2]]
   
            if '[' not in params[1]:
                if len(params) == 2:
                    tr.add(float(params[0]), float(params[1]))
                elif len(params) == 3:
                    tr.add(float(params[0]), float(params[1]), int(params[2]))

            elif '[' in params[1]:
                if len(params) == 2:
                    tr.add(float(params[0]), [float(k) for k in eval(params[1])])
                elif len(params) == 3:
                    tr.add(float(params[0]), [float(k) for k in eval(params[1])], int(params[2]))


        elif 'inter' in block:
            params = [k.strip() for k in block[block.index('(')+1: block.index(')')].split(',')]

            if len(params) == 5:
                tr.interval(int(params[0]), int(params[1]), float(params[2]), int(params[3]), float(params[4]))
            if len(params) == 7:
                tr.interval(int(params[0]), int(params[1]), float(params[2]), int(params[3]), float(params[4]), int(params[5]), int(params[6]))


        elif 'text' in block:
            
            params = block[block.index('(')+1:]
            p1 = int(params[0:params.index(',')])

            params = params[params.index(',')+1:]
            p2 = params[params.index('\'')+1: params.index('\'', params.index('\'')+1)]
            params = params[params.index('\'', params.index('\'')+1):]

            if ',' in params:
                p3 = params[params.index(',')+1 : params.index(')')]
            else:
                p3 = None

            if not p3:
                tr.text(p1, p2)
            if p3:
                tr.text(p1, p2, p3)

    
    plot = tr.plot()

    print(tr.blocks)

    if generate:
        tr.generate('zwo_files/'+tag + '-'+name)

    return plot