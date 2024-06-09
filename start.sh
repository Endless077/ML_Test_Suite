#!/bin/bash

# Function to echo with timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $@"
}

# Function to start the API server
start_api_server() {
    log "Starting API server..."
    gnome-terminal -- bash -c "cd \"$current_dir/fastapi_server\" && python3 -B -m server; read -p 'Press Enter to exit' " &
}

# Function to start the React app
start_react_app() {
    log "Starting React app..."
    gnome-terminal -- bash -c "cd \"$current_dir/react_app\" && npm run dev; read -p 'Press Enter to exit' " &
}

# Get the absolute path of the current directory
current_dir=$(pwd)

###################################################################################################

log "FastAPI and React app startup"

# Check if both directories exist
if [ ! -d "$current_dir/fastapi_server" ]; then
    log "Directory 'fastapi_server' not found."
    exit 1
fi

if [ ! -d "$current_dir/react_app" ]; then
    log "Directory 'react_app' not found."
    exit 1
fi

if [ ! -d "$current_dir/utils" ]; then
    log "Directory 'utils' not found."
    exit 1
fi

if ! command -v gnome-terminal &> /dev/null; then
    log "gnome-terminal could not be found. Please install it and try again."
    exit 1
fi

# Function to add a directory to PYTHONPATH if not already added
add_to_pythonpath() {
    local dir="$1"
    if [[ ":$PYTHONPATH:" != *":$dir:"* ]]; then
        export PYTHONPATH="$PYTHONPATH:$dir"
    fi
}

# Add current directory and necessary subdirectories to PYTHONPATH
log "Adding necessary directories to PYTHONPATH..."
add_to_pythonpath "$current_dir"
add_to_pythonpath "$current_dir/fastapi_server"

# Find and add all subdirectories of "utils" to PYTHONPATH
while IFS= read -r -d '' dir; do
    add_to_pythonpath "$dir"
done < <(find "$current_dir/utils" -type d -print0)

log "Directories added to PYTHONPATH."

# Start the API server
start_api_server

# Start the React app (uncomment if needed)
# start_react_app
