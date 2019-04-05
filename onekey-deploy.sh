#!/usr/bin/env bash

# 当使用未初始化的变量时，程序自动退出
# 也可以使用命令 set -o nounset
set -u

# 当任何一行命令执行失败时，自动退出脚本
# 也可以使用命令 set -o errexit
set -e

set -x

APP_PATH="/Users/dolphin/source/pydolphin-service"
REMOTE_APP_PATH="/home/dolphin/source/"

# scp -r ${APP_PATH} google-cloud:${REMOTE_APP_PATH}

rsync -avzPh ${APP_PATH} google-cloud:${REMOTE_APP_PATH} 