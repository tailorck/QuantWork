"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
from time import time
from LinRegLearner import LinRegLearner 
from KNNLearner import KNNLearner
from BagLearner import BagLearner

if __name__=="__main__":
    inf = open('Data/ripple.csv')
    #inf = open('Data/mydata.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]
    
    knn = KNNLearner(k=3)
    lrl = LinRegLearner()
    knnbag = BagLearner(learner = KNNLearner, kwargs={"k":1}, bags = 100)
    lrlbag = BagLearner(learner = LinRegLearner, kwargs = {}, bags = 100)
    
    learners = [knn, lrl, knnbag, lrlbag]
    names = ["KNN", "LinReg", "KNNBag", "LinRegBag"]
    for i in range(4):
      t0 = time() 
      # create a learner and train it
      learner = learners[i]
      learner.addEvidence(trainX, trainY) # train it
      t1 = time()

      print "---{:^15}---".format(names[i])
      print "Training Time: ", t1-t0
      print 
      # evaluate in sample
      predY = learner.query(trainX) # get the predictions
      t2 = time()
      rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
      print "In sample results"
      print "RMSE: ", rmse
      c = np.corrcoef(predY, y=trainY)
      print "corr: ", c[0,1]
      print "Time: ", t2-t1 

      # evaluate out of sample
      predY = learner.query(testX) # get the predictions
      t3 = time()
      rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
      print
      print "Out of sample results"
      print "RMSE: ", rmse
      c = np.corrcoef(predY, y=testY)
      print "corr: ", c[0,1]
      print "Time: ", t3-t2
      print
