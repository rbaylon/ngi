#!/bin/sh

uwsgi -s /tmp/ngi_app.sock --manage-script-name --mount /=run:app --venv ~/.local/share/virtualenvs/xxx >/dev/null 2>&1 &
echo $! > /tmp/ngi_uwsgi_flaskapp.pid
