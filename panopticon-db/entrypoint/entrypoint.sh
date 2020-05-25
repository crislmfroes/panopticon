#!/usr/bin/bash
mongo admin --host localhost -u root -p test --eval "db.createUser({user: 'panopticon_production', pwd: 'production', roles: [{role: 'readWrite', db: 'panopticon'}]}); db.createUser({user: 'panopticon_devel', pwd: 'development', roles: [{role: 'readWrite', db: 'panopticon'}]}); "