# Redis storage adapters

[![Circle CI](https://circleci.com/gh/thumbor-community/redis.svg?style=svg)](https://circleci.com/gh/thumbor-community/redis)

Thumbor redis storage adapters.

## Installation

`pip install tc_redis`

## Configuration

To use redis as a storage or result storage some values must be configured in `thumbor.conf`

##### Redis Storage
```
STORAGE='tc_redis.storages.redis_storage'

REDIS_STORAGE_IGNORE_ERRORS = True
REDIS_STORAGE_SERVER_STARTUP_NODES = 'localhost:7001,localhost:7002'
REDIS_STORAGE_SERVER_PASSWORD = None
```

##### Redis Result Storage

```
RESULT_STORAGE='tc_redis.result_storages.redis_result_storage'

REDIS_RESULT_STORAGE_IGNORE_ERRORS = True
REDIS_RESULT_STORAGE_SERVER_STARTUP_NODES = 'localhost:7001,localhost:7002'
REDIS_RESULT_STORAGE_SERVER_PASSWORD = None
```

# dffrntlab part

## Where it is


