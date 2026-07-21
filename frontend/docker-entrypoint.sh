#!/bin/sh
set -e

# Replace API URL placeholder at runtime
if [ -n "$VITE_API_URL" ]; then
    echo "Setting API URL to: $VITE_API_URL"
    find /usr/share/nginx/html -type f -name "*.js" -exec sed -i "s|__API_URL__|$VITE_API_URL|g" {} \;
fi

exec "$@"