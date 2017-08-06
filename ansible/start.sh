#!/usr/bin/env bash

cd ./../var/lib/GeoIP/
./download.sh
cd ./../../../ansible

ansible-playbook -i ./hosts site.yml
