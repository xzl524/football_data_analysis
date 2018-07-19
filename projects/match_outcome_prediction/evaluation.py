# coding: utf-8

from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.metrics import accuracy_score
from footballmodels import PoissonRegression
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from scipy.stats import skellam  # skellam distribution

def avg_interest_rate_per_match(y_true, y_pred, odds_matrix):
    """
    Parameters:
    ----------
    y_true: 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) labels.
    y_pred: 1d array-like, or label indicator array / sparse matrix
        Predicted labels.
    odds_matrix: 2d array-like with dimension of [:,3].
    
    Returns
    -------
    avg_inter: float
        Average Interest Per Match: the amount of money can be made, 
        on average, if 1 dollar is bet for each match
    """
    
    ohe = OneHotEncoder(n_values=3, sparse=False)
    y_pred_oh = ohe.fit_transform(y_pred.reshape(len(y_pred), 1))
    y_true_oh = ohe.fit_transform(y_true.reshape(len(y_true), 1))
    avg_inter = np.mean(np.sum(np.multiply(odds_matrix, np.multiply(y_true_oh, y_pred_oh)), axis=1))-1
    
    return avg_inter

def poi_regression_multiple_evaluation(X_home, X_away, hgoal, agoal, y, odds, num_rep=100, test_size=0.2):
    
    pred_acc_train = []
    pred_acc_test = []
    avg_int_rate_train = []
    avg_int_rate_test = []
    
    for i in tqdm(np.arange(num_rep), desc='Start model repeatability test', unit='tests'):
        
        Xhometrain, Xhometest, Xawaytrain, Xawaytest, hgoaltrain, hgoaltest, agoaltrain, agoaltest, ytrain, ytest, oddstrain, oddstest = train_test_split(X_home, X_away, hgoal, agoal, y, odds, test_size = test_size, stratify=y)
        
        # Fit poisson regression model
        poi = PoissonRegression()
        poi.fit(Xhometrain, Xawaytrain, hgoaltrain, agoaltrain)
                
        # Encoding result
        ypredtrain = poi.predict(Xhometrain, Xawaytrain)
        ypredtest = poi.predict(Xhometest, Xawaytest)
        
        pred_acc_train.append(accuracy_score(ytrain, ypredtrain))
        pred_acc_test.append(accuracy_score(ytest, ypredtest))
        
        avg_int_rate_train.append(avg_interest_rate_per_match(ytrain, ypredtrain, oddstrain))
        avg_int_rate_test.append(avg_interest_rate_per_match(ytest, ypredtest, oddstest))
    
    pred_acc_train = np.array(pred_acc_train)
    pred_acc_test = np.array(pred_acc_test)
    avg_int_rate_train = np.array(avg_int_rate_train)
    avg_int_rate_test = np.array(avg_int_rate_test)
        
    return pred_acc_train,pred_acc_test, avg_int_rate_train, avg_int_rate_test
