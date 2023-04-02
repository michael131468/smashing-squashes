#!/bin/sh

# Container entrypoint script
# - Reconfigure the smashing authentication token to AUTH_TOKEN environment
# - Launch smashing dashboard as daemon
# - Launch feeder script

cd dashboard
sed -e "s/YOUR_AUTH_TOKEN/${AUTH_TOKEN}/" config.ru > /tmp/config.ru
cp /tmp/config.ru ./config.ru
smashing start &
sleep 1
python3 ../feeder/feeder.py
