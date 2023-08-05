# -*- coding: utf-8 -*-
# Frapi helper, support similarity, confusion matrix, etc. calculation from features
# BIG CHENG, init 2019/03/08

from __future__ import print_function

import numpy as np

def fes2sim(fes1, fes2):
  #todo: check fes
  return np.inner(fes1, fes2)

"""
def fess2similarity(fess1, fess2):
  #todo: check fes
  return np.inner(fes1, fes2))
"""
  
def fess2confusion(fess):
  #todo: check fess
  return np.round(np.inner(fess, fess)*100).astype(int)
  
  
def find_max_sim(fes, fess):
  #todo: check fess
  sims = np.inner(fes, fess)
  idx = np.argmax(sims)
  return idx, sims[idx]
  
