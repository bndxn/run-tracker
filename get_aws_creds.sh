#!/bin/bash

set -e

echo "Fetching temporary AWS credentials..."
CREDS=$(aws sts get-session-token --duration-seconds 3600 \
    --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
    --output text)

read AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN <<< "$CREDS"

# Create a new file without existing AWS keys
grep -vE '^AWS_ACCESS_KEY_ID=|^AWS_SECRET_ACCESS_KEY=|^AWS_SESSION_TOKEN=' .env > .env.tmp || true

# Append the new AWS credentials
cat <<EOF >> .env.tmp
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN
EOF

# Replace the old .env with the new one
mv .env.tmp .env

echo ".env file updated with new AWS credentials."
