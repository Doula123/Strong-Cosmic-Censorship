import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from imblearn.over_sampling import SMOTE 
from imblearn.pipeline import Pipeline as ImbPipeline 


"""
features:
- Planet Orbital Period Value [days]
- Planet Transit Duration Value [hours]
- Planet Transit Depth Value [ppm]
- Planet Radius Value [R_Earth]
- Planet Insolation Value [Earth flux]
- Planet Equilibrium Temperature Value [K]
- TESS Magnitude
- Stellar Distance [pc]
- Stellar Effective Temperature Value [K]
- Stellar log(g) Value [cm/s**2]
- Stellar Radius Value [R_Sun]
"""





SELECTED_FEATURES = [
    'pl_orbper', 'pl_trandurh', 'pl_trandep', 'pl_rade', 'pl_insol', 
    'pl_eqt', 'st_tmag', 'st_dist', 'st_teff', 'st_logg', 'st_rad']

TARGET = 'tfopwg_disp'

MODEL_FILE = 'rf_model.pkl'

def load_and_preprocess_data():
    df = pd.read_csv("TESS.csv", comment='#')
    df = df[SELECTED_FEATURES + [TARGET]].dropna()
    return df


def train_model():
    df = load_and_preprocess_data()
    X = df[SELECTED_FEATURES]
    y = df[TARGET]
    
    le = LabelEncoder()#encode target label
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    rf = RandomForestClassifier(random_state=42)

    pipeline = ImbPipeline([
        ('smote', SMOTE(random_state=42, k_neighbors=3)), # 🌟 Smaller k_neighbors for very small classes like 'FA'
        ('classifier', rf)
    ])
    
    param_grid = {
        'classifier__n_estimators': [500, 1500],
        'classifier__max_depth': [None, 20, 40],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
        'classifier__max_features': ['sqrt', 'log2'],
        'classifier__class_weight': [None, 'balanced', 'balanced_subsample'] 
    }
    
    clf = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=1, scoring='f1_macro')
    clf.fit(X_train, y_train)

    
    best_clf = clf.best_estimator_
    
    y_pred = best_clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0)
    
    joblib.dump(best_clf, MODEL_FILE) #saving model and lavel encoder
    joblib.dump(le, 'le.pkl')
    
    return best_clf, le, accuracy, report, clf.best_params_


def main():
    if os.path.exists(MODEL_FILE):
        print("Existing model found. Loading model...")
        clf = joblib.load(MODEL_FILE)
        le = joblib.load('le.pkl')
        
        df = load_and_preprocess_data()
        X = df[SELECTED_FEATURES]
        y = le.transform(df[TARGET])

        #recalc for mor precision
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model loaded successfully. Accuracy: {acc:.3f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))

    else:
        print("No saved model found. Training new model...")
        clf, le, accuracy, report, best_params = train_model() 
        print("\nModel trained successfully!")
        print(f"Best Parameters: {best_params}")
        print(f"Accuracy: {accuracy:.3f}")
        print("Classification Report:")
        print(report)


if __name__ == "__main__":
    main()


