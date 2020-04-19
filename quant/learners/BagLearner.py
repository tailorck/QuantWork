import numpy as np
import KNNLearner as knn
import LinRegLearner as lrl
import pandas as pd

class BagLearner(object):
  
  def __init__(self, learner = knn.KNNLearner, kwargs={"k":3}, bags=20, boost=False):
    self.learners = [learner(**kwargs) for _ in range(bags)] 
  
  def addEvidence(self, dataX, dataY):
    """
    train learners using random selection with replacement
    
    Parameters
    ----------
      dataX: X values of data to add
      dataY: the Y training values
    """
    for model in self.learners:
      rand_indices = np.random.randint(len(dataX)-1, size = len(dataX))
      randX_data = np.array([dataX[i] for i in rand_indices])
      randY_data = np.array([dataY[i] for i in rand_indices])
      model.addEvidence(randX_data, randY_data)
      
  def query(self, testX):
    """
    Returns an array of predictions for each feature in input matrix

    Parameters
    ----------
      testX: a numpy matrix of feature values to query model with. 
    """
    return pd.DataFrame(np.mean([model.query(testX).values for model in self.learners], axis=0), index = model.query(testX).index)
    

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
