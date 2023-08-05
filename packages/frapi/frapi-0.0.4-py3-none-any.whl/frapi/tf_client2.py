#!/usr/bin/env python2.7

## BIG CHENG, init from tf-serving/client, 2018/12/05

"""A client that talks to tensorflow_model_server loaded with FR model.

The client queries the service with a test images to get predictions, and display the running time.

Typical usage example:

    tf_client2.py --num_tests=100 --server=localhost:8500
"""

from __future__ import print_function

import sys
import threading

# This is a placeholder for a Google-internal import.

import grpc
import numpy
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
#import mnist_input_data

import time

tf.app.flags.DEFINE_integer('concurrency', 1,
                            'maximum number of concurrent inference requests')
tf.app.flags.DEFINE_integer('num_tests', 1, 'Number of test images')
tf.app.flags.DEFINE_string('server', '', 'PredictionService host:port')
tf.app.flags.DEFINE_string('work_dir', '/tmp', 'Working directory. ')
FLAGS = tf.app.flags.FLAGS


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
      response = numpy.array(
          result_future.result().outputs['embeddings'].float_val)
      #prediction = numpy.argmax(response)
      #print ("prediction=", prediction)
      #if label != prediction:
      #  task_syncer.inc_error()
    
    task_syncer.inc_done()
    task_syncer.dec_active()  ## concurrency control   
    task_syncer._fess = response  ## store result
  return _callback



def do_inference(hostport, work_dir, concurrency, num_tests):
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
  #test_data_set = mnist_input_data.read_data_sets(work_dir).test
  image = numpy.load("coco1.npy")
  print (image.shape)
  image = numpy.reshape(image, (1, 160, 160, 3))
  print (image.shape, image.size)

  channel = grpc.insecure_channel(hostport)
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  task_syncer = _TaskSyncer(num_tests, concurrency)
  ##task_syncer = _TaskSyncer(1, 1) ## run only 1

  t1 = time.time()
  for _ in range(num_tests):
    request = predict_pb2.PredictRequest()
    #request.model_spec.name = tf.saved_model.tag_constants.SERVING
    
  if False: ## mnet
    request.model_spec.name = "mnet1"
    request.model_spec.signature_name = 'mnet1_signature'
  else: ## fnet
    request.model_spec.name = "fnet1"
    request.model_spec.signature_name = 'mnet1_signature'
    
    #image, label = test_data_set.next_batch(1)
    
    request.inputs['input'].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, shape=[1, 160, 160, 3]))
    #request.inputs['phase_train'].CopyFrom(
    #    tf.contrib.util.make_tensor_proto(False, dtype=tf.bool, shape=[1]))
    
    task_syncer.throttle()  ## concurrency control
    
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(1, task_syncer))

  #task_syncer.get_error_rate() ## wait !!
  task_syncer.wait_result() ## wait !!
  t2 = time.time()
  print ("time=", t2-t1)  
  print ("err#=", task_syncer._error)  
  return str(task_syncer._fess)
  

#def do_inference_loop(hostport, work_dir, concurrency, num_tests, n_loop=10):
def do_inference_loop(hostport, work_dir, concurrency, num_tests):
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
  #test_data_set = mnist_input_data.read_data_sets(work_dir).test
  image = numpy.load("coco1.npy")
  print (image.shape)
  image = numpy.reshape(image, (1, 160, 160, 3))
  print (image.shape, image.size)

  channel = grpc.insecure_channel(hostport)
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  
  task_syncer = _TaskSyncer(num_tests, concurrency)
  ##task_syncer = _TaskSyncer(1, 1) ## run only 1

  request = predict_pb2.PredictRequest()
  #request.model_spec.name = tf.saved_model.tag_constants.SERVING
  
  if False: ## mnet
    request.model_spec.name = "mnet1"
    request.model_spec.signature_name = 'mnet1_signature'
  else: ## fnet
    request.model_spec.name = "fnet1"
    request.model_spec.signature_name = 'mnet1_signature'
    
  #image, label = test_data_set.next_batch(1)
  
  request.inputs['input'].CopyFrom(
      tf.contrib.util.make_tensor_proto(image, shape=[1, 160, 160, 3]))
  #request.inputs['phase_train'].CopyFrom(
  #    tf.contrib.util.make_tensor_proto(False, dtype=tf.bool, shape=[1]))
  #task_syncer.throttle()
  
  t1 = time.time()
  for i in range(num_tests):
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(1, task_syncer))

    #task_syncer.get_error_rate() ## wait !!
  task_syncer.wait_result() ## wait !!
  t2 = time.time()
  print ("time=", t2-t1)

    
  return str(task_syncer._fess)
  
  
def main(_):
  if not FLAGS.server:
    print('please specify server host:port')
    return
  result = do_inference(FLAGS.server, FLAGS.work_dir, FLAGS.concurrency, FLAGS.num_tests)
  #result = do_inference(FLAGS.server, FLAGS.work_dir, 1, 2)
  #result = do_inference_loop(FLAGS.server, FLAGS.work_dir, FLAGS.concurrency, FLAGS.num_tests)
  #result = do_inference_loop(FLAGS.server, FLAGS.work_dir, 1, 100) ## time= 1.1436009407
  print('\nInference result: %s' % (result))  ## 3000.npy -> 6


if __name__ == '__main__':
  tf.app.run()
