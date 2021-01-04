"""
Created on Fri Dec 18 14:45:27 2020

@author: maximilianreihn
"""


#TODO ramp und cooldown und warmup unterscheiden 
#TODO messages

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import numpy as np
import datetime
import json
import os

colors = ['black','grey', 'blue', 'green', 'yellow', 'orange', 'red']
zones = [0, 59, 75, 89, 104, 118, 9999]

class training(object):
    
    def __init__(self, workout_name= 'new workout', description='description', ftp = 315, offline = False):
        print(os.getcwd())
        if offline:
            path = ''
        else:
            path = 'src/worker/'

        f = open(path+'head.txt', 'r')
        head = f.read()
        
        head = head.replace('name_var', workout_name)
        head = head.replace('description_var', description)
        
        self.ftp = ftp
        self.zwo = head
        self.off = offline
        self.blocks = []
        self.messages = {}
        
    
    
    def text(self, id_block = 0, message = 'standard message', offset = 0):
        
        if self.blocks[id_block]['interval']:
            if offset >= (self.blocks[id_block]['dur']*self.blocks[id_block]['repeats']):
                print('\n##########\nOffset to big\n\n')
                raise FileNotFoundError
        else:
            if offset >= self.blocks[id_block]['dur']:
                print('\n##########\nOffset to big\n\n')
                raise FileNotFoundError
                
        if len(message)>31:
            print('\n##########\nMessage to long restirct to 31 chars!\n\n')
            raise FileNotFoundError
        
        if id_block < 0 or id_block > len(self.blocks):
            raise FileNotFoundError
        else:
            if id_block in self.messages.keys():
                if any([offset == k for k in self.messages[id_block]]):
                    raise FileNotFoundError
                else:
                    self.messages[id_block].append({'text': message, 'offset': offset})
            else:
                self.messages[id_block] = [{'text': message, 'offset': offset}]
                    
        
        
        
    def add(self, dur = 60, percent = 60, cadence = 0):
        if dur==0:
            print('\n##########\nDuration must be greater 0!\n\n')
            raise FileNotFoundError
            
            
        if type(percent) != list:
            percent = [percent, percent]
            
        self.blocks.append({'dur' : dur,
                    'percent' : percent,
                    'cad': [cadence]*2,
                           'interval':False})
        
        #self.plot()
        
    def interval(self, repeats = 5, on_dur = 30, on_perc = 100, off_dur = 30, off_perc = 60, on_cad=0, off_cad=0):
        if off_dur ==0 or on_dur ==0:
            print('\n##########\nDuration must be greater 0!\n\n')
            raise FileNotFoundError
            
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
        dis = []
        for i in range(len(self.blocks)):
            
            if i in self.messages.keys():
                for k in range(len(self.messages[i])):
                    '''
                    fig.add_trace(go.Scatter(x=[self.dt(sec + self.messages[i][k]['offset'])],
                                             y=[200],
                                             hoverinfo = 'text',
                                             text = self.messages[i][k]['text'],
                                             legendgroup = 'messages',
                                             showlegend = False,
                                             mode='markers+text',
                                             textposition="bottom right",
                                            line = dict(color='red')), secondary_y=False)
                    '''
                    
                    fig.add_trace(go.Scatter(x=[self.dt(sec + self.messages[i][k]['offset'])] * 2,
                                             y=[0, 200],
                                             hoverinfo = 'text',
                                             text = 'Offset: '+str(self.messages[i][k]['offset']) + '<br>' + self.messages[i][k]['text'],
                                             legendgroup = 'messages',
                                             showlegend = False,
                                             mode='lines+markers',
                                            line = dict(color='red')), secondary_y=False)
                
            
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
            
                if perc_diff > 0:
                    steig  = (self.blocks[i]['percent'][1] - self.blocks[i]['percent'][0]) / self.blocks[i]['dur']
                    dis.extend([self.blocks[i]['percent'][0] + k * steig for k in range(int(self.blocks[i]['dur']))])
            
            
            
                               
            for zo in range(diff):
                
                if self.blocks[i]['interval']:
                    dis.extend([self.blocks[i]['percent'][zo%2]] * int(self.blocks[i]['dur'][zo%2]))
                
                elif perc_diff == 0:
                    dis.extend([self.blocks[i]['percent'][0]] * int(self.blocks[i]['dur']))
                    
                
                
                if self.blocks[i]['interval']:
                    z_len = self.blocks[i]['dur'][zo%2]
                    temp_end = self.blocks[i]['percent'][zo%2]
                    temp_z = self.zone(self.blocks[i]['percent'][zo%2])
                    
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
                    
                    
                col = colors[temp_z -1 + int(2*up) + 1 - up]
                
                
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
                                        line = dict(color='black')), secondary_y=False)
                
                fig.add_trace(go.Scatter(x=x_scale[1:3],
                                         y=[k*self.ftp/100 for k in y_scale[1:3]],
                                         hoverinfo='none',
                                         showlegend = False,
                                         mode='lines',
                                        line = dict(color='rgba(0,0,0,255)')), secondary_y=True)
                
                
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
                
        
        average = self.avg_power(sec)
        norm = self.np_power(dis)
            
        fig.add_annotation(x=self.dt(300), y=150,
                text= "Average power "+str(int(average))+"w<br>" + "Normalised power (NP) "+str(int(norm))+"w<br>"+'Time '+self.dt(sec)[-7:-3]+'h',
                showarrow=False,bordercolor="blue",align='left',
        borderwidth=1, bgcolor="white")

        
        fig.update_xaxes(title_text='Zeit', type = 'date', tickangle = 0)

        if len(self.messages.keys()) > 0:
            range1 = [0, max([200, max([max(block['percent']) for block in self.blocks])])]
            range2 = [0, max([200, max([max(block['percent']) for block in self.blocks])]) * self.ftp/100]
        else:
            range1 = [0, max([150, max([max(block['percent']) for block in self.blocks])])]
            range2 = [0, max([150, max([max(block['percent']) for block in self.blocks])]) * self.ftp/100]

        fig.update_yaxes(title_text='% FTP', secondary_y=False, range = range1)
        fig.update_yaxes(title_text='Watt', secondary_y=True, showgrid = False, range = range2)

        if not self.off:
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return graphJSON

        else:
            plot(fig)  
        
        
    def np_power(self, dis):
        if len(dis)>30:
            dis = [self.ftp/100 * k for k in dis]
            dis_p4 = []
            for k in range(30, len(dis)):
                dis_p4.append(sum(dis[k-30:k]) / 30)
                
            dis_p4 = [np.power(k,4) for k in dis_p4]
            avg_p4 = sum(dis_p4) / len(dis_p4)
            
            norm = np.power(avg_p4, 0.25)
                
            return norm
        
        else:
            return 0
        
        
        
    def avg_power(self, sec):
        average = 0
        for bl in self.blocks:
            if bl['interval']:
                int_avg = (bl['percent'][0]*bl['dur'][0] + bl['percent'][1]*bl['dur'][1])/sum(bl['dur'])
                average += int_avg * (bl['repeats']*sum(bl['dur'])/sec)
            else:   
                int_avg = sum(bl['percent'])/2
                average += int_avg*(bl['dur']/sec)
        
        return average /100 *self.ftp
        
        
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
        
    
    def syntax(self, block, index, warm_cool = False):
        if not block['interval']:
            if block['cad'][0]>0:
                cad = ' Cadence="'+str(block['cad'][0])+'"'
            else:
                cad = ''

            if block['percent'][0] == 0 or block['percent'][1] == 0:
                end = self.message_syntax('FreeRide', index)
                return '\t\t<FreeRide Duration="'+str(int(block['dur']))+'" FlatRoad="170"'+cad+end

            elif block['percent'][0] == block['percent'][1]:
                end = self.message_syntax('SteadyState', index)
                return '\t\t<SteadyState Duration="'+str(int(block['dur']))+'" Power="'+str(block['percent'][0]/100.)+'"'+cad+end

            elif block['percent'][0] < block['percent'][1]:
                if warm_cool:
                    typ = 'Warmup'
                else:
                    typ = 'Ramp'
                end = self.message_syntax(typ, index)
                return '\t\t<'+typ+' Duration="'+str(int(block['dur']))+'" PowerLow="'+str(block['percent'][0]/100.)+'" PowerHigh="'+str(block['percent'][1]/100.)+'"'+cad+end

            elif block['percent'][0] > block['percent'][1]:
                if warm_cool:
                    typ = 'Cooldown'
                else:
                    typ = 'Ramp'
                end = self.message_syntax(typ, index)
                return '\t\t<'+typ+' Duration="'+str(int(block['dur']))+'" PowerLow="'+str(block['percent'][0]/100.)+'" PowerHigh="'+str(block['percent'][1]/100.)+'"'+cad+end
        
        
        else:
            rep = str(block['repeats'])
            on_t = str(block['dur'][0])
            off_t = str(block['dur'][1])
            on_p = str(block['percent'][0]/100.)
            off_p = str(block['percent'][1]/100.)
            if block['cad'][0]>0:
                cad = ' Cadence="'+str(block['cad'][0])+'" CadenceResting="'+str(block['cad'][1])+'"'
            else:
                cad = ''
            end = self.message_syntax('IntervalsT', index)
            return '\t\t<IntervalsT Repeat="'+rep+'" OnDuration="'+on_t+'" OffDuration="'+off_t+'" OnPower="'+on_p+'" OffPower="'+off_p+'"'+cad+end
            
        

    def message_syntax(self, opener, index):
        if index in self.messages.keys():
            end = '>\n'
            
            for message in self.messages[index]:
                end += '\t\t\t<textevent timeoffset="'+str(message['offset'])+'" message="'+message['text']+'"/>\n'
            
            end += '\t\t</'+opener+'>'
            return end
        else:
            return '/>'
        
    def generate(self, filename): 
        k=0
        for block in self.blocks:
            if (self.blocks.index(block)==0) or (self.blocks.index(block) == len(self.blocks) -1):
                self.zwo += '\n'
                self.zwo += self.syntax(block, k, warm_cool = True)
            else:
                self.zwo += '\n'
                self.zwo += self.syntax(block, k)
            k += 1
            
        self.zwo += '\n'
        
        if self.off:
            path = ''
        else:
            path = 'src/worker/'
            
        f = open(path + 'foot.txt','r')
        foot = f.read()
        self.zwo += foot
        
        print(os.getcwd())
        print(filename + '.zwo', 'w')
        f = open(filename + '.zwo', 'w')
        f.write(self.zwo)
        f.close()

        
        
        #return self.zwo
    
    
    