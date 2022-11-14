#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:55:33 2022

@author: euniceokomeobiang
"""

import numpy as np
import json
import sqlite3
import pandas as pd
import copy
import os
from pathlib import Path


# Part I: Get all the possible routes .................................................................


class routes():
    def __init__(self, universe, departure, arrival, fuel, count):
        
        planets = np.unique(np.concatenate((universe.origin, universe.destination))).tolist()
        self.neigh = {}
        planets.remove(arrival)
        
        for x in planets:
            self.neigh[x] = pd.concat([universe[universe.origin==x].iloc[:,1:3].set_axis(['neighbors','time'], axis=1),
                       universe[universe.destination==x].iloc[:,[0,2]].set_axis(['neighbors','time'], axis=1)])
            self.neigh[x]['fuel'] = [0]*self.neigh[x].shape[0]
            self.neigh[x] = self.neigh[x].append({'neighbors':x, 'time':1, 'fuel':6}, ignore_index=True)
            self.neigh[x].index = self.neigh[x].neighbors
            
        self.routes = [] ; self.route = {'route':[[0,departure]], 'fuel':fuel, 'count':count}
        self.departure = departure ; self.arrival = arrival ; self.count = count
        
    def paths(self):
        
        for go in self.neigh[self.departure].neighbors:
            pathact = copy.deepcopy(self.route)
            self.nextPlanet(pathact, self.departure, go)
        return self.routes
    
    def nextPlanet(self, path, leave, go):
        if (path['count']>=self.neigh[leave].loc[go, 'time']):
        
            if ((path['fuel'] >= self.neigh[leave].loc[go, 'time']) or 
                (self.neigh[leave].loc[go, 'fuel']!=0)):
                path['count'] = path['count'] - self.neigh[leave].loc[go, 'time']
                path['route'].append([self.count - path['count'], go])
                path['fuel'] = min(6, path['fuel']
                                   - self.neigh[leave].loc[go, 'time']*(self.neigh[leave].loc[go, 'fuel']==0)
                                   + self.neigh[leave].loc[go, 'fuel'])
            
                if (go != self.arrival):
                    leave = go
                    for go in self.neigh[leave].neighbors:
                        pathact = copy.deepcopy(path)
                        self.nextPlanet(pathact, leave, go)
                else: self.routes.append(path)



# Part II: Get the odds ..................................................................................

class odds():
    def __init__(self, routes, hunting):
        self.routes = routes ; self.hunting = hunting ; self.odds = []
        
    def odd(self):
        for route in self.routes:
            k = 0
            for r in route['route']:
                if ((r[0] in self.hunting['day']) and (self.hunting['planet'][self.hunting['day'].index(r[0])]==r[1])):
                    k = k+1
                    r.append('BH')
                else: r.append('Clear')
            route['odd'] = (1-sum([(9**(i-1))/(10**i) for i in range(1, k+1)]))*100
            self.odds.append(route['odd'])
        return self.routes, np.array(self.odds)



# Part III: Let's run it all ..............................................................................

class calcul():
    def __init__(self, milleniumFile, empireFile):
        # Read the routes
        with open(milleniumFile, encoding='utf-8') as json_file:
            self.backData1 = json.load(json_file)
        cnx = sqlite3.connect(os.path.join(Path(milleniumFile).parent.absolute(), self.backData1['routes_db']))
        table = cnx.cursor().execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.universe = pd.read_sql_query('SELECT * FROM {}'.format(''.join(table.fetchone())), cnx)
        self.universe = self.universe.set_axis(['origin', 'destination', 'time'], axis=1)
        
        # Read the hunting
        with open(empireFile, encoding='utf-8') as json_file:
            self.backData2 = json.load(json_file)
        
        self.hunting = {'planet':[], 'day':[]}
        for h in self.backData2['bounty_hunters']:
            planet, day = h.values()
            self.hunting['planet'].append(planet) ; self.hunting['day'].append(day)

        self.routes = routes(self.universe, self.backData1['departure'], self.backData1['arrival'], self.backData1['autonomy'], self.backData2['countdown']).paths()
        self.routes, self.odds = odds(self.routes, self.hunting).odd()
        
        self.res = [0]
        
    def result(self):

        if (len(self.odds) != 0): 
            self.res[0] = max(self.odds) ; self.res.append([])
            indices = np.where(self.odds == max(self.odds))[0].tolist()
            for i in indices:
                route = []
                prev = self.backData1['departure']
                for j in range(1,len(self.routes[i]['route'])):
                    if (prev != self.routes[i]['route'][j][1]):
                        r = 'travel from {} to {}'.format(prev, self.routes[i]['route'][j][1])
                    else: r = 'refuel on {}'.format(prev)
                    if (self.routes[i]['route'][j][2] == 'BH'): r = r + ' with 10% chance of being captured on day {} on {} - '.format(self.routes[i]['route'][j][0], self.routes[i]['route'][j][1])
                    else: r = r + ' - '
                    route.append(r) ; prev = self.routes[i]['route'][j][1]
                route[j-1] = route[j-1].strip(' - ')+'.'
                self.res[1].append(route)
            
        return self.res
            
