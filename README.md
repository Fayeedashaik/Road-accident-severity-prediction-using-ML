# 🚦 Road Accident Severity Prediction

A full-stack **Traffic Safety Analytics Dashboard** built with Python, Scikit-learn, and Streamlit.

---

## 🎯 Overview

This project uses **Machine Learning (Random Forest Classifier)** to predict road accident severity based on environmental and situational factors. It includes a complete pipeline from data generation to a deployable web application.

**Severity Classes:** `Minor` | `Serious` | `Fatal`

---

## 📂 Project Structure

```
Road-Accident-Severity-Prediction/
│
├── dataset/
│     └── accident_data.csv          ← Auto-generated dataset (2000 rows)
│
├── model/
│     ├── accident_model.pkl         ← Trained Random Forest model
│     ├── label_encoders.pkl         ← LabelEncoders for categories
│     └── feature_names.pkl          ← Feature names list
│
├── analysis.ipynb                   ← EDA & visualization notebook
├── train_model.py                   ← Model training script
├── app.py                           ← Streamlit web dashboard
└── requirements.txt                 ← Python dependencies
```

---

## ⚙️ Setup & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Train the model
```bash
python train_model.py
```

### Step 3 — Launch the dashboard
```bash
streamlit run app.py
```

---

## 🖥️ Dashboard Pages

| Page | Description |
|---|---|
| 🏠 Home | Project overview, tech stack, applications |
| 📊 Data Analysis | Dataset preview, statistics, correlation heatmap |
| 📈 Visualization | 6 interactive Plotly charts |
| 🤖 Severity Prediction | ML-powered real-time prediction form |

---

## 🤖 Model Performance

| Metric | Score |
|---|---|
| Accuracy | 71.5% |
| Precision | 72.0% |
| Recall | 71.5% |
| F1 Score | 70.8% |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Pandas / NumPy** — Data processing
- **Scikit-learn** — Random Forest classifier
- **Plotly** — Interactive visualizations
- **Streamlit** — Web dashboard
- **Joblib** — Model serialization

---

## 📊 Features Used

1. Weather Conditions
2. Road Type
3. Speed Limit
4. Light Conditions
5. Time of Day
6. Number of Vehicles
7. Driver Age

---

*Built as a portfolio ML project for Traffic Safety Analytics.*
