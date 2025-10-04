import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix, accuracy_score



data = pd.read_csv("CleanedKepler.csv")

data = data[data['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])]
print(data.shape)

features = [
    'koi_period',
    'koi_duration',
    'koi_depth',
    'koi_prad',
    'koi_srad',
    'koi_model_snr'
]

x = data[features]
y = (data['koi_disposition'] == 'CONFIRMED').astype(int)


print("Confirmed", y.sum())
print("False Positive", len(y)-y.sum())

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, stratify=y, random_state=42)

model = RandomForestClassifier(
    n_estimators=100,
    max_features='log2',
    random_state=42
)
model.fit(X_train, y_train)

y_prediction = model.predict(X_test)

print(classification_report(y_test, y_prediction, target_names=['False Positive','Confirmed']))

accuracy = accuracy_score(y_test, y_prediction)
print(f"Total Accuracy: {accuracy * 100:.2f}%")

print(confusion_matrix(y_test, y_prediction))

scores = cross_val_score(model, x, y, cv=5, scoring='accuracy')
print(f"Mean CV accuracy: {scores.mean():.4f}")