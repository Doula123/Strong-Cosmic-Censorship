import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score

import warnings
warnings.filterwarnings('ignore')

data1 = pandas.read_csv('Kepler.csv',comment = "#")
data1=data1[['ra','dec','koi_prad','koi_period','koi_steff','koi_srad','koi_disposition']]
data1 = data1.rename(columns={
    'koi_prad':'pl_rade',
    'koi_period':'pl_orbper',
    'koi_steff':'st_teff',
    'koi_srad':'st_rad',
    'koi_disposition':'disposition'
})
data1['disposition'] = data1['disposition'].map({'CONFIRMED': 0, 'CANDIDATE': 1 ,'FALSE POSITIVE': 2})

data2 = pandas.read_csv('K2.csv',comment = "#")
data2=data2[['ra','dec','pl_rade','pl_orbper','st_teff','st_rad','disposition']]
data2['disposition'] = data2['koi_disposition'].map({'CONFIRMED': 0, 'CANDIDATE': 1 ,'FALSE POSITIVE': 2})

data3 = pandas.read_csv('TESS.csv',comment = "#")
data3=data3[['ra','dec','pl_rade','pl_orbper','st_teff','st_rad','tfopwg_disp']]
data3 = data3.rename(columns={'tfopwg_disp':'disposition'})
data3 = data3[~data3['disposition'].isin(['APC','FA','KP'])]
data3['disposition'] = data3['disposition'].map({'CP': 0, 'PC': 1 ,'FP': 2})

data=pandas.concat([data1, data2, data3], ignore_index=True)

#data = data[data['koi_disposition'] != 'CANDIDATE']
#mapping = {'CONFIRMED': 0, 'FALSE POSITIVE': 1}
#data['koi_disposition'] = data['koi_disposition'].map(mapping)
#data = data.drop(['kepid','kepoi_name','kepler_name','koi_tce_delivname','koi_pdisposition','koi_fpflag_nt','koi_fpflag_co','koi_fpflag_ss','koi_fpflag_ec','koi_kepmag','dec','koi_score'], axis =1)
#err_columns = data.filter(like='err').columns
#data = data.drop(err_columns, axis=1)




x = data.drop('disposition', axis = 1)
y = data['disposition']

RFclassifier = RandomForestClassifier(n_estimators=300, random_state=42,max_features="log2",max_depth=30)
cv_scores = cross_val_score(RFclassifier, x, y, cv=5, scoring='accuracy')
print("Mean CV Accuracy:", cv_scores.mean())

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

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