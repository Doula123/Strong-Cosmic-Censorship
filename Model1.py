import pandas as pd
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import joblib


data = pd.read_csv("CleanedKepler.csv")

data = data[data['disposition'] != 'REFUTED']

print(data.shape)

data = data.dropna(subset=['disposition'])
data['duration_ratio'] = data['duration'] / (data['orb_period'] + 1e-6)

print(data['disposition'].unique())

features = [
    'orb_period',
    'duration',
    'depth',
    'planet_rad',
    'stellar_rad',
    'model_snr',
    'impact',
    'stellar_teff',
    'stellar_g_log',
    'planet_eq_temp',
    'planet_insol',
    'duration_ratio',
]

x = data[features]


label_map = {'FALSE POSITIVE':0, 'CANDIDATE':1, 'CONFIRMED':2}
y = (data['disposition'].map(label_map))


print("Class distribution:")
print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, stratify=y, random_state=42)

#model = RandomForestClassifier(
    #n_estimators=100,
    #class_weight='balanced',
   # max_features='log2',
   # random_state=42
#)
##model.fit(X_train, y_train)

#y_prediction = model.predict(X_test)


pipe = Pipeline([
    ('imputer', IterativeImputer(random_state=42)),
    ('model', RandomForestClassifier(
         class_weight=None,
        max_depth=20,
        max_features='sqrt',
        min_samples_leaf=2,
        min_samples_split=2,
        n_estimators=200,
        random_state=42
    ))
  
])


pipe.fit(X_train, y_train)
y_prediction = pipe.predict(X_test)

target_names = ['False Positive', 'Candidate', 'Confirmed']

print(classification_report(y_test, y_prediction, target_names=target_names))
print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_prediction) * 100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_prediction))

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='accuracy')
print("Mean CV accuracy: {:.4f}".format(scores.mean()))
      
rf = pipe.named_steps['model']
importances = rf.feature_importances_

for name, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
    print(f"{name}: {imp:.4f}")

joblib.dump(pipe, "exoplanet_model.pkl")