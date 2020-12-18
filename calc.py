#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 14:45:27 2020

@author: maximilianreihn
"""


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import numpy as np
import datetime

colors = ['black','grey', 'blue', 'green', 'yellow', 'orange', 'red']
zones = [0, 59, 75, 89, 104, 118, 9999]

class training(object):
    
    def __init__(self, workout_name= 'new workout', description='description', ftp = 315):
        f = open('head.txt', 'r')
        head = f.read()
        
        head = head.replace('name_var', workout_name)
        head = head.replace('description_var', description)
        
        self.ftp = ftp
        self.zwo = head
        self.blocks = []
        
    
    
    def text(self, id_block, message, offset = 0):
        None
        
        
        
    def add(self, dur, percent, cadence = 0):
        if type(percent) != list:
            percent = [percent, percent]
            
        self.blocks.append({'dur' : dur,
                    'percent' : percent,
                    'cad': [cadence]*2,
                           'interval':False})
        
        #self.plot()
        
    def add_inter(self, repeats, on_dur, on_perc, off_dur, off_perc, on_cad=0, off_cad=0):
        self.blocks.append({'dur' : [on_dur, off_dur],
                    'percent' : [on_perc, off_perc],
                    'cad': [on_cad, off_cad],
                            'repeats':repeats,
                           'interval':True})
        
        
        
    def delete(self, id_block):
        self.blocks.pop(id_block)
        self.plot()
        
        
    def plot(self):
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        
        sec = 0
        
        for i in range(len(self.blocks)):
            
            if self.blocks[i]['interval']:
                diff = int(self.blocks[i]['repeats']*2)
                perc_diff = 0
                up = False
                temp_z = self.zone(self.blocks[i]['percent'][0])
                temp_s = sec
                temp_p = self.blocks[i]['percent'][0]
                
            else:
                perc_diff = abs(self.blocks[i]['percent'][1]- self.blocks[i]['percent'][0])
                diff = int(abs( self.zone(self.blocks[i]['percent'][0]) - self.zone(self.blocks[i]['percent'][1])) + 1)
                up = (self.zone(self.blocks[i]['percent'][1]) > self.zone(self.blocks[i]['percent'][0]))    
                temp_z = self.zone(self.blocks[i]['percent'][0])
                temp_s = sec
                temp_p = self.blocks[i]['percent'][0]
                temp_z = temp_z - up
            
            
            
            
                               
            for zo in range(diff):
                col = colors[temp_z -1 + int(2*up) + 1 - up]
                
                if self.blocks[i]['interval']:
                    z_len = self.blocks[i]['dur'][zo%2]
                    
                elif diff >1:
                    
                    if up:
                        differ = min([zones[temp_z - 1 + int(2*up)], self.blocks[i]['percent'][1]])
                    else:
                        differ = max([zones[min([5,temp_z - 1 + int(2*up)])], self.blocks[i]['percent'][1]])
                    
                    z_len = abs(temp_p - differ) / perc_diff * self.blocks[i]['dur']
                    
                    temp_end = differ
                    
                else:
                    z_len = self.blocks[i]['dur']
                    temp_end = temp_p
                    
                    
                    
                hover_text = 'ID: '+str(i)+ '<br>' 
                hover_text += self.dt(z_len)[-5:]+' min <br>'
                
                    
                if self.blocks[i]['interval']:
                    
                    x_scale = [temp_s, temp_s, temp_s + z_len, temp_s + z_len]
                    y_scale = [0, self.blocks[i]['percent'][zo%2], self.blocks[i]['percent'][zo%2],0]
                    col = colors[self.zone(self.blocks[i]['percent'][zo%2])]
                    hover_text += str(self.blocks[i]['percent'][zo%2])+' % FTP<br>'
                    hover_text += str(round(self.blocks[i]['percent'][zo%2]*self.ftp/100)) +' w<br>'   
                    

                
                elif self.blocks[i]['percent'][0] == 0 or self.blocks[i]['percent'][1] == 0:
                    z_len = self.blocks[i]['dur']
                    x_scale = np.linspace(temp_s, temp_s +z_len, 100)
                    y_scale = 5 * np.sin(x_scale/z_len*12) +50
                    col = 'rgb(200, 200, 200)'
                    hover_text += 'Freeride<br>'
                    
                    
                else:
                    x_scale = [temp_s, temp_s, temp_s + z_len, temp_s + z_len]
                    y_scale = [0, temp_p , temp_end, 0]
                    if temp_p != temp_end:
                        hover_text += str(temp_p) + ' bis '+str(temp_end)+' % FTP<br>'
                        hover_text += str(round(temp_p*self.ftp/100))+ ' bis '+str(round(temp_end*self.ftp/100))+' w<br>'
                    else:
                        hover_text += str(temp_end)+' % FTP<br>'
                        hover_text += str(round(temp_p*self.ftp/100)) +' w<br>'
                    
                if self.blocks[i]['cad'][zo%2] > 0 :
                    hover_text += str(self.blocks[i]['cad'][zo%2])+' rpm'
                        
                trace1=dict(type='scatter',
                    x=[self.dt(temp_s + z_len/2)]*4,
                    y=[max(temp_end, 40)*k/5 for k in range(1,5)],
                    mode='markers',
                    text=[hover_text]*4,
                    hoverinfo='text',
                    marker=dict( color=['rgba(0,0,0,0)']*4),
                    showlegend = False)
                
                fig.add_trace(trace1)
                
                x_scale = [self.dt(k) for k in x_scale]
                    
                fig.add_trace(go.Scatter(x=x_scale,
                                         y=y_scale,
                                         fill='tozeroy', 
                                         fillcolor = col,
                                         hoverinfo = 'text',
                                         text = hover_text,
                                         legendgroup = col,
                                         showlegend = False,
                                         mode='lines',
                                        line = dict(color='black')), secondary_y=False,)
                
                fig.add_trace(go.Scatter(x=x_scale[1:3],
                                         y=[self.ftp/100*k for k in y_scale[1:3]],
                                         hoverinfo='none',
                                         showlegend = False,
                                         mode='lines',
                                        line = dict(color='rgba(0,0,0,0)')), secondary_y=True)
                
                
                if self.blocks[i]['cad'][zo%2]>0:
                    hover_text += 'Cadence '+str(self.blocks[i]['cad'][zo%2])+' rpm'
                    
                    fig.add_trace(go.Scatter(x=[self.dt(temp_s), self.dt(temp_s + z_len)],
                                         y=[0, 40],
                                         legendgroup = col,
                                         showlegend = False,
                                         mode='lines',
                                        hoverinfo='none',
                                        line = dict(color='black')),secondary_y=False)
                    fig.add_trace(go.Scatter(x=[self.dt(temp_s), self.dt(temp_s + z_len)],
                                         y=[40, 0],
                                         legendgroup = col,
                                         showlegend = False,
                                         mode='lines',
                                        hoverinfo='none',
                                        line = dict(color='black')),secondary_y=False)
                
                
                
                temp_s += z_len
                temp_z = temp_z - 1 + int(2*up)
                temp_p = temp_end
                
            if self.blocks[i]['interval']:
                sec += round(self.blocks[i]['repeats']*sum(self.blocks[i]['dur']))
            else:   
                sec += self.blocks[i]['dur']
            
        fig.update_xaxes(title_text='Zeit', type = 'date', tickangle = 0)
        
        fig.update_yaxes(title_text='% FTP', secondary_y=False)
        fig.update_yaxes(title_text='Watt', secondary_y=True, showgrid = False)

        #fig.show()
        
        plot(fig)
        
    @staticmethod
    def dt(seconds):
        return '2000-01-01 ' + str(datetime.timedelta(seconds = seconds))
        
    @staticmethod
    def zone(perc):
        if perc <= zones[1]:
            return 1
        elif perc <= zones[2]:
            return 2
        elif perc <= zones[3]:
            return 3
        elif perc <= zones[4]:
            return 4
        elif perc <= zones[5]:
            return 5
        else:
            return 6
        
    @staticmethod
    def syntax(block, warm = False, cool = False):
        if not block['interval']:
            if block['cad'][0]>0:
                cad = ' Cadence="'+str(block['cad'][0])+'"'
            else:
                cad = ''

            if block['percent'][0] == 0 or block['percent'][1] == 0:

                return '\t\t<FreeRide Duration="'+str(block['dur'])+'" FlatRoad="170"'+cad+'/>'

            elif block['percent'][0] == block['percent'][1]:

                return '\t\t<SteadyState Duration="'+str(block['dur'])+'" Power="'+str(block['percent'][0]/100)+'" pace="0"'+cad+'/>'

            elif block['percent'][0] < block['percent'][1]:
                if warm:
                    typ = 'Warmup'
                else:
                    typ = 'Ramp'

                return '\t\t<'+typ+' Duration="'+str(block['dur'])+'" PowerLow="'+str(block['percent'][0]/100)+'" PowerHigh="'+str(block['percent'][1]/100)+'" pace="0"'+cad+'/>'

            elif block['percent'][0] > block['percent'][1]:
                if warm:
                    typ = 'Cooldown'
                else:
                    typ = 'Ramp'
                return '\t\t<'+typ+' Duration="'+str(block['dur'])+'" PowerLow="'+str(block['percent'][0]/100)+'" PowerHigh="'+str(block['percent'][1]/100)+'" pace="0"'+cad+'/>'
        
        
        else:
            rep = str(block['repeats'])
            on_t = str(block['dur'][0])
            off_t = str(block['dur'][1])
            on_p = str(block['percent'][0])
            off_p = str(block['percent'][1])
            if block['cad'][0]>0:
                cad = ' Cadence="'+str(block['cad'][0])+'" CadenceResting="'+str(block['cad'][1])+'"'
            else:
                cad = ''
            return '<IntervalsT Repeat="'+rep+'" OnDuration="'+on_t+'" OffDuration="'+off_t+'" OnPower="'+on_p+'" OffPower="'+off_p+'" pace="0"'+cad+'/>'
            
        
    def generate(self, filename):       
        for block in self.blocks:
            if self.blocks.index(block)==0:
                self.zwo += '\n'
                self.zwo += self.syntax(block, warm = True)
            elif self.blocks.index(block) == len(self.blocks) -1:
                self.zwo += '\n'
                self.zwo += self.syntax(block, cool = True)
            else:
                self.zwo += '\n'
                self.zwo += self.syntax(block)
            
        self.zwo += '\n'
        
        f = open('foot.txt','r')
        foot = f.read()
        self.zwo += foot
        

        f = open(filename + '.zwo', 'w')
        f.write(self.zwo)
        f.close()
        
        
        #return self.zwo
    
    
    