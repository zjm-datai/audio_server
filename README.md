
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

