#!/usr/bin/env bash
#
# Archive newspaper or magazine files
#
# Filname (case insensitive) should follow this pattern:
# "<newspaper> <DATE>.pdf", where <DATE> could be one of the folloiwng
# 1. <DD_MM_YY??>
# 2. <DD.MM.YY??>

echo \
"Choose news type to be archived:
[1] Financial Times EU
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

read -p "Enter 4-digit year [default 2023]: " year
if [[ ${#year} -eq 0 ]] ; then
    year=2023;
fi

downloads="${HOME}/Downloads"
documents="${HOME}/Documents"

cd ${downloads}/Telegram\ Desktop
echo "Moved into" $(pwd)

_move_news() {
    for f in $query ; do
        local len=${#f}
        if [[ "$len" -lt 8 ]] ; then
            echo "File name length incorrect! Expect [DD_MM_YY??] or [DD.YY.YY??] but found [$f]"
            exit -10
        elif [[ "$len" -eq 14 ]] ; then
            # DD_MM_YYYY.pdf
            local y=${f:6:4}
            case $y in
                ${year}) ;;
                *)
                    echo "$f does not belong to year $year, skipping it ..."
                    continue
            esac
        elif [[ "$len" -eq 12 ]] ; then
            # DD_MM_YY.pdf
            local y=${f:6:2}
            case $y in
                ${year:2}) y=${year} ;;
                *)
                    echo "$f does not belong to year $year, skipping it ..."
                    continue
            esac
        fi

        local d=${f:0:2}
        case $d in
            [0-9][0-9]) ;;
            *) echo "========================================================"
               echo "Day format shoould be [DD] but Found invalid day: [${d}]" >&2
               echo "Invalid file: >> ${category} ${f} <<" >&2
               echo "========================================================"
               echo "Failed to archive due to the above error" >&2
               exit -11
        esac

        local m=${f:3:2}
        case $m in
            [0-9][0-9]) ;;
            *) echo "==========================================================="
               echo "Month format should be [MM] but found invalid month: [${m}]" >&2
               echo "Invalid file: >> ${category} ${f} <<" >&2
               echo "==========================================================="
               echo "Failed to archive due to the above error" >&2
               exit -11
        esac

        local t=${dest}/${y}/${m}
        if [[ ! -d "${t}" ]] ; then
            echo "${t} does not exist yet, creating it ..."
            mkdir -p "${t}"
        fi

        echo "Moving ${category} ${f} to ${t} as ${d}${suffix}.pdf"
        mv "${category} ${f}" "${t}/${d}${suffix}.pdf"
    done
}

case $ntype in
    1)
        category="Financial Times"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "^Financial" | grep -wv -e "UK" | awk '{print $3}' )
        suffix="_eu"
        dest="${documents}/FT"
        _move_news
        ;;
    2)
        category="Financial Times UK"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "^Financial" | grep -w -e "UK" | awk '{print $4}' )
        suffix="_uk"
        dest="${documents}/FT"
        _move_news
        ;;
    3)
        category="The Wall Street Journal"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "Wall Street" | awk '{print $5}' )
        suffix=
        dest="${documents}/WSJ"
        ;;
    4)
        category="The New Yorker"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -i -e "Yorker" | awk '{print $4}' )
        suffix=
        dest="${documents}/TNY"
        _move_news
        ;;
    5)
        category="The Economist"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -E "Economist|TE" | awk '{print $1}' )
        suffix=
        dest="${documents}/TE"
        ;;
    6)
        category="Foreign Affaris"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -i -e "Affairs" | awk '{print $1}' )
        suffix=
        dest="${documents}/FA"
        ;;
    *) echo "Unknown Category " ; exit -1 ;;
esac

# ----------------------- CLEAN ----------------------
unset ntype year download document query category dest suffix
