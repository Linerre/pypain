#!/usr/bin/env bash
#
# Archive newspaper or magazine files
#
# Newspaper filenames (case insensitive) should follow this pattern:
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

# Pre-check before moving on
_pre_check() {
    case $ntype in
        1) ls | grep -e "^Financial" | grep -wv -e "UK" ;;
        2) ls | grep -e "^Financial" | grep -w -e "UK" ;;
        3) ls | grep -e "Wall Street" ;;
        4) ls | grep -i -e "Yorker" ;;
        5) ls | grep -E "Economist|TE" ;;
        6) ls | grep -E "Affairs|FA" ;;
    esac
    read -p "Archive these file(s)? [y/n] " agree
    case $agree in
        y|Y) ;;
        n|N) echo "Exit" ; exit 0 ;;
        * ) echo "Reply unrecognizable: ${agree}"
            exit -12
    esac
}

_move_news() {
    for f in $query ; do
        local len=${#f}
        if [[ "$len" -lt 8 ]] ; then
            echo "========================================================"
            echo "File name length incorrect!" >&2
            echo "Expect: [DD_MM_YY??] or [DD.YY.YY??]" >&2
            echo "Found: >>> ${f} <<<"
            echo "========================================================"
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
               echo "Invalid file: >>> ${category} ${f} <<<" >&2
               echo "========================================================"
               echo "Failed to archive due to the above error" >&2
               exit -11
        esac

        local m=${f:3:2}
        case $m in
            [0-9][0-9]) ;;
            *) echo "==========================================================="
               echo "Month format should be [MM] but found invalid month: [${m}]" >&2
               echo "Invalid file: >>> ${category} ${f} <<<" >&2
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

# TE-YYYY-MM-DD-TYP.suffix
_move_te() {
    for f in $query ; do
        case $f in
            The*|Economist )
                echo "Expect 'TE-<DATE>.<suffix>' but found '<${f}>', skipping it ..."
                continue
                ;;
            * )
        esac

        if [[ ${#f} -lt 20 ]] ; then
            echo "==========================================================="
            echo "File name length incorrect!" >&2
            echo "Expect: [DD_MM_YY??] or [DD.YY.YY??]" >&2
            echo "Found: >>> ${f} <<<" >&2
            echo "==========================================================="
            exit -10
        fi

        local y=${f:3:4}
        case $y in
            ${year}) ;;
            *) echo "$f does not belong to ${year}, skipping it ..."
               continue
        esac
        local m=${f:8:2}
        local d=${f:11:2}
        local s=${f:18}
        local t=${dest}/${y}/${m}/${d}
        if [[ ! -d "${t}" ]] ; then
            echo "${t} does not exist yet, creating it ..."
            mkdir -p "${t}"
        fi

        echo "Moving ${f} to ${t} as ${m}_${d}.${s}"
        mv "${f}" "${t}/${m}_${d}.${s}"
    done
}

case $ntype in
    1)
        _pre_check
        category="Financial Times"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "^Financial" | grep -wv -e "UK" | awk '{print $3}' )
        suffix="_eu"
        dest="${documents}/FT"
        _move_news
        ;;
    2)
        _pre_check
        category="Financial Times UK"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "^Financial" | grep -w -e "UK" | awk '{print $4}' )
        suffix="_uk"
        dest="${documents}/FT"
        _move_news
        ;;
    3)
        _pre_check
        category="The Wall Street Journal"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -e "Wall Street" | awk '{print $5}' )
        suffix=
        dest="${documents}/WSJ"
	      _move_news
        ;;
    4)
        _pre_check
        category="The New Yorker"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -i -e "Yorker" | awk '{print $4}' )
        suffix=
        dest="${documents}/TNY"
        _move_news
        ;;
    5)
        _pre_check
        category="The Economist"
        echo "To archive [${ntype}] ${category} ... "
        query=$( ls | grep -E "Economist|TE" | awk '{print $1}' )
        suffix=
        dest="${documents}/TE"
        _move_te
        ;;
    6)
        _pre_check
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

exit 0
