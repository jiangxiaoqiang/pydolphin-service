#!/usr/bin/env bash

# 当使用未初始化的变量时，程序自动退出
# 也可以使用命令 set -o nounset
set -u

# 当任何一行命令执行失败时，自动退出脚本
# 也可以使用命令 set -o errexit
set -e

set -x

#
# const define area
#
PROGRAM_NAME="manage.py"

#
# stop process
#
PID=`ps -ef|grep -w ${PROGRAM_NAME}|grep -v grep|cut -c 9-15`
if [ -z "${PID}" ]; then
        echo "Process aready down..."
else
        array=(${PID//\n/})
        for var in ${array[@]}
        do
                singlepid=`echo ${var} | awk 'gsub(/^ *| *$/,"")' `
                if [[ ${singlepid} -gt 1 ]]; then
                        kill -15 ${singlepid}
                else
                        echo "Process ${PROGRAM_NAME} not found"
                fi
        done
fi

sleep 5s

#
# start process
#
count=`ps -ef | grep ${PROGRAM_NAME} | grep -v "grep" | wc -l`
if [[ ${count} -lt 1 ]]; then
	nohup /usr/local/bin/python3 manage.py runserver 0.0.0.0:9000 > /dev/null &
else
	echo "unable to start app, process already exists!"
fi
