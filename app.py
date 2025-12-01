# app.py
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle

# Load the trained model
model_path = 'hr_xgb.pickle'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Print submitted form keys/values for debugging
    for key, value in request.form.items():
        print(key, value)

    # --- Obtain expected features from the model if possible ---
    if hasattr(model, "feature_names_in_"):
        expected_features = list(model.feature_names_in_)
    else:
        # fallback if model doesn't have feature_names_in_ - adjust as needed
        expected_features = [
            'last_evaluation', 'number_project', 'tenure', 'work_accident',
            'promotion_last_5years', 'salary', 'department_IT', 'department_RandD',
            'department_accounting', 'department_hr', 'department_management',
            'department_marketing', 'department_product_mng', 'department_sales',
            'department_support', 'department_technical', 'overworked'
        ]

    # Create an empty single-row DataFrame with expected columns initialized to 0
    X = pd.DataFrame([{c: 0 for c in expected_features}])

    # Map common form keys to model feature names if form uses different names
    # Add more mappings here if your HTML form uses different names
    key_map = {
        'number_of_projects': 'number_project',
        'average_montly_hours': 'average_montly_hours',  # if needed
        'time_spend_company': 'tenure',
        'work_accident': 'work_accident',
        'promotion_last_5years': 'promotion_last_5years',
        'last_evaluation': 'last_evaluation',
        'salary': 'salary',
        'department': 'department'  # special handling below
    }

    # Fill DataFrame from form values
    for key, value in request.form.items():
        mapped = key_map.get(key, key)  # default to same key if not mapped

        # Special handling for department field (one-hot)
        if key == 'department' or mapped == 'department':
            # Build the one-hot column name used during training
            # training used names like 'department_sales' etc.
            onehot_col = f"department_{value}"
            if onehot_col in X.columns:
                X.at[0, onehot_col] = 1
            else:
                # if the exact onehot column name is not in expected features,
                # try common variants (case differences)
                for col in X.columns:
                    if col.lower() == onehot_col.lower():
                        X.at[0, col] = 1
                        break
                # if still not found, create it (and ensure other dept cols exist)
                if onehot_col not in X.columns:
                    X[onehot_col] = 1
                    # ensure expected_features order later will include it
        else:
            # Normal numeric / categorical field: set value to the corresponding column if present
            if mapped in X.columns:
                X.at[0, mapped] = value
            else:
                # try case-insensitive match
                lc_map = {c.lower(): c for c in X.columns}
                if mapped.lower() in lc_map:
                    X.at[0, lc_map[mapped.lower()]] = value
                else:
                    # column not expected — ignore or log
                    print(f"Warning: form field '{key}' mapped to '{mapped}' not in expected features; ignoring.")

    # Replace inf / -inf and convert types where possible
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    # Try to convert columns to numeric where possible
    for col in X.columns:
        try:
            X[col] = pd.to_numeric(X[col])
        except Exception:
            # leave as-is (some one-hot cols might already be numeric)
            pass

    # Ensure all expected_features exist in X (create if missing)
    for feat in expected_features:
        if feat not in X.columns:
            X[feat] = 0

    # Reorder columns to expected order (model may rely on it)
    X = X[expected_features]

    print("Prepared input for model:")
    print(X.head())

    # Make prediction (single row)
    try:
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X)[:, 1][0]  # probability of class 1 (leave)
        else:
            # fallback if model doesn't support predict_proba
            pred = model.predict(X)[0]
            prob = float(pred)  # not a probability, but something to show
    except Exception as e:
        # show error in server logs and return helpful message to user
        print("Prediction error:", e)
        return render_template('index.html', predict_value=f"Prediction error: {e}")

    # Interpret probability threshold as you like
    threshold = 0.7
    label = "Employee is at Flight risk" if prob > threshold else "Employee is not at Flight Risk"

    result_text = f"{label} (probability={prob:.3f})"
    print("Result:", result_text)

    # Return back to template (adjust template to display predict_value)
    return render_template('index.html', predict_value=result_text)


if __name__ == "__main__":
    app.run(debug=True)



