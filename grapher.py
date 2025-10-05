import warnings
import joblib
warnings.filterwarnings("ignore", message="X has feature names, but")
from Cleandata import clean_uploaded_dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    RocCurveDisplay,
    classification_report, accuracy_score
)

def grapher(data, model, features):
	# Data must be cleaned beforehand! need consistent labels with features dictionary,
	# must match liam model feature list


	X = data[features]
	label_map = {'FALSE POSITIVE': 0, 'CANDIDATE': 1, 'CONFIRMED': 2}
	y = data['disposition'].map(label_map)

	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.2, stratify=y, random_state=69
	)

	# predict
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)

	target_names = ['False Positive', 'Candidate', 'Confirmed']
	print("\nClassification Report:\n")
	print(classification_report(y_test, y_pred, target_names=target_names, digits=3, zero_division=0))
	print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
	print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

	scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
	print("Mean CV accuracy: {:.4f}".format(scores.mean()))

	rf = model.named_steps['model']
	importances = rf.feature_importances_

	print("\nFeature importances:")
	for name, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
		print(f"{name}: {imp:.4f}")

	y_proba = model.predict_proba(X_test)
	if y_proba.shape[1] > 1:
		y_score = y_proba[:, 2]  # probability for "Confirmed"
	else:
		y_score = y_proba[:, 0]

	# --- ROC Curve ---
	plt.figure(figsize=(8, 6))
	RocCurveDisplay.from_predictions(y_test == 2, y_score)
	plt.title("ROC Curve (CONFIRMED vs Others)")
	plt.tight_layout()


	# --- Confusion Matrix ---
	plt.figure(figsize=(8, 6))
	cm = confusion_matrix(y_test, y_pred)
	ConfusionMatrixDisplay(cm, display_labels=target_names).plot(colorbar=False)
	plt.title("Confusion Matrix")
	plt.tight_layout()


	# --- Feature Importances ---
	plt.figure(figsize=(8, 6))
	sorted_idx = np.argsort(importances)
	plt.barh(np.array(features)[sorted_idx], np.array(importances)[sorted_idx])
	plt.title("Random Forest Feature Importances")
	plt.tight_layout()


	plt.show()


if __name__ == "__main__":

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




	# importing and cleaning data that model has never seen before!
	data = pd.read_csv("/home/eliot/PycharmProjects/Strong-Cosmic-Censorship/CleanedKepler.csv")

	valid_labels = ['FALSE POSITIVE', 'CANDIDATE', 'CONFIRMED']
	data = data[data['disposition'].isin(valid_labels)]
	# adding duration_ratio
	data['duration_ratio'] = data['duration'] / (data['orb_period'] + 1e-6)

	model_path = '/home/eliot/PycharmProjects/Strong-Cosmic-Censorship/exoplanet_model.pkl'
	pipe = joblib.load(model_path)

	grapher(data,pipe,features)