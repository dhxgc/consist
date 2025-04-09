#!/bin/sh

python /app/app.py &
python /app2/app.py &
nginx -g "daemon off;"