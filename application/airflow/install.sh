#!/bin/sh
# https://github.com/rabbitmq/rabbitmq-peer-discovery-k8s/tree/master/examples/k8s_statefulsets

app=$1

kubectl create configmap airflow-config --from-file="application/$app/airflow.cfg" --from-file="application/$app/requirements.txt" -n $app -o yaml --dry-run | kubectl replace -f -
if test "$?" != "0"; then
  kubectl create configmap airflow-config --from-file="application/$app/airflow.cfg" --from-file="application/$app/requirements.txt" -n $app
fi

kubectl create configmap airflow-dags --from-file="application/$app/dags/" -n $app -o yaml --dry-run | kubectl replace -f -
if test "$?" != "0"; then
  kubectl create configmap airflow-dags --from-file="application/$app/dags/" -n $app
fi

kubectl apply -f application/$app/service.yaml -n $app
kubectl apply -f application/$app/controller.yaml -n $app

#kubectl --record deployment.apps/airflow-webserver set image deployment.v1.apps/airflow-webserver airflow-webserver=puckel/docker-airflow:1.10.4 -n $app
#kubectl --record deployment.apps/airflow-scheduler set image deployment.v1.apps/airflow-scheduler airflow-webserver=puckel/docker-airflow:1.10.4 -n $app