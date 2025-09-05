import pandas as pd
import os
import json
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
from my_project import logging
from functools import reduce
from operator import mul

class ModelTrainer:
    def __init__(self, config):
        self.config = config

        # Candidate models
        self.models = {
            "elasticnet": ElasticNet(),
            "randomforest": RandomForestRegressor(),
            "xgbregressor": XGBRegressor(objective="reg:squarederror"),
        }

        # Available metrics
        self.metrics = {
            "r2": r2_score,
            "mse": mean_squared_error,
            "mae": mean_absolute_error,
        }

    def _count_total_param_combinations(self, params):
        sizes = [len(v) for v in params.values()]
        return reduce(mul, sizes, 1)

    def tune_model(self, model, params, x_train, y_train, scoring, n_iter=20):
        """
        Use RandomizedSearchCV for faster tuning.
        n_iter = number of random combinations (dynamic)
        """
        total_combinations = self._count_total_param_combinations(params)
        n_iter = min(n_iter, total_combinations)  # avoid warning

        search = RandomizedSearchCV(
            model,
            params,
            n_iter=n_iter,
            cv=3,
            scoring=scoring,
            n_jobs=-1,
            random_state=42,
            error_score="raise"
        )
        search.fit(x_train, y_train)
        return search.best_estimator_, search.best_params_

    def initiate_model_trainer(self):
        logging.info("Loading training and test data")
        train_df = pd.read_csv(self.config.trained_data_path)
        test_df = pd.read_csv(self.config.test_data_path)

        target_column = self.config.target_column
        x_train, y_train = train_df.drop(columns=[target_column]), train_df[target_column]
        x_test, y_test = test_df.drop(columns=[target_column]), test_df[target_column]

        logging.info("Training and tuning models")
        params = self.config.params
        model = self.models[self.config.model_name]

        # Tune model
        tuned_model, tuned_params = self.tune_model(
            model, params, x_train, y_train,
            scoring=self.config.evaluation_metric,
            n_iter=30
        )

        # Make predictions and evaluate
        preds = tuned_model.predict(x_test)
        metric_fn = self.metrics.get(self.config.evaluation_metric, r2_score)
        score = metric_fn(y_test, preds)

        logging.info(f"{self.config.model_name} -> Score: {score:.4f}, Best Params: {tuned_params}")

        # Save model
        model_path = os.path.join(self.config.root_dir, f"{self.config.model_name}.pkl")
        joblib.dump(tuned_model, model_path)

        # Save best params
        params_file = os.path.join(self.config.root_dir, f"{self.config.model_name}_best_params.json")
        with open(params_file, "w") as f:
            json.dump({"model_name": self.config.model_name, **tuned_params}, f, indent=4)

        logging.info(f"Model saved at: {model_path}")
        logging.info(f"Params saved at: {params_file}")

        return score
