# -*- coding: utf-8 -*-
# Facade interface for Face Detection
# BIG CHENG, init 2019/03/08

from __future__ import print_function

import dlib
import numpy as np
#from scipy import misc
from PIL import Image

class fd_dlib:

  def __init__(self):
    self.detector = dlib.get_frontal_face_detector()

  def detect(self, fname):
    ## todo check 
    #img = misc.imread(fname)
    img = Image.open(fname)
    img = np.array(img)
    #Image.fromarray(img )
    print (img.shape)
    dets = self.detector(img, 0)
    
    print(dets[0])


"""
def run_crop_face():

    faces_folder_path = "coco1.png"
    detector = dlib.get_frontal_face_detector()
    f = faces_folder_path

    print("Processing file: {}".format(f))
    img = misc.imread(f)

    dets = detector(img, 0)
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
 
    #io.imsave(faces_result_path, img)
"""

## naive local test
if __name__ == "__main__":

  def utest_fd():
    fd1 = fd_dlib()
    #img = img_util.file2img("coco1.png")
    fd1.detect("coco1.png")

  #run_crop_face()
  utest_fd()

"""
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


  fr1 = fr_facade()
  
  def utest_reg():
    fname_imgs = ["coco1.png", "coco7.png", "nicole1.png", "nicole7.png"]
    names = ["coco"]*2 + ["nicole"]*2
    fr1.files2reg(fname_imgs, names)
    print (fr1.fess_reg.shape)

  def utest_inf():
    fname_imgs = ["coco1.png", "nicole1.png"]
    names = ["coco"] + ["nicole"]
    fr1.files2reg(fname_imgs, names)
    print(fr1.file2inf("coco7.png"))
    print(fr1.file2inf("nicole7.png"))
  
  #utest_reg()
  utest_inf()

"""    

