# models/risk_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import joblib

class RiskModel:
    def __init__(self):
        # Sample small dataset
        data = pd.DataFrame({
            "text": [
                "I feel very sad and hopeless",
                "I am anxious about everything",
                "I am okay today",
                "I feel happy and productive",
                "I want to end my life",
                "I am stressed about work"
            ],
            "risk": [1,1,0,0,1,1]
        })
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(data['text'])
        y = data['risk']
        self.clf = LogisticRegression()
        self.clf.fit(X, y)

    def predict(self, texts):
        X = self.vectorizer.transform(texts)
        prob = self.clf.predict_proba(X)[:,1].mean()  # average risk over messages
        return float(prob)
