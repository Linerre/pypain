#!/usr/bin/env bash
#
# File name: `Financial Times DD-MM-YY.pdf or FT_DDMMYYYY.pdf'l
#
# set -x

# -------------------- SET UP ---------------------
read -p "Full Year (4-digit)? > " year
if [[ ${#year} -eq 0 ]]; then
    # Default to this year
    year=$(date +"%Y")
fi

printf "Archive news of the year %s\n" $year

dw="$HOME/Downloads"
dc="$HOME/Documents"
back=$(pwd)

# -------------------- LOGIC ---------------------
_mov() {
    if [[ -f "$2" ]]; then
        echo "$2 exists; skipping ..."
    else
        mv "$1" "$2"
    fi
}

move_ft() {
    cd $dw
    cd "Telegram Desktop"
    echo "Moved into: " $(pwd)
    local fts=$( ls | grep -e "^FT" )
    local pfx="Financial Times"
    local sfx="eu"

    local y=${year}
    for ft in $fts; do
        local d=${ft:3:2}
        local m=${ft:5:2}
        # Create the month dir as needed
        local des=${dc}/FT/${y}/${m}
        [[ -d $des ]] || mkdir $des
        local nn="${d}-${sfx}.pdf"
        case $m in
            01 )
                printf "Moving January issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            02 )
                printf "Moving Feburary issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            03 )
                printf "Moving March issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            04 )
                printf "Moving April issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            05 )
                printf "Moving May issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            05 )
                printf "Moving June issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            07 )
                printf "Moving July issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            08 )
                printf "Moving August issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            09 )
                printf "Moving Semptember issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            10 )
                printf "Moving October issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            11 )
                printf "Moving November issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            12 )
                printf "Moving December issue %s\n" "$ft"
                _mov "${ft}" "${des}/${nn}"
                ;;
            * )
                printf "Found strange month: %s\n" $m
                return -11
        esac
    done
    cd $back
    echo "Return back to " $back
}

# ----------------------- CALL FN --------------------
move_ft

# ----------------------- CLEAN ----------------------
unset dw dc year back
unset -f move_ft
