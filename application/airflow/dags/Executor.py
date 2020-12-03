from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'anupam',
    'depends_on_past': False,
    'start_date': datetime(2019, 9, 15),
    'email': ['anupam@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    'provide_context': True
}

dag = DAG('Executor', default_args=default_args, schedule_interval=None)

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Starting executor Task 1 | Passed Conf : {{ dag_run.conf["json_executor_task"] }}"',
    dag=dag)

executor = DockerOperator(
    task_id='executor',
    image='openjdk:8-jre-alpine',
    api_version='auto',
    auto_remove=True,
    volumes=['/usr/local/airflow/artifacts:/usr/local/airflow/artifacts', '/var/run/docker.sock:/var/run/docker.sock'],
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    environment={
        'VPC_EXECUTOR_TASK': '{{ dag_run.conf["json_executor_task"] }}'
    },
    command='java -cp /usr/local/airflow/artifacts/jar-with-dependencies.jar <class>',
    dag=dag)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Finishing executor Task 2 | Execution Time : {{ ts }}"',
    dag=dag)

executor.set_upstream(t1)
executor.set_downstream(t2)
