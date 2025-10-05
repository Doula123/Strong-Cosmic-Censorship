# ==========================================
# 🌌 Exoplanet Candidate Model Evaluation Dashboard
# ==========================================
import warnings
import joblib
warnings.filterwarnings("ignore", message="X has feature names, but")

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
	# model should be already fitted

	X = data[features]
	label_map = {'FALSE POSITIVE': 0, 'CANDIDATE': 1, 'CONFIRMED': 2}
	y = data['koi_disposition'].map(label_map)

	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.05, stratify=y, random_state=42
	)

	# fit and predict
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


	# ---- plots ----
	fig, axes = plt.subplots(1, 3, figsize=(16, 9))
	axes = axes.ravel()

	# --- roc ---
	RocCurveDisplay.from_predictions(y_test == 2, y_score, ax=axes[0])
	axes[0].set_title("ROC Curve (CONFIRMED vs Others)")

	# --- Confusion Matrix ---
	cm = confusion_matrix(y_test, y_pred)
	ConfusionMatrixDisplay(cm, display_labels=target_names).plot(ax=axes[1], colorbar=False)
	axes[1].set_title("Confusion Matrix")

	# --- importances ---
	sorted_idx = np.argsort(importances)
	axes[2].barh(np.array(features)[sorted_idx], np.array(importances)[sorted_idx])
	axes[2].set_title("Random Forest Feature Importances")

	plt.tight_layout()
	plt.show()





if __name__ == "__main__":

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
	]

	data = pd.read_csv("/home/eliot/PycharmProjects/Strong-Cosmic-Censorship/CleanedKepler.csv")
	data = data[data['koi_disposition'] != 'REFUTED']
	data = data.dropna(subset=['koi_disposition'])

	model_path = '/home/eliot/PycharmProjects/Strong-Cosmic-Censorship/backend/exoplanet_model.pkl'
	pipe = joblib.load(model_path)

	grapher(data,pipe,features)