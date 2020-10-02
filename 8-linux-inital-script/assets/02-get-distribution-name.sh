#!/bin/bash

### descrption: get distribution name
### create time: 2020-10-02 (yyyy-MM-dd)
### author: deltaV235

OS_NAME=$(cat /etc/os-release | grep ^NAME= | cut -d '"' -f 2 |
  cut -d " " -f 1 | awk '{print tolower($0)}')
