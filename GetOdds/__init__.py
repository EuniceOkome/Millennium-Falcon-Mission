#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 09:29:28 2022

@author: euniceokomeobiang
"""

from .GetOdds import calcul


def getresults(milleniumFile, empireFile):
    
    return calcul(milleniumFile, empireFile).result()

