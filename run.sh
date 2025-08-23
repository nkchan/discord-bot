#!/bin/bash

# Change to the script's directory to ensure correct relative paths
cd "$(dirname "$0")"

# Execute the bot using the Python interpreter from the virtual environment
# The .env file will be loaded by the systemd service
./venv/bin/python ./discord_bot.py
