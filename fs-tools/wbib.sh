#!/usr/bin/env bash
: '
Script Name: wbib.sh
Description: This script generates a bib entry for a given wikipedia page.  The entry
will be inserted to one of the designated files under $HOME/projects/ord/bibs/wiki.
If no specific category is passed via option `p`, then the entry is recorded in
`uncate.bib` under the abovementioned directory.

Usage:
  wbib <PAGE_TITLE> [options]

Options:
  -c            Set the category for the entry, must be one of pp,cs,ft

Page Titles:
Page titles should not contain whitespace characters.  Use `_` to replace them.  Notice
that these titles might appear in the encoded format in the page urls.  `B+_tree` in the
corresponding url is shown as `B%2B_tree` where `+` sign is encoded into `%2B`.
'

usage() { echo "Usage: $0 <PAGE_TITLE> [-c <pp|cs|ft>]" 1>&2; exit 1; }

# Check if any argument is given
[ "$#" -eq 0 ] && usage

# Extract the first argument as a string
PAGE_TITLE="$1"
echo "== To fech entry for $first_arg"

# Check if the first argument is a string
if [[ ! "$PAGE_TITLE" =~ ^[[:alpha:]_\+\-]+$ ]]; then
    echo "[Err]: First argument should NOT contain whitespace or any non-letter characters."
    exit 1
fi

# No whitespace in page title (must encoded using `%20`)
# grep optipns:
# -q, --quiet
# -s, --no-message
# if echo "$1" | grep -q '\s'; then
#     echo "[Err]: Page title contains whitespace character: $1"
#     exit 1
# fi

# Specify the API endpoint
API_URL="https://en.wikipedia.org/w/api.php"

# User-Agent
USR_AGT="Nobody/0.0.1 (Arch; Buu) Auto/0.0.1"

# Dest
DEST="${HOME}/projects/org/bibs/wiki"
CATE="uncate.bib"

# :c disables verbose error handling
# c: means `p` option takes an argument
while getopts ":c:" opt; do
    case "$opt" in
        c)
            case "$OPTARG" in
                pp)
                    echo "== Setting CATEGORY to people.bib"
                    CATE="people.bib"
                    ;;
                cs)
                    echo "== Setting CATEGORY to compsci.bib"
                    CATE="compsci.bib"
                    ;;
                ft)
                    echo "== Setting CATEGORY to font.bib"
                    CATE="fonts.bib"
                    ;;
            esac
            ;;
        \?)
            echo "[Err]: Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "[Err]: Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
        *)
            echo "== Option arg not given as one of pp|cs|ft"
            echo "== Using default: uncate.bib"
            ;;
    esac
done

URL=
DATE=
REVID=
ENTRY=

# https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=revisions%7Cinfo&titles=Merkle_tree&formatversion=2&rvprop=timestamp%7Cids&rvlimit=5&inprop=url
fetch() {
    # Use curl to retrieve information from the Wikipedia API
    # -H --header "Agent: name/version"
    # -A --user-agent
    # -G --get
    echo "== Start fetching ..."
    local page_info=$(
        curl -s "$API_URL" \
             -A "$USR_AGT" \
             --get \
             --data-urlencode "action=query" \
             --data-urlencode "format=json" \
             --data-urlencode "prop=info" \
             --data-urlencode "titles=$PAGE_TITLE" \
             --data-urlencode "formatversion=2" \
             --data-urlencode "inprop=url" |
            jq -r '.query.pages[0] | {title: .title, url: .editurl, date: .touched, id: .lastrevid}'
          )
    echo
    echo "== Filtered page info as follows:"
    echo "---------------------------------"
    echo $page_info | jq -r '.'
    echo "---------------------------------"
    echo

    ENTRY=$( echo "$page_info" | jq -r '.title' )
    echo "== ENTRY: $ENTRY"
    REVID=$( echo "$page_info" | jq -r '.id' )
    echo "== REVID: $REVID"
    DATE=$( echo "$page_info" | jq -r '.date' | awk -F'T' '{print $1}' )
    # DATE=${DATE%%T*}
    echo "== DATE: $DATE"
    URL=$( echo "$page_info" | jq -r '.url' | awk -F'&' '{print $1}' )
    URL="${URL}&oldid=${REVID}"
    echo "== URL: $URL"
}

record() {
    local today=$( date +"%Y-%m-%d" )
    local wentry=$(
        cat <<EOF
 @online{wiki:$PAGE_TITLE,
   author = {{Wikipedia contributors}},
   shortauthor = {Wikipedia},
   date = {$DATE},
   title = {$ENTRY},
   organization = {{Wikipedia}{,} The Free Encyclopedia},
   url = {$URL},
   urldate = {$today},
}
EOF
          )
    echo
    echo "== Trying to add the following entry:"
    echo "-------------------------------------"
    echo "$wentry"
    echo "-------------------------------------"
    echo
    read -p "Proceed? (y/n): " answer
    # Check if the input is "y" (case-insensitive)
    if [[ "$answer" == [Yy] ]]; then
        if [ -f "${DEST}/${CATE}" ]; then
            # Add a newline to separate entries
            echo >> "${DEST}/${CATE}"
            echo "$wentry" >> "${DEST}/${CATE}"
        else
            echo "[Err]: ${DEST}/${CATE} not found"
            exit 1
        fi
        echo "== Added one entry to $CATE"
    else
        echo "Exiting. No action taken."
    fi
}

fetch
record

unset -v DATE URL API_URL USR_AGT
unset -f fetch

exit 0
