# test_workflow.py
from flytekit import task, workflow
import pandas as pd
from sklearn.metrics import mean_squared_error
from train import fetch_data_from_database, train_linear_regression_model
from sklearn.linear_model import LinearRegression

@task
def test_linear_regression_model(data: pd.DataFrame, model: LinearRegression) -> float:
    X_test = data['engine_cc'].values.reshape(-1, 1)
    y_test = data['power_bhp'].values.reshape(-1, 1)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    
    return mse

@workflow
def test_workflow():
    data = fetch_data_from_database()
    model = train_linear_regression_model(data)
    mse = test_linear_regression_model(data, model)
    return mse

if __name__ == "__main__":
    test_workflow()
