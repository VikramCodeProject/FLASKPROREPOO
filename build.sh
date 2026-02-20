#!/bin/bash
set -o errexit

pip install -r requirements.txt

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "Build completed successfully!"
