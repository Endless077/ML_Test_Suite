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

# Check if the current directory is in PYTHONPATH
is_in_pythonpath=false

IFS=':' read -ra pythonpath_dirs <<< "$PYTHONPATH"
for dir in "${pythonpath_dirs[@]}"; do
    if [ "$dir" == "$current_dir" ]; then
        is_in_pythonpath=true
        break
    fi
done

# If the current directory is not in PYTHONPATH, add it along with the 'fastapi_server' subdirectory and subdirectories of 'utils'
if [ "$is_in_pythonpath" = false ]; then
    log "Current directory is not in PYTHONPATH. Adding directories to PYTHONPATH..."
    export PYTHONPATH="$PYTHONPATH:$current_dir"
    export PYTHONPATH="$PYTHONPATH:$current_dir/fastapi_server"

    # Find all subdirectories starting from "utils" and add them to PYTHONPATH
    while IFS= read -r -d '' dir; do
        export PYTHONPATH="$PYTHONPATH:$dir"
    done < <(find "$current_dir/utils" -type d -print0)

    log "Python packages installed and directories added to PYTHONPATH."
else
    log "Current directory is already in PYTHONPATH."
fi

# Start the API server
start_api_server

# Start the React app
#start_react_app
