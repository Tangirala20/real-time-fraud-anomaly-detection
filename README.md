# Real-Time Fraud & Anomaly Detection Platform

A Python-based fraud detection project combining **XGBoost supervised learning** and **Isolation Forest unsupervised anomaly detection** to identify suspicious financial transactions. The project includes synthetic transaction generation, feature engineering, model evaluation, and saved-model validation on newly generated data.

## Project Overview

Financial fraud detection requires identifying suspicious transactions while minimizing false positives. This project explores two complementary machine learning approaches:

- **XGBoost:** Learns patterns from labeled transactions to classify potential fraud.
- **Isolation Forest:** Identifies anomalous transactions without using fraud labels during training.

The objective is to build a reproducible foundation for a real-time fraud detection service.

## Architecture

```text
Synthetic Transaction Generator
              |
              v
      Raw Transaction CSV
              |
              v
       Feature Engineering
              |
              v
    Processed Feature Dataset
              |
              v
       +------+------+
       |             |
       v             v
    XGBoost     Isolation Forest
       |             |
       +------+------+
              |
              v
       Model Evaluation
```

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** XGBoost, Scikit-learn
- **Model Persistence:** Joblib
- **Testing:** Pytest
- **Development:** Visual Studio Code

## Features

- Synthetic transaction generation with configurable transaction volume.
- Transaction schema validation using Pydantic.
- User-level transaction velocity and rolling amount features.
- Country-based feature engineering.
- Supervised fraud classification with XGBoost.
- Unsupervised anomaly detection with Isolation Forest.
- Model evaluation using precision, recall, F1-score, PR-AUC, and ROC-AUC.
- Validation using newly generated transactions without retraining the saved models.

## Project Structure

```text
real-time-fraud-anomaly-detection/
├── src/
│   ├── schemas.py
│   ├── data_generator.py
│   ├── analyze_data.py
│   ├── feature_engg.py
│   ├── train_model.py
│   └── validate_models.py
├── tests/
│   └── test_schemas.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── configs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/real-time-fraud-anomaly-detection.git
cd real-time-fraud-anomaly-detection
```

### 2. Create a virtual environment

**Windows CMD:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install -r requirements.txt
python -m pip install xgboost
```

### 4. Generate transactions

```cmd
python -m src.data_generator
```

Configure `max_transactions` in the generator to control the number of transactions.

### 5. Analyze the dataset

```cmd
python -m src.analyze_data
```

### 6. Generate features

```cmd
python -m src.feature_engg
```

### 7. Train both models

```cmd
python -m src.train_model
```

The trained models are saved in the `models/` directory.

### 8. Validate saved models

Generate a fresh dataset and its features, then run validation without retraining:

```cmd
python -m src.data_generator
python -m src.feature_engg
python -m src.validate_models
```

**Note:** The generator and feature pipeline use the same configured output paths. Keep a separate copy of any dataset you need to preserve.

## Model Evaluation

The initial synthetic experiment produced the following results on 5,000 newly generated transactions:

| Metric | XGBoost | Isolation Forest |
|---|---:|---:|
| Precision | 1.00 | 0.14 |
| Recall | 1.00 | 0.99 |
| F1-score | 1.00 | 0.24 |
| PR-AUC | 1.00 | 0.944 |
| ROC-AUC | 1.00 | 0.973 |

These are results from the current synthetic generator and model configuration, not benchmarks for real-world fraud detection. Results can change when the generator, feature engineering, or model parameters change.

### Interpretation

- **XGBoost:** Perfect classification on this synthetic validation dataset. This likely reflects learnable patterns in the generator and requires further investigation before drawing conclusions about generalization.
- **Isolation Forest:** Detected most labeled suspicious transactions but generated many false positives at its default decision threshold.

## Important Limitations

- The dataset is synthetic; it does not represent verified financial fraud.
- The generated labels are based on predefined suspicious-transaction rules.
- Perfect synthetic test metrics do not establish real-world model performance.
- Anomaly thresholds and false-positive rates require further tuning.
- This project is a learning and portfolio prototype, not a production-ready financial security system.

## Future Enhancements

- [ ] Tune model hyperparameters and classification thresholds.
- [ ] Evaluate precision-recall trade-offs and false-positive rates.
- [ ] Add automated tests for feature engineering and model predictions.
- [ ] Build a FastAPI endpoint for real-time transaction scoring.
- [ ] Add streaming ingestion using Kafka.
- [ ] Containerize the application with Docker.
- [ ] Add monitoring, logging, and model drift detection.
- [ ] Evaluate on a suitable real-world or independently designed benchmark dataset.

## Running Tests

```cmd
python -m pytest tests/ -v
```

## Author

**Sai Lavanya Tangirala**

Python | Machine Learning | Data Engineering

## Disclaimer

This project is intended for educational and portfolio purposes only. It does not provide financial advice or guarantee fraud detection in real-world environments.