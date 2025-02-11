from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class StrategyOptimizer:
    def __init__(self):
        self.model = RandomForestClassifier()

    def optimize(self, df):
        features = df[["rsi", "macd", "volume"]].values
        labels = df["signal"].values
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        return accuracy
