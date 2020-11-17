1.	Put the docker-compose.yml file and redis.conf file under the project folder
2.	Change to the project folder where locate the yml and conf files
3.	Run “docker-compose up -d” to create 6 redis container
4.	Create Redis cluster
#docker run --rm -it inem0o/redis-trib create --replicas 1 192.168.42.1:7001 192.168.42.1:7002 192.168.42.1:7003 192.168.42.1:7004 192.168.42.1:7005 192.168.42.1:7006
The ip address is the address set in redis.conf file

 

