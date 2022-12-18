#!/bin/bash

echo "Clonning the git repo to proceed with the deployment"
git clone https://github.com/ZineddineAlch/LOG8415-Project.git
echo "Some set up"
echo "1-Please make sure you updated .aws/Creadentials"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo "2-Please enter the .pem file of your key pair names 'vockey' in the root folder of lab1_log8415/src"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

python launch.py