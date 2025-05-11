
docker rm $(docker ps -a)
docker rmi $(docker images)
docker builder prune