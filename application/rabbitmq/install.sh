#!/bin/sh
# https://github.com/rabbitmq/rabbitmq-peer-discovery-k8s/tree/master/examples/k8s_statefulsets

app=$1

kubectl apply -f application/$app/rabbitmq_rbac.yaml -n $app

kubectl create configmap rabbitmq-config --from-file="application/$app/enabled_plugins" --from-file="application/$app/rabbitmq.conf" --from-file="application/$app/definitions.json" -n $app -o yaml --dry-run | kubectl replace -f -
if test "$?" != "0"; then
  kubectl create configmap rabbitmq-config --from-file="application/$app/enabled_plugins" --from-file="application/$app/rabbitmq.conf" --from-file="application/$app/definitions.json" -n $app
fi

kubectl apply -f application/$app/service.yaml -n $app
kubectl apply -f application/$app/controller.yaml -n $app


# rabbitmqadmin -q import rabbit.definitions.json