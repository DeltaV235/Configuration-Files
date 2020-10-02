#!/bin/bash

### descrption: get distribution name
### create time: 2020-10-02 (yyyy-MM-dd)
### author: deltaV235

if [ '${OS_NAME}' -eq "ubuntu" ] then;
	PACKAGE_MANAGER="apt"
elif [ '${OS_NAME}' -eq "centos" ] then;
	PACKAGE_MANAGER="yum"
end

echo -e "${PACKAGE_MANAGER}"
