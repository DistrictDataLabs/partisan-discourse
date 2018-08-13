#!/bin/bash
# Restores the local development database from a production backup.

# Capture and download a database backup
heroku pg:backups:capture
heroku pg:backups:download

# Run the postgresql restore
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U django -d partisan latest.dump

# Cleanup
rm latest.dump
