https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html

aws eks update-kubeconfig --name shn-prometheus-aws-qat-eks-cluster --role-arn arn:aws:iam::aws_account_id:role/shn-prometheus-cfn-deployer-role

kubectl apply -f aws-auth-cm.yaml

#dashboard

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/heapster.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/influxdb.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/rbac/heapster-rbac.yaml

kubectl apply -f eks-admin-service-account.yaml


#Connect Dashboard

kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')

kubectl proxy

http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

#nodeport
kubectl -n kube-system edit service kubernetes-dashboard
Change type: ClusterIP to type: NodePort
add nodePort: 30000 in ports section

#Crate Installation

kubectl create namespace crate
kubectl apply -f external-crate.yml -n crate

kubectl apply -f internal-service.yml -n crate

kubectl apply -f external-service.yml -n crate

kubectl apply -f controller.yml -n crate

#Crate adapter Installation

kubectl create namespace crate-adapter

kubectl apply -f internal-service.yml -n crate-adapter

kubectl apply -f controller.yml -n crate-adapter

#Prometheus Installation

###kubectl create -f clusterRole.yml

kubectl create namespace prometheus

kubectl apply -f controller.yml -n prometheus

kubectl apply -f nodeport-service.yml -n prometheus

#Update Docker deployment in kubernetes pods
kubectl set image deployment/crate-adapter-deployment crate-adapter=aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:crate-adapter -n crate-adapter

kubectl get pods -l app=prometheus -w -n prometheus
##### update containers image in statefulset
kubectl patch statefulset server --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:prometheus-server-v1"}]' -n prometheus


##### staging an update --- by default partition = 0 
kubectl patch statefulset server -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":1}}}}' statefulset.apps/server patched -n prometheus


curl -X POST http://localhost:9090/-/reload

https://stackoverflow.com/questions/51026174/running-a-command-on-all-kubernetes-pods-of-a-service

****
Working
wget -O - --post-data '' http://localhost:9090/-/reload


#DLP Docker Image

goto /Users/akundu/test/dlp
cp /Users/akundu/skyhighProjects/vm/shn-prometheus/applications/dlp/Dockerfile ./

$(aws ecr get-login --no-include-email --region us-west-2)
docker build -t dlpapi-server .
docker tag dlpapi-server:latest aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:dlp
docker push aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:dlp

docker tag eureka-registry:latest aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:eureka-registry
docker push aws_account_id.dkr.ecr.us-west-2.amazonaws.com/shn/prometheus:eureka-registry

kubectl create namespace dlp
kubectl apply -f internal-service.yml -n dlp
kubectl apply -f controller.yml -n dlp


#Install NGINX-INGRESS
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/common/ns-and-sa.yaml
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/common/default-server-secret.yaml
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/common/nginx-config.yaml
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/rbac/rbac.yaml
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/deployment/nginx-ingress.yaml
kubectl apply -f https://github.com/nginxinc/kubernetes-ingress/blob/master/deployments/service/nodeport.yaml

kubectl apply -f kubernetes/ingress.yml


#MYSQL run commands

kubectl run mysql-client -n mysql --image=mysql:5.7 -i --rm --restart=Never --\
  mysql -h mysql-0.mysql <<EOF
CREATE DATABASE test;
CREATE TABLE test.messages (message VARCHAR(250));
INSERT INTO test.messages VALUES ('hello');
EOF


kubectl run mysql-client -n mysql --image=mysql:5.7 -i -t --rm --restart=Never --\
  mysql -h mysql-read -e "SELECT * FROM test.messages"
  
kubectl run mysql-client-loop -n mysql --image=mysql:5.7 -i -t --rm --restart=Never --\
  bash -ic "while sleep 1; do mysql -h mysql-read -e 'SELECT @@server_id,NOW()'; done"