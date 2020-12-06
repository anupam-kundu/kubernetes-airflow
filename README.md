# kubernetes-airflow
airflow is managed as container service inside kubernetes.
aws eks is used as kubernetes cluster
installed s/w
1. mysql
2. rabbitMQ


folders
applications
1. airflow/dags
2. mysql
3. rabbitmq

cloudformation infra template 
cfn/eks-infrastructure.yaml
cfn/deployment-code-pipeline.yaml

kubernetes help commands
kubernetes/command.md

deploy code pipeline and setup infrastructure using below command
sh cfn/setup-code-pipeline.sh

