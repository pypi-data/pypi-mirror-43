# -*- coding: utf-8 -*-
# Facade interface for Face Recognition
# BIG CHENG, init 2019/03/08

from __future__ import print_function

import numpy as np
#import frapi
import frapi.cli2srv as cli2srv
import frapi.img_util as img_util
import frapi.math_helper as math_helper
import frapi.file_util as file_util

def file2fes(fname):
  ## todo: check fname
  img = img_util.file2img(fname)
  fes = cli2srv.img2fes(img)
  return fes
  
class fr_facade:
  
  def __init__(self):
    self.fess_reg = None
    self.names_reg = None
    if False: ## mnet1
      cli2srv._env.server = "127.0.0.1:8600"
      cli2srv._env.model = "mnet1"
      
  def files2reg(self, fnames, names):
    ## todo: check fnames, names ...
    imgs = img_util.files2imgs(fnames)
    #print (imgs.shape)
    self.names_reg = names
    self.fess_reg = cli2srv.imgs2fess(imgs)

  ## ref. to files2reg
  def imgs2reg(self, imgs, names):
    #print (imgs.shape)
    ## todo: check imgs shape, names ...
    self.names_reg = names
    self.fess_reg = cli2srv.imgs2fess(imgs)
    
  #todo:
  #def dir2reg():

  def file2inf(self, fname):
    ## todo: check fname
    fes = file2fes(fname)
    idx, sim = math_helper.find_max_sim(fes, self.fess_reg)
    ## todo: check idx
    return self.names_reg[idx], sim
    

## naive local test
if __name__ == "__main__":
  import os

  fr1 = fr_facade()
  dir_base = "../imgs"
  
  def utest_reg():
    #dir_base = "../imgs"
    #fname_imgs = ["coco1.png", "coco7.png", "nicole1.png", "nicole7.png"]
    #path_imgs = [os.path.join(dir_base, fname) for fname in fname_imgs]
    path_imgs = file_util.list_files(dir_base)
    print (path_imgs)
    names = ["coco"]*2 + ["nicole"]*2
    print (names)
    fr1.files2reg(path_imgs, names)
    print (fr1.fess_reg.shape)

  def utest_inf():
    path_imgs = file_util.fnames2paths(dir_base, ["coco1.png", "nicole1.png"])
    names = ["coco"] + ["nicole"]
    fr1.files2reg(path_imgs, names)
    path_unknowns = file_util.fnames2paths(dir_base, ["coco7.png", "nicole7.png"])
    print(fr1.file2inf(path_unknowns[0]))
    print(fr1.file2inf(path_unknowns[1]))
  
  #utest_reg()
  utest_inf()


