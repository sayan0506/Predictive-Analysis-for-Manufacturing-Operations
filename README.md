# Predictive Analysis for Manufacturing Operations

## Objective

This project implements a RESTful API for predictive analysis of manufacturing operations. The API enables users to upload manufacturing data, train a machine learning model, and make predictions regarding machine downtime or product defects.

---

## Features

1. **Upload Endpoint**: Accepts a CSV file containing manufacturing data (e.g., `Machine_ID`, `Temperature`, `Run_Time`).
2. **Train Endpoint**: Trains a machine learning model on the uploaded dataset and returns performance metrics such as accuracy and F1-score.
3. **Predict Endpoint**: Accepts JSON input (e.g., `{"Temperature": 80, "Run_Time": 120}`) and returns predictions, including confidence scores.

---

## Dataset

The API uses a manufacturing dataset [Machine Downtime.csv](https://github.com/sayan0506/Predictive-Analysis-for-Manufacturing-Operations/blob/main/Machine%20Downtime.csv) Which doesn't contain the "Run_Time" feature column, thus we created a synthetic column, using the following code:

    base_run_time = np.random.normal(400, 100) if row['Downtime'] == 'No' else np.random.normal(100, 5)
    
    # Adjust run time based on temperature
    temp_adjustment = (100 - row['Temperature(C)']) * 0.5  # Higher temp -> lower run time
    return max(base_run_time + temp_adjustment, 0)  # Ensure no negative run time


After generating the ssynthetic data we obtain [Machine_Downtime_Synthetic.csv](https://github.com/sayan0506/Predictive-Analysis-for-Manufacturing-Operations/blob/main/Machine_Downtime_Synthetic.csv) containing the following key columns along with some other feature columns, among which we are mentioning the following columns which also mentioned in the assignment.

Note: For our simplicity, we have taken "Bearing temperature" and made that column as "Temperature(C)" column, so the final csv contains some of follwoing columns:

- **Machine_ID**: Unique identifier for the machine.
- **Temperature**: Operating temperature of the machine(here bearing temperature).
- **Run_Time**: Operations Run time
- **Downtime**: Whether the machine experienced downtime (1 for Yes, 0 for No).

If no dataset is available, synthetic data is generated for testing and development purposes.

---

## Technical Details

- **Language**: Python
- **Framework**: Flask
- **Libraries**: 
  - `pandas`
  - `scikit-learn`
  - `flask`
  - `numpy`

---

## API Endpoints

### 1. **Upload Endpoint**
- **Method**: `POST`
- **URL**: `/upload`
- **Description**: Uploads a CSV file containing manufacturing data.
- **Request**:
  ```
  Content-Type: multipart/form-data
  ```
  Example:
  ```
  curl -X POST -F "file=@data.csv" http://127.0.0.1:5000/upload
  ```
- **Response**:
  ```json
  {
    "columns": [
    "Date","Machine_ID","Assembly_Line_No","Hydraulic_Pressure(bar)","Coolant_Pressure(bar)","Air_System_Pressure(bar)","Coolant_Temperature","Hydraulic_Oil_Temperature(?C)","Temperature(C)","Spindle_Vibration(?m)","Tool_Vibration(?m)","Spindle_Speed(RPM)","Voltage(volts)","Torque(Nm)","Cutting(kN)","Downtime","Run_Time"],
    "message": "File uploaded successfully!"
    }
  ```

---

### 2. **Train Endpoint**
- **Method**: `POST`
- **URL**: `/train`
- **Description**: Trains a supervised learning model on the uploaded dataset.
- **Request**:
  ```json
  {
    "features": "Temperature,Run_Time",
    "target": "Downtime"
  }
  ```
  Example:
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"features": "Temperature,Run_Time", "target": "Downtime_Flag"}' http://127.0.0.1:5000/train
  ```
- **Response**:
  ```json
  {
    "accuracy": 0.49066666666666664,
    "confusion_matrix": [[134,41],[150,50]],
    "f1_score": 0.3436426116838488,
    "message": "Model trained successfully"
    }
  ```

---

### 3. **Predict Endpoint**
- **Method**: `POST`
- **URL**: `/predict`
- **Description**: Returns a prediction based on the input JSON data.
- **Request**:
  ```json
  {
    "Temperature": 85,
    "Run_Time": 100
  }
  ```
  Example:
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"Temperature": 85, "Run_Time": 100}' http://127.0.0.1:5000/predict
  ```
- **Response**:
  ```json
  {
    "Downtime": "Yes",
    "Confidence": 0.85
  }
  ```

---

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/manufacturing-predictive-api.git
   cd manufacturing-predictive-api
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

5. **Test Endpoints**
   Use tools like [Postman](https://www.postman.com/) or `curl` to test the API endpoints.

---

## Project Structure

```
├── app.py                # Main Flask application
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── data/                 # Sample dataset (if any)
├── synthetic_data.py     # Script to generate synthetic data
├── templates/            # HTML templates (if applicable)
└── static/               # Static files (CSS/JS, if applicable)
```

---

## Example Dataset

Sample CSV structure for uploading:
```
Machine_ID,Temperature,Run_Time,Downtime_Flag
1,85,120,1
2,75,100,0
3,90,110,1
4,70,95,0
```

---

## Notes

- The ML model used is a **Random Forest Classifier**, but this can be replaced with other models like Logistic Regression or Decision Trees.
- Use the `/upload` endpoint before training or predicting to ensure the dataset is properly loaded.

---

## Reference

* [Optimization of machine downtime](https://www.kaggle.com/datasets/srinivasanusuri/optimization-of-machine-downtime)

## References
[1]: https://github.com/username/repository-name "GitHub Repository"

## License

This project is licensed under the [MIT License](LICENSE).

---

Let me know if you need additional information or improvements for the README!
