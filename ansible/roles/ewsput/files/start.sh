#!/usr/bin/env bash

#
# only needed if you have a proxied environment running
#
export https_proxy=https://192.168.1.194:3128/
export http_proxy=https://192.168.1.194:3128/

cd /opt/put-service
python3 worker.py