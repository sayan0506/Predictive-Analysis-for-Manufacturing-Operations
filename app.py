from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score

app = Flask(__name__)

@app.route('/')
def index():
    # home route for instructions or upload from local
    # at home button it renders the index.html template
    return render_template('index.html')

# Upload Endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    global DATASET

    # check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error":"Upload a CSV file"}), 400

    # read csv
    try:
        DATASET = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400
    

    return jsonify({"message":"File uploaded successfully!","columns": list(DATASET.columns)})


# Train Endpoint
@app.route('/train', methods=['POST'])
def train_model():
    #global DATASET, 
    global MODEL, SCALER, label_encoder

    # label encoder object
    label_encoder = LabelEncoder()

    # scaler object
    SCALER = StandardScaler()

    # model object
    MODEL = DecisionTreeClassifier(
        criterion="gini",
        max_depth=12,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42
        )
    #MODEL = RandomForestClassifier()

    
    if DATASET is None:
        return jsonify({"error":"No dataset uploaded"})
    
    # 2. Parse json data from request 
    data = request.get_json()

    # extract inputs
    features = data.get('features') # 'features' is the json key from which it retrieves the features
    target = data.get('target')

    if not features or not target:
        return jsonify({"error": "Features and target must be provided!"}), 400
    
    print(features, type(features))
    columns = features.copy()
    columns.extend([target])
    
    print(f"Columns - {columns}")
    extracted_features = DATASET[columns] # extract the required columns
    

    # Label encoding
    label_encoder = LabelEncoder()
    #extracted_features['Machine_ID'] = label_encoder.fit_transform(extracted_features['Machine_ID'])

    # label encoding for y
    y_ = label_encoder.fit_transform(extracted_features[target].values)

    # 3. Check the missing values
    missing_values = extracted_features.isnull().sum().to_dict()
    missing_percentage = (extracted_features.isnull().sum() / len(DATASET)) * 100
    
    # 4. interpolate missing values using polynomial
    extracted_features.interpolate(method='polynomial', order=2, inplace=True)
    print(f"Missing value status : \n{extracted_features.isnull().sum()}")

    # 5. convert to numpy array
    X = extracted_features[features].values
    y = y_
    

    # 7. train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, shuffle=True)

    # 6. Normalize the data
    X_train = SCALER.fit_transform(X_train)
    X_test = SCALER.transform(X_test)

    # 9. Train the model
    MODEL.fit(X_train, y_train)

    # 10. Make predictions
    y_pred = MODEL.predict(X_test)

    # 11. Evaluate the model
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # 12. Print output on test set
    output = {
        "message": "Model trained successfully",
        "confusion_matrix": cm.tolist(),
        "accuracy": accuracy,
        "f1_score": f1,
    }
    return jsonify(output)


# predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if MODEL is None or SCALER is None:
        return jsonify({"error":"Model is not trained, train the model first."}), 400
    
    # get json input
    input_data = request.json
    
    if not input_data:
        return jsonify({"error":"No input data provided"}), 400
    
    # convert input data to dataframe
    df = pd.DataFrame([input_data])

    # scale the input data
    input_scaled = SCALER.transform(df)
    
    # prediction
    predicion = MODEL.predict(input_scaled)
    prediction_label = "Yes" if predicion[0] == 1 else "NO" 
    confidence = max(MODEL.predict_proba(input_scaled)[0])
    

    output = {
        "message": "Prediction done",
        "Downtime": prediction_label,
        "confidence": confidence
    }
    
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)







