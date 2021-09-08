#!/bin/sh

kill -9 $(ps aux | grep -e "crypto_run.py" | awk '{ print $2 }') 
