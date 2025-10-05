import pandas as pd
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline

# ----------------------------
# Load and prepare data
# ----------------------------
data = pd.read_csv("CleanedKepler.csv")

# remove unwanted label
data = data[data['koi_disposition'] != 'REFUTED']

print("Data shape before drop:", data.shape)

# remove rows with no disposition
data = data.dropna(subset=['koi_disposition'])

# add engineered feature
data['duration_ratio'] = data['koi_duration'] / (data['koi_period'] + 1e-6)

print("Unique dispositions:", data['koi_disposition'].unique())

# features
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

X = data[features]

# map labels
label_map = {'FALSE POSITIVE':0, 'CANDIDATE':1, 'CONFIRMED':2}
y = data['koi_disposition'].map(label_map)

print("Class distribution:\n", y.value_counts())

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ----------------------------
# Pipeline
# ----------------------------
pipe = Pipeline([
    ('imputer', IterativeImputer(random_state=42)),
    ('model', RandomForestClassifier(random_state=42))
])

# ----------------------------
# GridSearchCV
# ----------------------------
param_grid = {
    'model__n_estimators': [100, 200, 300, 500],
    'model__max_depth': [10, 20, 40, None],
    'model__max_features': ['sqrt', 'log2', None],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4],
    'model__class_weight': [None, 'balanced']
}

grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=-1,
    verbose=2
)

# Fit grid search
grid.fit(X_train, y_train)

print("\nBest Parameters:")
print(grid.best_params_)
print("Best CV Accuracy: {:.4f}".format(grid.best_score_))

# ----------------------------
# Evaluate on test set
# ----------------------------
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)

target_names = ['False Positive', 'Candidate', 'Confirmed']
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=target_names))
print("Test Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred)*100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ----------------------------
# Feature Importances
# ----------------------------
rf = best_model.named_steps['model']
importances = rf.feature_importances_

print("\nFeature Importances:")
for name, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
    print(f"{name}: {imp:.4f}")
