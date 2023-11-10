#!/usr/bin/env bash

# Download, rename and archive an ebook in one sitting
# URL usually looks like this
# https://<domain>/path/to/title.pdf

coll="$HOME/Documents/books/"

download() {
    local URL=$1
    echo "To download from: $URL"
    #-OJLw
    # -s --silent
    # -S --show-error
    curl --write '%{filename_effective}\n' \
         --silent \
         --show-error \
         --output-dir "$coll" \
         --remote-name \
         --remote-header-name \
         --location ${URL}
}

download $1
