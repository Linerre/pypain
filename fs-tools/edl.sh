#!/usr/bin/env bash

# Download, rename and archive an ebook in one sitting
# URL usually looks like this
# https://<domain>/path/to/title.pdf

DEST="$HOME/Documents/books"
[[ ! -d "$DEST/temp" ]] && mkdir "$DEST/temp"
TEMPDIR="${DEST}/temp"

# Check if a URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi


# Set up an exit trap to delete the temporary directory on script exit
cleanup() {
  rm -r "$temp_dir"
}

# Trap exit signals and execute the cleanup function
# trap cleanup EXIT

download() {

    # Looks for ``.*filename="(anything)'' and extract ``anything'' part
    filename=$(curl -sI "$1" | grep -i 'content-disposition' | sed -n 's/.*filename="\([^"]*\).*/\1/p')

    if [ -z "$filename" ]; then
        echo "Could not determine the remote filename."
        exit 1
    fi

    # Extract title from the filename
    title=$(echo "$filename" | sed "s/\s*([0-9]*)\s*//" | awk -F ' - ' '{print $2}')
    # -d -t (use template)


    # This `./' is not allowed and mktemp creates a dir undert /tmp by default
    # local temp_dir=$(mktemp --directory -t ./black.XXXXXXX)

    #-OJLw
    # -s --silent
    # -S --show-error
    # -- output-dir
    # --write '%{filename_effective}\n' \
    echo "== Start downloading ..."
    echo "== filename: $filename"
    local URL="$1"
    curl --output-dir "$TEMPDIR" \
         --remote-name \
         --remote-header-name \
         --location ${URL}

    cd "$TEMPDIR"
    echo "== Now in $TEMPDIR"
    echo "== Renaming $filename"
    mv "$filename" "$title"
    echo "== New filename $title"

    echo "== Copying the downloaded file to $DEST"
    mv "$title" "${DEST}"/
    echo "== File saved as ${DEST}/${title}"

    cd -
    echo "== DONE =="
}

download $1

unset -v DEST TEMPDIR
unset -f download
exit 0
