#!/bin/bash

cat /tmp/ngi_uwsgi_flaskapp.pid | while read p;do kill $p ;done
