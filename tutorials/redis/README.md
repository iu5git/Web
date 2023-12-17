# Методические указания по работе с Redis

### Установка Redis

Установим в Docker-контейнере с Ubuntu Redis. Для этого выполним действия:

```shell
sudo apt install lsb-release curl gpg

curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

Чтобы запустить демон Redis, пишем:
```shell
sudo service redis-server start
```

### Запуск Redis

Запускаем:
```shell
redis-cli 
127.0.0.1:6379> ping
PONG
```

6379 - это порт на котором автоматически запускается `Redis`. 

Чтобы обратиться к вашему контейнеру с `Redis` из терминала операционной системы выполните
```shell
docker exec -it <container> <command>
```

Например
```shell
docker exec -it redis redis-cli CLIENT LIST
```

### Просмотр содержимого Redis

для просмотра всей внесенной в `Redis` информации воспользуйтесь командой 

```shell
keys *
```

