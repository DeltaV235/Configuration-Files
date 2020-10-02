#!/bin/bash

### descrption: create user by input username
### create time: 2020-10-01 (yyyy-MM-dd)
### author: deltaV235

# import terminal color
source assets/50-ansi-escape-code.sh

clear

echo -e "${YELLOW}------------------ create user (need root permision) ------------------${NC}"
read -p "please enter username: " username
sudo useradd -m $username \
	&& echo -e "${LIGHT_GREEN}create user success${NC}" \
	|| echo -e "${RED}create user failed${NC}"
echo -e "${YELLOW}------------------ create user finish ------------------${NC}"
