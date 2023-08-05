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

import frapi_image as fimg

class _env:
  concurrency = 1   # maximum number of concurrent inference requests
  num_tests = 1   # Number of test images
  server = "127.0.0.1:8500" # PredictionService host:port
  work_dir = '/tmp' # Working directory
  

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



def do_inference(hostport, work_dir, concurrency, num_tests, image):
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
    
  if False: ## mnet
    request.model_spec.name = "mnet1"
    request.model_spec.signature_name = 'mnet1_signature'
  else: ## fnet
    request.model_spec.name = "fnet1"
    request.model_spec.signature_name = 'mnet1_signature'
    
    #image, label = test_data_set.next_batch(1)
    
    request.inputs['input'].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, shape=[1, 160, 160, 3]))
    
    task_syncer.throttle()  ## concurrency control
    
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(1, task_syncer))

  #task_syncer.get_error_rate() ## wait !!
  task_syncer.wait_result() ## wait !!
  print ("err#=", task_syncer._error)  
  return task_syncer._fess

def img2fes(img):
  #FLAGS.server = "127.0.0.1:8500"
  env = _env()
  return do_inference(env.server, env.work_dir, env.concurrency, env.num_tests, img)

## main
if __name__ == "__main__":

  def utest_img2fes():
  
    def file2img1(fname):
      ## todo: add file check
      img = np.load(fname)
      print (img.shape)
      return img

    def prepare_img():
      if False: # npy
        return file2img1("coco1.npy")
      else:
        imgs = fimg.file2img(["coco1.png"])
        return imgs[0]

    img = prepare_img()
    print (img)
    fes = img2fes(img)
    print (str(fes))
    
  utest_img2fes()
    
    
    



