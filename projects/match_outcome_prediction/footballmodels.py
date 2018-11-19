# coding: utf-8

import numpy as np
import statsmodels.api as sm
from sklearn.metrics import accuracy_score
from scipy.stats import skellam
from sklearn.preprocessing import OneHotEncoder

class PoissonRegression:
    
    def __init__(self):
        pass
    
    def fit(self, X_home, X_away, hgoal, agoal):
        
        # Fit poisson regression model
        self.hgoal_reg = sm.GLM(hgoal, X_home, family=sm.families.Poisson()).fit()
        self.agoal_reg = sm.GLM(agoal, X_away, family=sm.families.Poisson()).fit()
        
    def _lambda(self, X_home, X_away):
        
        # Poisson Prediction
        hgoal_lambda = self.hgoal_reg.predict(X_home)
        agoal_lambda = self.agoal_reg.predict(X_away)
        
        return hgoal_lambda, agoal_lambda

    def predict_proba(self, X_home, X_away, n_max=20):
        
        # Poisson Prediction
        hgoal_lambda, agoal_lambda = self._lambda(X_home, X_away)

        p_win = np.sum(skellam.pmf(np.arange(n_max)+1, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)),axis=1)
        p_draw = np.sum(skellam.pmf(0, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)), axis=1)
        p_lose = np.sum(skellam.pmf(np.arange(n_max)-n_max, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)), axis=1)
    
        p_matrix = np.array([p_win,p_draw, p_lose]).transpose()
        
        return p_matrix
    
    def predict(self, X_home, X_away, n_max=20):
    
        # Encoding result
        ypred = self.predict_proba(X_home, X_away, n_max=n_max).argmax(axis=1)
        
        return ypred
    
    def select_match_with_fair_odds(self, X_home, X_away, odds, n_max=20):
    
        p_matrix = self.predict_proba(X_home, X_away, n_max=n_max)
        
        ypred = self.predict(X_home, X_away, n_max=n_max)
        oh_encoder = OneHotEncoder(n_values=3, sparse=False)
        ypred_oh = oh_encoder.fit_transform(ypred.reshape(len(ypred), 1))
    
        fair_matrix = np.multiply(odds, np.multiply(p_matrix, ypred_oh))
    
        sel = (fair_matrix[:,0]>1)|(fair_matrix[:,1]>1)|(fair_matrix[:,2]>1)

        return sel

    def select_match_with_fair_odds_prob(self, X_home, X_away, odds, n_max=20):
    
        p_matrix = self.predict_proba(X_home, X_away, n_max=n_max)
        
        fair_matrix = np.multiply(p_matrix, odds)
    
        sel = (fair_matrix[:,0]>1)|(fair_matrix[:,1]>1)|(fair_matrix[:,2]>1)

        return sel