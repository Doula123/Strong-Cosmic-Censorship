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

data = data[data['koi_disposition'] != 'REFUTED']

print(data.shape)

data = data.dropna(subset=['koi_disposition'])
data['duration_ratio'] = data['koi_duration'] / (data['koi_period'] + 1e-6)

print(data['koi_disposition'].unique())

planet_names = data['planet_name']

features = [
    'koi_period',
    'koi_duration',
    'koi_depth',
    'koi_prad',
    'koi_srad',
    'koi_model_snr',
    'koi_impact', 
    'koi_steff',
    'koi_slogg',
    'koi_teq',          
    'koi_insol',
    'duration_ratio',
]

x = data[features]


label_map = {'FALSE POSITIVE':0, 'CANDIDATE':1, 'CONFIRMED':2}
y = (data['koi_disposition'].map(label_map))


print("Class distribution:")
print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, stratify=y, random_state=42)

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
        max_depth=40,
        max_features='sqrt',
        min_samples_leaf=1,
        min_samples_split=5,
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