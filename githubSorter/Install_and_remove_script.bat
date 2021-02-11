
helm repo add bitnami https://charts.bitnami.com/bitnami

echo ##########Installing postgresql with helm##########

helm install my-release ^
  --set postgresqlPassword=secret,postgresqlDatabase=my-database ^
    bitnami/postgresql

kubectl wait --for=condition=Ready pod/my-release-postgresql-0 --timeout=300s

echo ##########Creating github table##########

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'create table github (repository_name varchar primary key, stars serial, primary_language varchar)'"

echo ##########Show DB status before applying the job##########

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'select * from github'"

echo ##########Installing app with helm##########

helm install app1 --set env.GITHUB_ACCESS_TOKEN=0a5c821306764e13a4e1c5424e1fab3bd0a7711b helm\githubSorter

kubectl wait pod -l job-name=app1-githubsorter --for=condition=Completed --timeout=300s

echo ##########Show DB status after applying the job##########

kubectl exec -it my-release-postgresql-0 -- sh -c "export PGPASSWORD=secret   && psql -U postgres -d my-database -c 'select * from github'"

echo ##########Show DB status after applying the jobRemove helm charts & pvc##########

helm uninstall app1

helm uninstall my-release

kubectl delete pvc data-my-release-postgresql-0
