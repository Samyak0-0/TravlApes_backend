#!/bin/bash
docker run -d -p 5000:5000 osrm-car:prepared
docker run -d -p 5001:5000 osrm-bike:prepared
docker run -d -p 5002:5000 osrm-foot:prepared
