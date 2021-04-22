#!/bin/bash
CONF='/cds/group/pcds/pyps/apps/hutch-python/ued/queueserver/ioc-ued-redis/redis.conf'
REDIS_DIR='/cds/group/pcds/pyps/apps/redis/6.2.1/bin'

"${REDIS_DIR}/redis-server" "${CONF}"
