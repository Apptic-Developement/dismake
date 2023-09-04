#!/bin/bash

# Check if a folder path is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

# Get the folder path from the first argument
folder_path="$1"

# Use the find command to locate and remove __pycache__ folders
find "$folder_path" -type d -name "__pycache__" -exec rm -r {} +

echo "Removed all __pycache__ folders in $folder_path"