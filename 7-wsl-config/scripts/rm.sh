#!/bin/bash

# Program: move files and directorise to a temp directory instead of removing these files directly.
# DeltaV235	2019/9/14	V1.0

tempDir=.recycle

if [ -d ~/$tempDir ];then
	mv $@ ~/$tempDir
else
	mkdir ~/$tempDir
	mv $@ ~/$tempDir
fi
