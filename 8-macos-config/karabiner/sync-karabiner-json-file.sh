#!/bin/bash

fileName=`date +%Y%m%d`"-karabiner.json"

cp ~/.config/karabiner/karabiner.json $fileName && 
    echo -e "\n\033[1;32mThe file karabiner.json was successfully synced to $fileName.\033[0m\n"

