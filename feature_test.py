import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score


import warnings
warnings.filterwarnings('ignore')

data = pandas.read_csv('Kepler.csv',comment = "#")
data = data[data['koi_disposition'] != 'CANDIDATE']

mapping = {'CONFIRMED': 0, 'FALSE POSITIVE': 1}
data['koi_disposition'] = data['koi_disposition'].map(mapping)

data = data.drop(['kepid','kepoi_name','kepler_name','koi_tce_delivname','koi_pdisposition','koi_fpflag_nt','koi_fpflag_co','koi_fpflag_ss','koi_fpflag_ec','koi_kepmag','dec','koi_score'], axis =1)
err_columns = data.filter(like='err').columns
data = data.drop(err_columns, axis=1)

print(data)

x = data.drop('koi_disposition', axis = 1)
y = data['koi_disposition']

RFclassifier = RandomForestClassifier(n_estimators=300, random_state=42,max_features="log2",max_depth=30)
cv_scores = cross_val_score(RFclassifier, x, y, cv=5, scoring='accuracy')
print("Mean CV Accuracy:", cv_scores.mean())

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

RFclassifier.fit(x_train, y_train)

y_pred = RFclassifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:\n", classification_rep)

importances = RFclassifier.feature_importances_
feature_importance_df = pandas.DataFrame({
    'Feature': x.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importances:")
print(feature_importance_df)

    #sample = x_test.iloc[0:1]
    #prediction = RFclassifier.predict(sample)

    #sample_dict = sample.iloc[0].to_dict()
    #print(f"\nSample Planet: {sample_dict}")
    #print(f"Predicted: {'CONFIRMED' if prediction[0] == 1 else 'CANDIDATE or False Positive'}")