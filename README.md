# Employee Churn Prediction


🚀 Project summary
This project is an end-to-end Employee Churn Prediction system built using machine learning. It covers data cleaning, exploratory data analysis, feature engineering, model development, evaluation, and deployment.
A Flask + HTML web application allows users to input employee details and predict churn probability.
The entire app is containerized using Docker and deployed as a live web service on Render.com.

## Dashboard
![alt image](https://github.com/MohTarique/Employee-Churn-Prediction/blob/master/images/Dashboard%201%20(3).png)
## Points
1. Everyone with seven projects left the company.
2. The scatterplot above shows that there was a sizeable group of employees who worked ~240–315 hours per month,
   315 hours per month is over 75 hours per week for a whole year. It's likely this is related to their satisfaction levels being close to zero.
3. The plot also shows another group of people who left, those who had more normal working hours.
   Even so, their satisfaction was only around 0.4. It's difficult to speculate about why they might have left. It's possible they felt pressured to work more, considering so many of their peers worked more. And that pressure could have lowered their satisfaction levels.
4. Finally, there is a group who worked ~210–280 hours per month, and they had satisfaction levels ranging ~0.7–0.9.


## Model Performance Summary
![alt image](https://github.com/MohTarique/Employee-Churn-Prediction/blob/master/images/Screenshot%20(137).png)

Multiple machine learning models were trained and evaluated using accuracy, precision, recall, F1-score, and ROC-AUC.

🔥 Best performing models (based on ROC-AUC):

XGBoost — 0.9744

Random Forest — 0.9685

SVM — 0.9641

The project uses ROC-AUC as the primary metric, and XGBoost was selected as the final model for deployment due to its strong overall performance across all metrics

📌 Tech Stack

Python, HTML

Pandas, NumPy, Matplotlib, Seaborn

Scikit-learn, XGBoost, SVM, KNN

Flask

Docker

VS Code, Juyter Notebook, Render.com

## 🧠 Project Workflow

### 1️⃣ Data Cleaning

  Removed duplicates
  
  Fixed data types
  
  Handled missing values
  
  Standardized categorical fields

### 2️⃣ Exploratory Data Analysis (EDA)

  Distribution plots
  
  Correlation heatmaps
  
  Churn patterns by department, salary, tenure
  
  Workload analysis
  
### 3️⃣ Feature Engineering

  feature selection
  
  One-hot encoding
  
  Scaling numeric variables
  
### 4️⃣ Model Development

Trained 6 major algorithms:

1.Logistic Regression

2.Decision Tree

3.Random Forest

4.XGBoost

5.SVM

6.KNN

Used:

###Cross Validation

refit='roc_auc'

###Best model selection

Saved model as .pickle

##🌐 Flask Web Application

A Flask-based web interface allows users to input employee attributes and instantly get churn prediction.
Key Files:
```
app.py
templates/index.html
static/style.css
hr_xgb.pickle
```

Start the app locally:
```
python app.py
```
##🐳 Docker Containerization

The project includes a Dockerfile for production deployment.
``` build image
docker build -t churn-app .
```
``` Run Container
docker run -p 5000:5000 churn-app
```
##🚀 Deployment on Render.com

1.Connected GitHub repo to Render Web Services

2.Selected Docker environment

3.Render automatically built and deployed the container

4.Web app is publicly available
