"""
Test a learner.  (c) 2015 Tucker Balch
"""

import sys 
import numpy as np
import math
import LinRegLearner as lrl
from time import time

if __name__=="__main__":
  if len(sys.argv) == 2:
    inf = open(sys.argv[1])
  else:
    inf = open('Data/ripple.csv')
  data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

  # compute how much of the data is training and testing
  train_rows = math.floor(0.6* data.shape[0])
  test_rows = data.shape[0] - train_rows

  # separate out training and testing data
  trainX = data[:train_rows,0:-1]
  trainY = data[:train_rows,-1]
  testX = data[train_rows:,0:-1]
  testY = data[train_rows:,-1]

  # create a learner and train it
  t0 = time()
  learner = lrl.LinRegLearner() # create a LinRegLearner
  learner.addEvidence(trainX, trainY) # train it
  t1 = time()

  print "---{:^15}---".format("LRL Tester")
  print "Train Time: ", t1-t0
  # evaluate in sample
  predY = learner.query(trainX) # get the predictions
  t2 = time()
  rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
  print
  print "In sample results"
  print "RMSE: ", rmse
  c = np.corrcoef(predY, y=trainY)
  print "corr: ", c[0,1]
  print "Time: ", t2-t1
  print

  # evaluate out of sample
  predY = learner.query(testX) # get the predictions
  t3 = time()
  rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
  print "Out of sample results"
  print "RMSE: ", rmse
  c = np.corrcoef(predY, y=testY)
  print "corr: ", c[0,1]
  print "Time: ", t3-t2
