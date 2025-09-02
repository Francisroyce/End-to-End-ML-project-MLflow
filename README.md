# End-to-End-ML-project-MLflow

## workflow

1. update config.yaml (after, define your constant)

2. update schema.yaml
3. update params.yaml
4. update the entity
5. update the configuration manager in src config
6. update the components
7. update the pipeline
8. update the main.py
9. update the app.py


mflow setup:


---

## **Step 0: Prerequisites**

Make sure you have **Python**, **pip**, and **git** installed, and you have access to your DagsHub repo:
`https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow`

---

## **Step 1: Install Dependencies**

Open a terminal and run:

```bash
pip install dagshub mlflow
```

This installs the DagsHub Python client and MLflow.

---

## **Step 2: Create a Personal Access Token (PAT) in DagsHub**

1. Go to [DagsHub Tokens](https://dagshub.com/user/settings/tokens)
2. Click **New Token** → Name it `"mlflow-token"`
3. Copy the token **somewhere safe**. You’ll use it as the password.

---

## **Step 3: Set up environment variables**

In your terminal, set your DagsHub username and token so MLflow can authenticate automatically:

```bash
export MLFLOW_TRACKING_USERNAME=Francisroyce
export MLFLOW_TRACKING_PASSWORD=your_token_here
```

> Replace `your_token_here` with the token you copied.

If you’re on **Windows Command Prompt**, use:

```cmd
set MLFLOW_TRACKING_USERNAME=Francisroyce
set MLFLOW_TRACKING_PASSWORD=your_token_here
```

---

## **Step 4: Initialize DagsHub in Python**

In a Python script or notebook:

```python
import dagshub

dagshub.init(
    repo_owner='Francisroyce',
    repo_name='End-to-End-ML-project-MLflow',
    mlflow=True
)
```

This connects MLflow tracking to your DagsHub repo.

---

## **Step 5: Log your first MLflow run**

```python
import mlflow

# Start a run
with mlflow.start_run():
    # Log parameters (hyperparameters)
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("optimizer", "adam")
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_metric("loss", 0.15)
```

---

## **Step 6: Log artifacts (optional, e.g., model file or plots)**

```python
# Example: logging a file
mlflow.log_artifact("example_model.pkl")  # Make sure this file exists
```

For saving and logging a **scikit-learn model**:

```python
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
# train your model here...
mlflow.sklearn.log_model(model, "random_forest_model")
```

---

## **Step 7: Check your runs on DagsHub**

Go to:
[https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow](https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow) → **Experiments**

You should see your run with parameters, metrics, and any artifacts you logged.

---

### Quick Test to Ensure Everything Works

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("test_param", 123)
    mlflow.log_metric("test_metric", 1.23)
print("Test run logged successfully!")
```

If you see it in DagsHub → Experiments, you’re fully set up.

---



