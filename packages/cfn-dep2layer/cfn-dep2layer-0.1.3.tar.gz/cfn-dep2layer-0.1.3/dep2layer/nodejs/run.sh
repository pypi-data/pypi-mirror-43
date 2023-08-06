#!/usr/bin/env bash 
cd /var/task/src

mkdir /tmp/nodejs
mkdir /tmp/.dep2layer
cp package.json /tmp/nodejs
cp package.json /tmp/.dep2layer/package.json
if [ -e package-lock.json ]; then
  cp package-lock.json /tmp/nodejs/package-lock.json
  cp package-lock.json /tmp/.dep2layer/package-lock.json
fi

mkdir /tmp/home
export HOME=/tmp/home #In lambci/lambda:nodejs8.10, default home path doesn't exist

cd /tmp/nodejs
npm r aws-sdk
code=$?
if [ $code != 0 ]; then
  echo Install faild. Exit code $code
  exit $code
fi

rm package.json
rm package-lock.json
rm -rf $HOME