#!/bin/bash

sudo apt update
sudo apt install -y redis libsass-dev

curl https://nim-lang.org/choosenim/init.sh -sSf | sh
echo 'export PATH=/home/vscode/.nimble/bin:$PATH' >> ~/.bashrc
