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
read -p "Type number: " ntype

if [[ ${ntype} -gt 6 || ${ntype} -lt 0 ]]; then
    echo "Type must be a number between 1 and 6. Given: ${ntype}" >&2
    exit 1
fi


download="${HOME}/Downloads"
document="${HOME}/Documents"

cd $download/Telegram\ Desktop
echo "Moved into" $(pwd)

case $ntype in
    1 )
        echo "To archive [${ntype}] Financial Times International ... "
        query=$( ls | grep -e "^Financial" | grep -wv -e "UK" | awk '{print $3}' )
        for f in $query; do
            echo $f
        done
        ;;
    2 )
        query=$( ls | grep -e "^Financial" | grep -w -e "UK" | awk '{print $4}' )
        for f in $query; do
            echo $f
        done
        ;;
    3 )
        query=$( ls | grep -e "Wall Street" | awk '{print $5}' )
        for f in $query; do
            echo $f
        done
        ;;
    4 )
        query=$( ls | grep -i -e "Yorker" | awk '{print $1}' )
        for f in $query; do
            echo $f
        done
        ;;
    5 )
        query=$( ls | grep -E "Economist|TE" | awk '{print $1}' )
        for f in $query; do
            echo $f
        done
        ;;
    6 )
        query=$( ls | grep -i -e "Affairs" | awk '{print $1}' )
        for f in $query; do
            echo $f
        done
        ;;
    * ) echo "Unknown Category " ; exit -1 ;;
esac


# ----------------------- CLEAN ----------------------
unset ntype download document
