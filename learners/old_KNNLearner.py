import numpy as np
import pandas as pd
from scipy.spatial import distance
import pdb

class KNNLearner(object):
  
  def __init__(self, k = 3):
    self.k = k
  
  def addEvidence(self, dataX, dataY):
    """
    Adds training data to learner
    
    Parameters
    ----------
      dataX: X values of data to add
      dataY: the Y training values
    """
    self.trainX = dataX
    self.trainY = dataY

  def query(self, testX):
    """
    Returns an array of predictions for each feature in input matrix

    Parameters
    ----------
      testX: a numpy matrix of feature values to query model with. 
    """
    trainX = self.trainX
    neighbors = distance.cdist(testX, trainX, 'euclidean')
    indices = np.argsort(neighbors, axis=1)
    NN = [row[0:self.k].tolist() for row in indices]
    #date_indices = [item for sublist in NN for item in sublist]
    #dates = testX.index[date_indices]
    dates = testX.index
    pdb.set_trace()
    return pd.DataFrame([np.mean([self.trainY[i] for i in row], axis=1) for row in testX.index[NN]], index=dates)
    

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
