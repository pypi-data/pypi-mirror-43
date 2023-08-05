# -*- coding: utf-8 -*-
# Frapi image utility, support normalization/whitening
# BIG CHENG, init 2019/03/07
# BIG CHENG, bug-fixed: scipy.misc.imread need Pillow installed !!!

from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import os
import sys
import math

from scipy import misc

#from tensorflow.python.platform import gfile
#import re

image_size = 160

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y  

def crop(image, random_crop, image_size):
    if image.shape[1]>image_size:
        sz1 = int(image.shape[1]//2)
        sz2 = int(image_size//2)
        if random_crop:
            diff = sz1-sz2
            (h, v) = (np.random.randint(-diff, diff+1), np.random.randint(-diff, diff+1))
        else:
            (h, v) = (0,0)
        image = image[(sz1-sz2+v):(sz1+sz2+v),(sz1-sz2+h):(sz1+sz2+h),:]
    return image
  
def flip(image, random_flip):
    if random_flip and np.random.choice([True, False]):
        image = np.fliplr(image)
    return image

def to_rgb(img):
    #print img
    w, h = img.shape[0], img.shape[1]
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img[:, :, 0]
    #print ret
    return ret



def load_data(image_paths, do_random_crop, do_random_flip, image_size, do_prewhiten=True):

    nrof_samples = len(image_paths)
    images = np.zeros((nrof_samples, image_size, image_size, 3))
    for i in range(nrof_samples):
        img = misc.imread(image_paths[i])
        #print img.shape
        #if img.ndim == 2:
        #    img = to_rgb(img)
        if img.shape[2] == 2:
            img = to_rgb(img) 
        if do_prewhiten:
            img = prewhiten(img)
        img = crop(img, do_random_crop, image_size)
        img = flip(img, do_random_flip)

        if img.shape[2] == 4:
            img = img [:, :, :3] 
        images[i,:,:,:] = img

    return images



def file2img(paths):

    images = load_data(paths, False, False, image_size)
    print (images)
    return images.astype(np.float32)          


## need to enter virtualenv !!!

if __name__ == "__main__":


   
    def utest_img():

        paths = ["./coco1.png"]
        print (paths[0])

        imgs = file2img(paths)
        print(imgs)


    utest_img()



