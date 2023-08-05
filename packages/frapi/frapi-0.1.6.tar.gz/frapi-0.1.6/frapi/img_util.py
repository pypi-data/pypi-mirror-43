# -*- coding: utf-8 -*-
# Frapi image utility, support normalization/whitening
# BIG CHENG, init 2019/03/07
# BIG CHENG, bug-fixed: scipy.misc.imread need Pillow installed !!!

from __future__ import print_function

import numpy as np
#from scipy import misc
from PIL import Image

img_size = 160

def prewhiten(x):
  mean = np.mean(x)
  std = np.std(x)
  std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
  y = np.multiply(np.subtract(x, mean), 1/std_adj)
  return y  

def to_rgb(img):
  w, h = img.shape[0], img.shape[1]
  ret = np.zeros((w, h, 3), dtype=np.uint8)
  ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img[:, :, 0]
  return ret

def _file2img(fname):
  ## todo: check file
  #img = misc.imread(fname)
  img = Image.open(fname)
  return img, np.array(img)
  #Image.fromarray(img )  ## reverse

## conver image for fr
# whitening
# to rgb (if gray-scale)
# remove alpha layer
def _img2img4fr(img, do_prewhiten=True):
    if len(img.shape) == 2: ## mono
      img = img.reshape(img_size, img_size, 1)
    if img.shape[2] <= 2:
      img = to_rgb(img) 
    if do_prewhiten:
      img = prewhiten(img)  
    if img.shape[2] == 4: ## if image has alpha layer
      img = img [:, :, :3]
    return img.astype(np.float32)

def load_data(image_paths, img_size, do_prewhiten=True):
  nrof_samples = len(image_paths)
  images = np.zeros((nrof_samples, img_size, img_size, 3))
  for i in range(nrof_samples):
    #img = misc.imread(image_paths[i])
    _, img = _file2img(image_paths[i])
    if img.shape[2] == 2:
        img = to_rgb(img) 
    if do_prewhiten:
        img = prewhiten(img)  
    if img.shape[2] == 4: ## if image has alpha layer
        img = img [:, :, :3] 
    images[i,:,:,:] = img

  return images

def file2img(path):
  images = load_data([path], img_size)
  return images[0].astype(np.float32)          

def files2imgs(paths):
  images = load_data(paths, img_size)
  return images.astype(np.float32)



## naive local test
if __name__ == "__main__":
  
  def utest_img():

    img = file2img("./coco1.png")
    #print(img)
    print(img.shape)

  def utest_imgs():

    paths = ["./coco1.png"]
    print (paths[0])

    imgs = files2imgs(paths)
    #print(imgs)
    print(imgs.shape)

  utest_img()
  utest_imgs()



