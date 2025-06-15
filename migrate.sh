#!/bin/bash

echo "Starting database migration..."
flask db migrate
flask db upgrade
echo "Database migration completed!"