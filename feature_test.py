import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

data = pandas.read_csv('Kepler.csv',comment = "#")

mapping = {'CONFIRMED': 0, 'CANDIDATE': 1, 'FALSE POSITIVE': 2}
data['koi_disposition'] = data['koi_disposition'].map(mapping)

data = data.drop(['kepid','kepoi_name','kepler_name','koi_tce_delivname','koi_pdisposition','koi_score'], axis =1)
err_columns = data.filter(like='err').columns
data = data.drop(err_columns, axis=1)

x = data.drop('koi_disposition', axis = 1)
y = data['koi_disposition']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

RFclassifier = RandomForestClassifier(n_estimators=250, random_state=42)

RFclassifier.fit(x_train, y_train)

y_pred = RFclassifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
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