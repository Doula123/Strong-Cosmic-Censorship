# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 12:32:01 2025

@author: micha
"""

"""from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification"""
import pandas as pd

"""
X, y = make_classification(n_samples=1000, n_features=4,
                           n_informative=2, n_redundant=0,
                           random_state=0, shuffle=False)
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)
print(clf.predict([[0, 0, 0, 0]]))
"""
# Read CSV
data = pd.read_csv("Kepler.csv", comment='#')

print(data)