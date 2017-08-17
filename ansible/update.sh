#!/usr/bin/env bash

ansible-playbook -i ./hosts site.yml --tags "updatesrc"
