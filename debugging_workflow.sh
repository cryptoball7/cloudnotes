#!/bin/bash

docker compose ps
docker compose logs api
docker compose logs nginx
curl https://cloudnotes.my.to/health

