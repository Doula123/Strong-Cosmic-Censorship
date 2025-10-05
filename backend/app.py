from flask import Flask, request, jsonify
import joblib
import pandas as pd
from validator import prepare_user_input

model = joblib.load ("exoplanet_model.pkl")

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
 

    if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
    uploaded_file = request.files['file']

    if not uploaded_file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are supported"}), 400  
    try:
        
        data = prepare_user_input(uploaded_file)

        planet_names = data['planet_name'].tolist()
        X = data.drop(columns=['planet_name'])
        prediction = model.predict(X)
        label_map = {0:'FALSE POSITIVE', 1:'CANDIDATE',2:'CONFIRMED'}
        results = [label_map[(int(p))] for p in prediction]

        columns = ['planet_name'] + X.columns.tolist() + ["Prediction"]
        rows = [ [planet_names[i]] + X.iloc[i].tolist()+[results[i]] for i in range(len(data))]

        return jsonify({
              
            "columns": columns,
            "rows": rows
        })


    except Exception as e:
        return jsonify({"error": str(e)}),500
    
if __name__ == "__main__":
     app.run(debug=True)


        