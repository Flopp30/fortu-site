#!/bin/sh

ENV_FILE=${1:-.env}

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: file $ENV_FILE not found."
    return 1 2>/dev/null || exit 1
fi

echo "Load variables from $ENV_FILE..."

export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "Done!"
