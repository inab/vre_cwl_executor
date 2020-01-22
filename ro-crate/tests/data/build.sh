#!/usr/bin/env bash

mkdir -p build
cp -r src/* build/
cd build
for dir in *
do
    if [[ ! -e $dir ]]; then
        bdbag --update --archive zip "$dir"
    elif [[ ! -d $dir ]]; then
        echo "$dir exists" 1>&2
    fi
done