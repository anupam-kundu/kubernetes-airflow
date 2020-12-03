from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator
from airflow.api.common.experimental.trigger_dag import trigger_dag
import json

default_args = {
    'owner': 'anupam',
    'depends_on_past': False,
    'start_date': datetime(2019, 9, 15),
    'email': ['anupam@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'provide_context': True
}

dag = DAG('Planner', default_args=default_args, schedule_interval=timedelta(hours=1), catchup=False)

start_task = BashOperator(
    task_id='init_task',
    bash_command='echo "Starting planner Task 1 | Execution Time : {{ ts }}"',
    dag=dag)


def schedule_executor(**kwargs):
    ti = kwargs['ti']
    val = ti.xcom_pull(task_ids='planner')
    encoding = 'utf-8'
    val=str(val, encoding)
    search_string='[{"executionTime"'
    result_string=val[val.index(search_string):]
    print(result_string)
    task_list=json.loads(result_string)
    execution_date=kwargs['execution_date']
    print(execution_date)
    for task in task_list:
        execution_date = execution_date.add(seconds=1)
        print(execution_date)
        run_id = 'trig__{}'.format(execution_date)
        print(run_id)
        stask={'json_executor_task' : task}
        print(stask)
        json_task=json.dumps(stask)
        print(json_task)
        trigger_dag(dag_id="Executor",
                    run_id=run_id,
                    conf=json_task,
                    execution_date=execution_date,
                    replace_microseconds=False)

planner = DockerOperator(
    task_id='planner',
    image='openjdk:8-jre-alpine',
    api_version='auto',
    auto_remove=False,
    volumes=['/usr/local/airflow/artifacts:/usr/local/airflow/artifacts', '/var/run/docker.sock:/var/run/docker.sock'],
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    command='java -cp /usr/local/airflow/artifacts/jar-with-dependencies.jar <class> {{ ts }}',
    xcom_push=True,
    xcom_all=True,
    dag=dag)

end_task = PythonOperator(
    task_id='queue_executor_tasks',
    python_callable=schedule_executor,
    dag=dag)

planner.set_upstream(start_task)
end_task.set_upstream(planner)
