#!/bin/bash

set -e

# 激活虚拟环境
source /app/api/.venv/bin/activate

# ---------------------------------------------
# Gunicorn 参数（从 AS_ 前缀环境变量读取，允许覆盖）
# ---------------------------------------------
WORKERS=${AS_SERVER_WORKER_AMOUNT:-4} # 并发 worker 数量
WORKER_CLASS=${AS_SERVER_WORKER_CLASS:-uvicorn.workers.UvicornWorker}
BIND="0.0.0.0:8081"
TIMEOUT=${AS_GUNICORN_TIMEOUT:-120} # 超时时间，>=90 更稳定
KEEPALIVE=${AS_GUNICORN_KEEPALIVE:-5}
MAX_REQUESTS=${AS_MAX_REQUESTS:-0} # 每多少请求后优雅重启（0 = 禁用）
LOG_LEVEL=${AS_LOG_LEVEL:-info}

APP_MODULE=${AS_APP_MODULE:-main:app} # FastAPI 入口模块

# ----------------------------
# 打印启动信息（可选）
# ----------------------------
echo "======================================================"
echo "🚀 Starting Audio Server API"
echo "🔧 Workers:          $WORKERS"
echo "🔧 Worker Class:     $WORKER_CLASS"
echo "🔧 Bind:             $BIND"
echo "🔧 Timeout:          $TIMEOUT"
echo "🔧 Keepalive:        $KEEPALIVE"
echo "🔧 Log Level:        $LOG_LEVEL"
echo "🔧 App Module:       $APP_MODULE"
echo "======================================================"

# ---------------------------------------------
# 🚀 启动 Gunicorn + Uvicorn Worker（生产模式）
# ---------------------------------------------
exec gunicorn \
    --bind "$BIND" \
    --workers "$WORKERS" \
    --worker-class "$WORKER_CLASS" \
    --timeout "$TIMEOUT" \
    --keep-alive "$KEEPALIVE" \
    --max-requests "$MAX_REQUESTS" \
    --log-level "$LOG_LEVEL" \
    --access-logfile "-" \
    --error-logfile "-" \
    "$APP_MODULE"