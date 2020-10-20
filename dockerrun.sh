#!/usr/bin/env bash
# Bash file to set env vars in settings.json and start the bot

# Make sure we are in correct directory
cd /app

# Use sed to add token env
sed -i "s/\"token\": \".*\"/\"token\": \"$TOKEN\"/" settings.json

# Use sed to add role env
sed  -i "s/\"role\": .*,/\"role\": $ROLE,/" settings.json

#Use sed to add channel env
sed  -i "s/\"channel\": .*,/\"channel\": $CHANNEL,/" settings.json

#Run the bot
python /app/bot.py
