
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install my-release ^
  --set postgresqlPassword=secret,postgresqlDatabase=my-database ^
    bitnami/postgresql

kubectl wait --for=condition=Ready pod/my-release-postgresql-0

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'create table github (repository_name varchar primary key, stars serial, primary_language varchar)'"

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'select * from github'"

REM helm install app3 --set env.GITHUB_ACCESS_TOKEN=66aea1a81684ecd67266558420ebf161f34e0ff5 helm\githubSorter