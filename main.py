from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.impute import SimpleImputer

# Load the trained model and imputer
model = joblib.load('diabetes_svm_model.pkl')
imputer = SimpleImputer(missing_values=0, strategy='median')  # Ensure same imputation strategy

# Initialize FastAPI app
app = FastAPI()


# Define request schema
class InputData(BaseModel):
    Glucose: float
    BMI: float

@app.post("/predict")
def predict(input_data: InputData):
    # Prepare the input data
    input_array = np.array([[input_data.Glucose, input_data.BMI]])

    # Handle missing values using the imputer
    input_array = imputer.fit_transform(input_array)

    # Make prediction
    prediction = model.predict(input_array)

    # Calculate confidence score using decision_function
    confidence_score = model.decision_function(input_array)
    # confidence_level = abs(confidence_score[0])  # Confidence is the absolute value of the distance
    confidence_level = 1 / (1 + np.exp(-confidence_score[0]))

    # Return prediction and confidence level as JSON response
    return {
        "prediction": int(prediction[0]),
        "confidence": confidence_level
    }
