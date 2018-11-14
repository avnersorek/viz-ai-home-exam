#!/usr/bin/env bash
set -e
docker build -t viz-exam .
docker run --rm -p 5000:5000 -v $(pwd):/app viz-exam
