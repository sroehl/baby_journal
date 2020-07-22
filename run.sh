#!/usr/bin/env bash

#source /home/steve/venv/baby_journal/bin/activate
export BABY_DB_LOC=/data/baby_journal.db

gunicorn --bind 0.0.0.0:5000 --certfile cert/certificate.pem --keyfile cert/private-key.pem run:app
