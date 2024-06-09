#!/bin/bash

# Function to echo with timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $@"
}

# Function to start the API server
start_api_server() {
    log "Starting API server..."
    gnome-terminal -- bash -c "cd \"$current_dir/fastapi_server\" && python3 -m server; read -p 'Press Enter to exit' " &
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
if [ ! -d "$current_dir/api" ]; then
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

# Install Python packages from requirements.txt
log "Installing Python packages from requirements.txt..."
pip install -r requirements.txt || { log "Error installing Python packages."; exit 1; }

# Add the current directory and the fastapi_server subfolder to PYTHONPATH
log "Adding directories to PYTHONPATH..."
export PYTHONPATH="$PYTHONPATH:$current_dir"
export PYTHONPATH="$PYTHONPATH:$current_dir/fastapi_server"

# Find all subdirectories starting from "utils" and add them to PYTHONPATH
while IFS= read -r -d '' dir; do
    export PYTHONPATH="$PYTHONPATH:$dir"
done < <(find "$current_dir/utils" -type d -print0)

log "Python packages installed and directories added to PYTHONPATH."

# Install necessary npm or yarn packages for the frontend
cd react_app || { log "Directory 'react_app' not found."; exit 1; }

log "Installing npm packages for the frontend..." 
npm install

log "Python packages installed, directories added to PYTHONPATH, and JavaScript packages installed."

# Start the API server
start_api_server

# Start the React app
#start_react_app
