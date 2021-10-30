#!/bin/sh
cd /volume1/repos/zwift/zwift-workout
/bin/git fetch --all
/bin/git reset --hard origin/main
/bin/git pull origin main
/usr/local/bin/docker-compose build
/usr/local/bin/docker-compose up -d