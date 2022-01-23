#!/usr/bin/bash

for version in {6..10};
    do
        filename="Python-3$version.asdl";
        wget "https://raw.githubusercontent.com/python/cpython/3.$version/Parser/Python.asdl" -O $filename;
        echo -e "-- version=3.$version\n$(cat $filename)" > $filename
    done;
