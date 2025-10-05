from flask import Flask, request, jsonify
import joblib
import pandas as pd
from validator import prepare_user_input, coreFeatures, optionalFeatures

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
    
@app.route("/predict_single", methods=["POST"])
def predict_single():
      try:
            input_data = request.json
            if not input_data:
                  return jsonify({"error": "No input provided"}), 400 
            planet_name = input_data.get("planet_name","Usersplanet")
            providedCore= [
                  f for f in coreFeatures
                  if f in input_data and input_data[f] not in [None,'','NaN']
            ]
            if len(providedCore) < 3:
                  return jsonify({"error": f"Please provide atleast 3 core features: {', '.join(coreFeatures)}", 
                                  "providedcore": providedCore      }), 400
            
            row = {"planet_name":planet_name}
            for f in coreFeatures + optionalFeatures:
                  row[f] = input_data.get(f,None)

            period = row.get('orb_period') or 0
            duration = row.get('duration') or 0
            row['duration_ratio']= duration/(period + 1e-6)

            df = pd.DataFrame([row])

            ordered_cols = [
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

            X= df[ordered_cols]
            pred = model.predict(X)[0]
            label_map = {0:'FALSE POSITIVE', 1:'CANDIDATE',2:'CONFIRMED'}
            prediction_label = label_map[int(pred)]

            return jsonify({
                  "planet_name": planet_name,
                  "prediction": prediction_label,
                  "features_used": {k: row[k] for k in coreFeatures + optionalFeatures},
            })
      
      except Exception as e:
            return jsonify({"error": str(e)})
      

      
    
if __name__ == "__main__":
     app.run(debug=True)


        