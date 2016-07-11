"""
Test a learner.  (c) 2015 Tucker Balch
"""

import sys
import numpy as np
import math
import matplotlib.pyplot as plt
from time import time

def test_learner(k, trainX, trainY, testX, testY):
    # create a learner and train it
    t0 = time()
    learner = KNNLearner(k) 
    learner.addEvidence(trainX, trainY) # train it
    t1 = time()
    print "---{:^15}---".format("KNN Tester")
    print "Train Time: ", t1-t0
    print

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    t2 = time()
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print "In sample results"
    print "RMSE: ", rmse
    c1 = np.corrcoef(predY, y=trainY)
    print "corr: ", c1[0,1]
    print "Time: ", t2-t1
    print

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    t3 = time()
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print "Out of sample results"
    print "RMSE: ", rmse
    c2 = np.corrcoef(predY, y=testY)
    print "corr: ", c2[0,1]
    print "Time: ", t3-t2
    print

def plot_overfit(trainX, trainY, testX, testY, maxK=50):
    out_of_sample_error = []
    in_sample_error = []
    for k in range(1,maxK+1):
        # create a learner and train it
        t0 = time()
        learner = KNNLearner(k) 
        learner.addEvidence(trainX, trainY) # train it
        t1 = time()

        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        t2 = time()
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        print "---     K = {}     ---".format(k)
        print "Train Time: ", t1-t0; print
        print "In sample results"
        print "RMSE: ", rmse
        print "Time: ", t2-t1; print
        in_sample_error.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        t3 = time()
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print "Out of sample results"
        print "RMSE: ", rmse
        print "Time: ", t3-t2; print
        out_of_sample_error.append(rmse)

    out_of_sample_error = np.array(out_of_sample_error)
    in_sample_error = np.array(in_sample_error)
    plt.figure()
    ax = plt.gca()
    ax.plot(range(1,100), out_of_sample_error, 'b-', label='Out of Sample')
    ax.plot(range(1,100), in_sample_error, 'g-', label='In Sample')
    ax.set_xlabel("K Value")
    ax.set_ylabel("RMS Error")
    plt.show()

if __name__=="__main__":
    if __package__ == None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from learners.KNNLearner import KNNLearner
        from learners.BagLearner import BagLearner
    else:
        from ..learners.KNNLearner import KNNLearner

    if len(sys.argv) == 2:
        inf = open(sys.argv[1])
    else:
      inf = open(path.dirname(path.abspath(__file__)) + '/ripple.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    # Choose to do single test or plot learning curve over multiple K
    #test_learner(3, trainX, trainY, testX, testY)
    plot_overfit(trainX, trainY, testX, testY, 20)
