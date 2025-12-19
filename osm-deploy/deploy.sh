#!/bin/bash

docker build -f ./Dockerfile-car -t osm-car:prepared .
docker build -f ./Dockerfile-bike -t osm-car:prepared .
docker build -f ./Dockerfile-foot -t osm-car:prepared .
