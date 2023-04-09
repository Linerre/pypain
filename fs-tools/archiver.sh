#!/usr/bin/env bash
#
# Archive newspaper or magazine files
#

echo \
"Choose news type to be archived:
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

downloads="${HOME}/Downloads"
documents="${HOME}/Documents"

cd ${downloads}/Telegram\ Desktop
echo "Moved into" $(pwd)

case $ntype in
    1)
        category="Finacial Times International"
        echo "To archive [${ntype}] ${category} ... "
        # query=$( ls | grep -e "^Financial" | grep -wv -e "UK" | awk '{print $3}' )
        query=$( ls | grep -E "^Financial|^FT" | grep -wv -e "UK" )
        dest="${documents}/FT"
        ;;
    2)
        category="Finacial Times UK"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "^Financial" | grep -w -e "UK" | awk '{print $4}' )
        dest="${documents}/FT"
        ;;
    3)
        category="The Wall Street Journal"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "Wall Street" | awk '{print $5}' )
        dest="${documents}/WSJ"
        ;;
    4)
        category="The New Yorker"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -i -e "Yorker" | awk '{print $1}' )
        dest="${documents}/TNY"
        ;;
    5)
        category="The Economist"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -E "Economist|TE" | awk '{print $1}' )
        dest="${documents}/TE"
        ;;
    6)
        category="Foreign Affaris"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -i -e "Affairs" | awk '{print $1}' )
        dest="${documents}/FA"
        ;;
    *) echo "Unknown Category " ; exit -1 ;;
esac

format_checker() {
    for f in $query; do
        local d=${f:0:2}
        local m=${f:3:2}
        local t=${dest}/${m}

        case $m in
            [0-9][0-9]) ;;
            *) echo "Month format should be [MM] but found invalid month: [${m}]" >&2
               echo "Invalid file: ${category} ${f}" >&2
               echo "Failed to archive due to the above error" >&2
               exit -11
        esac
        case $d in
            [0-9][0-9]) ;;
            *) echo "Day format shoould be [DD] but Found invalid day: [${d}]" >&2
               echo "Invalid file: ${category} ${f}" >&2
               echo "Failed to archive due to the above error" >&2
               exit -11
        esac

        if [[ ! -d "${t}"  ]]; then
            echo "${t} does not exist yet, creating it ..."
            # mkdir -p "${t}"
        fi
    done
}

move_news() {
    echo "Checking month and day formats ..."
    format_checker
    echo "Archiving ${category}-${m}-${d} ${f} to ${dest}/${m}/${d}"
}

move_news

# ----------------------- CLEAN ----------------------
unset ntype download document query category dest
