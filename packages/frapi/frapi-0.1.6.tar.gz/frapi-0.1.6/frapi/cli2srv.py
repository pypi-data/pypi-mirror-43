# -*- coding: utf-8 -*-
# Frapi client, currently using tf-serving & tensorflow_model_server
# BIG CHENG, init 2018/12/05

from __future__ import print_function

import sys
import threading

import grpc
import numpy as np
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

import frapi.img_util as img_util

class _TaskSyncer(object):
  """Syncer for the prediction tasks."""

  def __init__(self, num_tests, concurrency):
    self._condition = threading.Condition()

    ## task control
    self._num_tests = num_tests
    self._done = 0

    self._fess = None ## result fes
    self._error = 0

    ## concurrency control
    self._concurrency = concurrency
    self._active = 0
    

  def wait_result(self):
    with self._condition:
      while self._done != self._num_tests:
        self._condition.wait()
      #return self._error / float(self._num_tests)
      
  def inc_done(self):
    with self._condition:
      self._done += 1
      self._condition.notify()

  def throttle(self):
    with self._condition:
      while self._active == self._concurrency:
        self._condition.wait()
      self._active += 1

  def dec_active(self):
    with self._condition:
      self._active -= 1
      self._condition.notify()
      
  def inc_error(self):
    with self._condition:
      self._error += 1

  def get_error_rate(self):
    with self._condition:
      while self._done != self._num_tests:
        self._condition.wait()
      return self._error / float(self._num_tests)

def _create_rpc_callback(label, task_syncer):
  """Creates RPC callback function.

  Args:
    label: The correct label for the predicted example.
    task_syncer: Counter for the prediction result.
  Returns:
    The callback function.
  """
  def _callback(result_future):
    """Callback function.

    Calculates the statistics for the prediction result.

    Args:
      result_future: Result future of the RPC.
    """
    exception = result_future.exception()
    if exception:
      task_syncer.inc_error()
      print("!!!")
      print(exception)
      response = None
    else:
      sys.stdout.write('.')
      sys.stdout.flush()
      response = np.array(
          result_future.result().outputs['embeddings'].float_val)
      #prediction = np.argmax(response)
      #print ("prediction=", prediction)
      #if label != prediction:
      #  task_syncer.inc_error()
    
    task_syncer.inc_done()
    task_syncer.dec_active()  ## concurrency control   
    task_syncer._fess = response  ## store result
  return _callback



def do_inference(hostport, work_dir, concurrency, num_tests, model, signature, imgs):
  """Tests PredictionService with concurrent requests.

  Args:
    hostport: Host:port address of the PredictionService.
    work_dir: The full path of working directory for test data set.
    concurrency: Maximum number of concurrent requests.
    num_tests: Number of test images to use.

  Returns:
    The classification error rate.

  Raises:
    IOError: An error occurred processing test data set.
  """
  channel = grpc.insecure_channel(hostport)
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  task_syncer = _TaskSyncer(num_tests, concurrency)
  ##task_syncer = _TaskSyncer(1, 1) ## run only 1

  for _ in range(num_tests):
    request = predict_pb2.PredictRequest()
    
    """
    if False: ## mnet
      request.model_spec.name = "mnet1"
      request.model_spec.signature_name = 'mnet1_signature'
    else: ## fnet
      request.model_spec.name = "fnet1"
      request.model_spec.signature_name = 'mnet1_signature'
    """
    request.model_spec.name = model
    request.model_spec.signature_name = signature
    
    request.inputs['input'].CopyFrom(tf.contrib.util.make_tensor_proto(imgs, shape=imgs.shape))
    
    task_syncer.throttle()  ## concurrency control
    
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(1, task_syncer))

  #task_syncer.get_error_rate() ## wait !!
  task_syncer.wait_result() ## wait !!
  #print ("err#=", task_syncer._error)
  return task_syncer._fess

"""
class _env:
  concurrency = 1   # maximum number of concurrent inference requests
  num_tests = 1   # Number of test images
  server = "127.0.0.1:8500" # PredictionService host:port
  work_dir = '/tmp' # Working directory
  model = "fnet1" ## or fnet1
  signature = "mnet1_signature" # the same as fnet
"""

class cli2srv:

  def __init__(self):
    self.concurrency = 1   # maximum number of concurrent inference requests
    self.num_tests = 1   # Number of test images
    self.server = "127.0.0.1:8500" # PredictionService host:port
    self.work_dir = '/tmp' # Working directory
    self.model = "fnet1" ## or fnet1
    self.signature = "mnet1_signature" # the same as fnet

  def img2fes(self, img):
    if (len(img.shape) == 3):
      imgs = img.reshape(1, 160, 160, 3)
    else:
      imgs = img
    return do_inference(self.server, self.work_dir, self.concurrency, self.num_tests, self.model, self.signature, imgs)

  def imgs2fess(self, imgs):
    n_imgs = imgs.shape[0]
    # todo: check n_imgs ...
    fess = do_inference(self.server, self.work_dir, self.concurrency, self.num_tests, self.model, self.signature, imgs)
    #print (fess.shape)
    return fess.reshape(n_imgs, 128)


## naive local test
if __name__ == "__main__":

  def utest_img2fes():
    img = img_util.file2img("coco1.png")
    print (img.shape) # (160,160,3)

    cli1 = cli2srv()
    if False: # mnet1
      cli1.server = "127.0.0.1:8600"
      cli1.model = "mnet1"

    fes = cli1.img2fes(img)
    print (str(fes))
    
  def utest_imgs2fess():
    imgs = img_util.files2imgs(["coco1.png", "coco7.png"])
    print (len(imgs.shape)) # (2, 160,160,3)
    fess = imgs2fess(imgs)
    print (str(fess))    
    #print (str(fess[1]))
    
  utest_img2fes()
  #utest_imgs2fess()
    
    
    



