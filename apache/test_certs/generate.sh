#!/bin/bash

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $1-selfsigned.key -out $1-selfsigned.crt \
-subj "//C=US/ST=North Carolina/L=Raleigh/O=Home/CN=$1"