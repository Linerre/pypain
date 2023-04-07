#!/usr/bin/env bash
# set -x

# -------------------- SET UP ---------------------
read -p "Full Year (4-digit)? > " year
if [[ ${#year} -eq 0 ]]; then
    # Default to this year
    year=$(date +"%Y")
fi
read -p "World or UK? [w/u] > " category
if [[ ${#category} -eq 0 ]]; then
    # Default to UK
    category="u"
fi

printf "Archive news of the year %s\n" $year

dw="$HOME/Downloads"
dc="$HOME/Documents"
back=$(pwd)

# -------------------- LOGIC ---------------------
move_ft() {
    cd $dw
    cd "Telegram Desktop"
    echo "Moved into: " $(pwd)
    # File name: `Financial Times DD-MM-YY.pdf'
    case $category in
        "w")
            local fts=$( ls | grep -e "^Financial" | grep -wv -e "UK" | awk '{print $3}' )
            local pfx="Financial Times"
            local sfx="in"
            ;;
        "u")
            local fts=$( ls | grep -e "^Financial" | grep -w -e "UK" | awk '{print $4}')
            local pfx="Financial Times UK"
            local sfx="uk"
            ;;
        *)
            echo "Expect category of w/u, given" $category
            return -10
    esac

    local y=${year}
    for ft in $fts; do
        local d=${ft:0:2}
        local m=${ft:3:2}
        # Create the month dir as needed
        local des=${dc}/FT/${y}/${m}
        [[ -d $des ]] || mkdir $des
        local src="${pfx} ${ft}"
        local nn="${d}-${sfx}.pdf"
        case $m in
            "01" )
                printf "Moving January issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "02" )
                printf "Moving Feburary issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "03" )
                printf "Moving March issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "04" )
                printf "Moving April issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "05" )
                printf "Moving May issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "05" )
                printf "Moving June issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "07" )
                printf "Moving July issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "08" )
                printf "Moving August issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "09" )
                printf "Moving Semptember issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "10" )
                printf "Moving October issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "11" )
                printf "Moving November issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
                ;;
            "12" )
                printf "Moving December issue %s\n" "$src"
                mv "${src}" "${des}/${nn}"
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
unset dw dc category year back
unset -f move_ft
