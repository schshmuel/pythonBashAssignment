
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install my-release ^
  --set postgresqlPassword=secret,postgresqlDatabase=my-database ^
    bitnami/postgresql

kubectl wait --for=condition=Ready pod/my-release-postgresql-0

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'create table github (repository_name varchar primary key, stars serial, primary_language varchar)'"