# -*- coding: utf-8 -*-
# Frapi image utility, support normalization/whitening
# BIG CHENG, init 2019/03/07
# BIG CHENG, bug-fixed: scipy.misc.imread need Pillow installed !!!

from __future__ import print_function

import os
from glob import glob

def fname2path(path_root, fname):
  return os.path.join(path_root, fname)

def fnames2paths(path_root, fnames):
  return [os.path.join(path_root, fname) for fname in fnames]

def list_subdirs(path_root): ## similar to os.walk
  ## todo: check path_root
  paths = []
  for fname in sorted(os.listdir(path_root)):
    path = os.path.join(path_root, fname)
    if os.path.isdir(path):
        paths += [path]
            
  return paths
  
def list_files(path_root): ## similar to os.walk
  ## todo: check path_root
  paths = []
  for fname in sorted(os.listdir(path_root)):
    path = os.path.join(path_root, fname)
    if os.path.isfile(path):
        paths += [path]
            
  return paths  
  
"""
def iter_files(path_root): ## similar to os.walk
    for fname1 in sorted(os.listdir(path_root)):
        path1 = os.path.join(path_root, fname1)
        if os.path.isfile(path1):
            yield fname1, path1

### list all level-1 dirs w/ their files under root (flatten)
def iter_tree1(path_root):
    for fname1, path1 in file_iter.iter_dirs(path_root):
        for fname2, path2  in file_iter.iter_files(path1):
            yield fname1, path1, fname2, path2

### list all image under root (flatten)
def list_imgs(path_root):
    for fname1, path1, fname2, path2 in file_iter.iter_tree1(path_root):
        print (fname1, path2)
"""


## naive local test
if __name__ == "__main__":

  def utest_list_subdirs():  
    print(list_subdirs(".."))
    
  
  utest_list_subdirs()
  



