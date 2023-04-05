#!/usr/bin/env bash
#
# Move newspaper or magazine files from SOURCE to DESTINATION
#

echo "
     Choose news type to be archived:
     [1] Financial Times International
     [2] Financial Times UK
     [3] Wall Street Journal
     [4] New Yorker
     [5] Economist
     [6] Foreign Affairs
"

read -p "Type number: " news_type

# TODO: validate user input in the range of 1-6
echo "To archive ${news_type}"
