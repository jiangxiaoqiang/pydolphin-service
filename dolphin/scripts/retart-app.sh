#!/usr/bin/env bash

# 当使用未初始化的变量时，程序自动退出
set -u

# 当任何一行命令执行失败时，自动退出脚本
set -e

# 在运行结果之前，先输出执行的那一行命令
set -x

PYDOLPHIN_SERVICE_PROCESS_NAME="spider-service"

count=`ps -ef | grep ${PYDOLPHIN_SERVICE_PROCESS_NAME} | grep -v "grep" | wc -l`
if [ $count -lt 1 ]; then

else
	echo "process pgagent aready exists!"
fi




