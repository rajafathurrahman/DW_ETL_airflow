from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import pandas as pd
from sqlalchemy import create_engine

# Define the default_args dictionary to specify default parameters for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'ETL_airflow',
    default_args=default_args,
    description='An example ETL DAG',
    schedule_interval=timedelta(days=1),  # Set the schedule interval as per your requirement
)

# Define the function to get data
def get_data():
    yesterday = datetime.strftime(datetime.now().date() - timedelta(days=1), "%Y-%m-%dT%H:%M:%S")
    today = datetime.strftime(datetime.now().date(), "%Y-%m-%dT%H:%M:%S")

    offset = 0
    limit = 1000
    dfres = []
    while True:
        url = f"https://data.edmonton.ca/resource/cnsu-iagr.json?$limit={limit}&$offset={offset}&$where=date_and_time%20between%20%27{yesterday}%27%20and%20%27{today}%27"
        
        response = requests.request("GET", url)
        result = response.json()
        dfres += result
        if len(result) >= 1:
            offset = len(dfres)
        else:
            break
    return dfres

# Define the function for data transformation
def transform_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='get_data_task')  # Retrieve data from the XCom system

    # Data transformation logic
    df = pd.DataFrame(data)
    df.drop(columns=['station_location','station_description', 'latitude','longitude'],inplace=True)

    ti.xcom_push(key='transformed_data', value=df.to_dict(orient='records'))

# Define the function for storing data
def store_data(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_data_task')  # Retrieve data from the XCom system

    # Data storage logic
    engine = create_engine('mysql+mysqlconnector://admin:123456@192.168.0.126:3306/dw')
    pd.DataFrame(transformed_data).to_sql(name='etl_waterflow', con=engine, if_exists='append', index=False)

# Define the tasks in the DAG
get_data_task = PythonOperator(
    task_id='get_data_task',
    python_callable=get_data,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

store_data_task = PythonOperator(
    task_id='store_data_task',
    python_callable=store_data,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies
get_data_task >> transform_data_task >> store_data_task

if __name__ == "__main__":
    dag.cli()
