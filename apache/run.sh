#!/bin/bash

# Start Shibd
service shibd start

# Start httpd
exec apache2ctl -D FOREGROUND
