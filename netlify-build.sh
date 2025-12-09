#!/bin/bash
# Netlify build script to inject environment variables into frontend

# Create a script that will inject API_BASE_URL into index.html
if [ -n "$API_BASE_URL" ]; then
    # Replace the API_BASE_URL placeholder in index.html
    sed -i.bak "s|window.API_BASE_URL = window.API_BASE_URL |||window.API_BASE_URL = '$API_BASE_URL' |||g" frontend/index.html
    rm -f frontend/index.html.bak
fi

echo "Build completed successfully"

