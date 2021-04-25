#!/usr/bin/env bash

function help(){
    echo "命令格式："
    echo "  server.sh start --port|-p [默认8080] --worker|-w [默认3] --gpu [0|1] --mode|-m [tfserving|single] --env|-e [local|test|prod] "
    echo "  server.sh stop"
    echo "  server.sh debug 快速启动，端口：8083"
    echo "  例：bin/server.sh start -p 8080 -w 1 -g 3 -m single -e test"
    exit
}

if [ "$1" = "stop" ]; then
    echo "停止  Web 服务"
    ps aux|grep sandbox_server|grep -v grep|awk '{print $2}'|xargs kill -9
    exit
fi

if [ -z "$*" ]; then
    help
    exit
fi

if [ "$1" = "debug" ]; then
    echo "OCR Web 服务调试模式"
    ENV=local MODE=debug gunicorn --log-level=DEBUG  --reload --workers=1 --name=sandbox_server --bind=0.0.0.0:8083 --timeout=300 app.server:app 2>&1
    exit
fi

if [ ! "$1" = "start" ]; then
    help
    exit
fi
#set -x
echo "启动 sandbox web 服务器..."
Date=$(date +%Y%m%d%H%M)
ARGS=`getopt -o p:e:w: --long port:,env:,worker: -n 'help.bash'  -- "$@"`
eval set -- "$ARGS"

while [ -n "$1" ]
do
#        echo "param: $1 $2"
        case "$1" in
                -p|--port)
                  echo "自定义端口号：$2"
                  if ! [ $PORT ]; then PORT=$2; fi #如果已经在环境变量中定义了，则不覆盖，环境变量优先级最大！！！这个是为了兼容容器方式启动，因为容器方式只能通过环境变量传入这些参数
                  shift 2 ;;
                -e|--env)
                  echo "环境选择:$2"
                  if ! [ $ENV ]; then ENV=$2; fi
                  shift 2 ;;
                -w|--worker)
                  echo "进程数：$2"
                  if ! [ $WORKER ]; then WORKER=$2; fi
                  shift 2 ;;
                --)
                  echo "参数读取结束"
                  shift 2
                  break ;;
                *) echo $1,$2,help; break ;;
        esac
done

if [ $? != 0 ]; then
    help
    exit 1
fi

if [ $? != 0 ]; then
    help
    exit 1
fi

#PORT=8080
#MODE=single

echo "环境变量："
echo "-------------------"
echo "PROT:$PORT"
echo "ENV:$ENV"
echo "WORKER:$WORKER"
echo "-------------------"

# 如果外部环境变量和参数中都没有定义port或者mode，给予默认值
if ! [ $PORT ]; then
    echo "未定义PORT，给予默认值：8083"
    PORT=8083
fi
if ! [ $ENV ]; then
    echo "未指定ENV不能启动"
    exit 0
fi
if ! [ $WORKER ]; then
    echo "未定义WORKER，给予默认值：5"
    WORKER=5
fi
export ENV=$ENV

echo "服务启动..."
# 参考：https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
# worker=3是根据GPU的显存数调整出来的，ration=0.2，大概一个进程占满为2.5G,4x2.5=10G显存
_CMD="gunicorn \
    --name=sandbox_server \
    --workers=$WORKER \
    --bind 0.0.0.0:$PORT \
    --timeout=300 \
    app.server:app"
echo "启动服务："
echo "$_CMD"
set -x
#eval "$_CMD"
eval "nohup $_CMD >logs/console.log 2>&1 &"
exit 0
