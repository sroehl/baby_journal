#!/usr/bin/env bash

celery worker -A app.celery --loglevel=info
