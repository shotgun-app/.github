#!/bin/sh
set -e
cd /home/lebar/projects/shotgun-app/shotgun-api
docker compose exec -T db psql -U shotgun -d shotgun -q < seeds/demo.sql
docker compose exec -T db psql -U shotgun -d shotgun -qc "delete from rides where driver_id='a0000000-0000-4000-8000-000000000001' and destination_city='Rome'; delete from sessions"
cd /tmp/claude-1000/-home-lebar-projects-shotgun-app/a7cd1ea2-a2a0-46b5-b66d-04fa9a96cef8/scratchpad/video
python3 record.py
