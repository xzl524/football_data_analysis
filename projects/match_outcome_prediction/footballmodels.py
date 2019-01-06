# coding: utf-8

import numpy as np
import statsmodels.api as sm
from scipy.stats import skellam

class PoissonRegression:
    
    def __init__(self):
        pass
    
    def fit(self, X_home, X_away, hgoal, agoal):
        """
        Fit poisson regression model.
        
        Parameters
        ----------
        X_home:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for home team.
        X_away:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for away team.
        hgoal:
            1d array-like, shape (n_samples, ). Array of goals for home team.
        agoal:
            1d array-like, shape (n_samples, ). Array of goals for away team.      
        """
        
        self.hgoal_reg = sm.GLM(hgoal, X_home, family=sm.families.Poisson()).fit()
        self.agoal_reg = sm.GLM(agoal, X_away, family=sm.families.Poisson()).fit()
        
    def _lambda(self, X_home, X_away):
        """
        Estimated goals for home team and away team.
        
        Parameters
        ----------
        X_home:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for home team.
        X_away:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for away team.
        
        Returns
        -------
        hgoal_lambda:
            1d array-like, shape (n_samples, ). Array of estimated goals for home team.
        agoal_lambda:
            1d array-like, shape (n_samples, ). Array of estimated goals for away team.
        """
        
        hgoal_lambda = self.hgoal_reg.predict(X_home)
        agoal_lambda = self.agoal_reg.predict(X_away)
        
        return hgoal_lambda, agoal_lambda

    def predict_proba(self, X_home, X_away, n_max=20):
        """
        Predict match outcome probabilities.

        Parameters
        ----------
        X_home:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for home team.
        X_away:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for away team.
        n_max: 
            int, no less than 0. Maxmium goals for a team per match.
            
        Returns
        -------
        p_matrix:
            2d array-like, shape (n_samples, 3). Matrix of estimated probabilities. Each row is the probabilities for 3 possibile outcomes of each match.
        """
        
        hgoal_lambda, agoal_lambda = self._lambda(X_home, X_away)

        p_win = np.sum(skellam.pmf(np.arange(n_max)+1, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)), axis=1)
        p_draw = np.sum(skellam.pmf(0, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)), axis=1)
        p_lose = np.sum(skellam.pmf(np.arange(n_max)-n_max, hgoal_lambda.reshape(-1,1), agoal_lambda.reshape(-1,1)), axis=1)
    
        p_matrix = np.array([p_win,p_draw, p_lose]).transpose()
        
        return p_matrix
    
    def predict(self, X_home, X_away, n_max=20):
        """
        Predict match outcomes.
        
        Parameters
        ----------
        X_home:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for home team.
        X_away:
            2d array-like, shape (n_samples, n_features). Input information to predict estimated goals for away team.
        n_max: 
            int, no less than 0. Maxmium goals for a team per match.
            
        Returns
        -------
        ypred:
            1d array-like, shape (n_samples, ). Array of encoded match outcomes.
        """

        ypred = self.predict_proba(X_home, X_away, n_max=n_max).argmax(axis=1)
        
        return ypred