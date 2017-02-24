#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:5000 --certfile cert/certificate.pem --keyfile cert/private-key.pem run:app
