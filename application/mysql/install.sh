#!/bin/sh

app=$1

kubectl create configmap mysql --from-file="application/$app/master.cnf" --from-file="application/$app/slave.cnf" -n $app -o yaml --dry-run | kubectl replace -f -
if test "$?" != "0"; then
  kubectl create configmap mysql --from-file="application/$app/master.cnf" --from-file="application/$app/slave.cnf" -n $app
fi

kubectl apply -f application/$app/service.yaml -n $app
kubectl apply -f application/$app/controller.yaml -n $app