
```sql
create database audio_server;
```

```shell
create database kn_audio;
```

```shell
alembic init migration
```

```shell
alembic revision --autogenerate -m "initial migration"
```

```shell
alembic upgrade head
```

```shell
docker build -t audio_server:1.0 .
````

1. 构建日志
2. 查看下载接口的错误，为什么下载的时候本地没法直接给，打日志
3. 再处理 minio 的问题，下载的时候 fput 拼接的时候 //tmp
4. 再处理 2 的问题