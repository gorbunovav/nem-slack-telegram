#!/bin/bash

[ -e config.ini ] && rm config.ini

config=$(<config_template.ini);
config="${config//\%slack-api-key\%/$SLACK_KEY}";
config="${config//\%telegram-api-key\%/$TELEGRAM_KEY}";
printf '%s\n' "$config" >config.ini


config=$(<bridge.py);
config="${config//SLACK_CHANNEL_MATCHING = \{*-146980320\}/SLACK_CHANNEL_MATCHING = \{$SLACK_CHANNELS\}}";
printf '%s\n' "$config" >bridge.py

exec "$@"
