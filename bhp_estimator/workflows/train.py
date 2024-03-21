from flytekit import task, workflow
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import psycopg2
import json 

@task
def fetch_data_from_database() -> pd.DataFrame:
    with open('config.json') as f:
        credentials = json.load(f)

    host = credentials["host"]
    user = credentials["user"]
    port = credentials["port"]
    database = credentials["database"]
    password = credentials["password"]
    
    conn = psycopg2.connect(
        host=host,
        user=user,
        port=port,
        database=database,
        password=password
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT engine, power FROM uc_training_data")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    df = pd.DataFrame(data, columns=['engine', 'power'])
    return df

@task
def train_linear_regression_model(data: pd.DataFrame) -> LinearRegression:
    X = data['engine'].values.reshape(-1, 1)
    y = data['power'].values.reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model

@task
def plot_data(data: pd.DataFrame, model: LinearRegression):
    plt.scatter(data['engine'], data['power'], color='blue')
    plt.plot(data['engine'], model.predict(data['engine'].values.reshape(-1, 1)), color='red')
    plt.xlabel('Engine CC')
    plt.ylabel('Power BHP')
    plt.title('Linear Regression')
    plt.show()

@workflow
def train_and_plot_workflow():
    data = fetch_data_from_database()
    model = train_linear_regression_model(data = data)
    plot_data(data = data, model = model)

if __name__ == "__main__":
    train_and_plot_workflow()
