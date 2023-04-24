#!/usr/bin/env bash
#
# Ask me about the `version' of any given argument
#


# echo "The version of $1 is: "

# Check if cmd exists (installed)
_check_cmd() {
    local cmd=$1
    which $cmd > /dev/null 2>&1
    local res=$?
    case $res in
        1) echo "$cmd not installed"; exit -11 ;;
        *) ;;
    esac
}

_check_cmd $1


print_version() {
    local cmd=$(basename $1)
    case $cmd in
        clj)
            echo "------------------------------"
            echo "FORMULA: $cmd --version"
            echo "------------------------------"
            $cmd --version
            ;;

        emacs)
            echo "------------------------------"
            echo "FORMULA: $cmd --version"
            echo "------------------------------"
            $cmd --version
            ;;
        go)
            echo "----------------------------"
            echo "FORMULA: $cmd version"
            echo "----------------------------"
            $cmd version
            ;;
        rustc)
            echo "----------------------------"
            echo "FORMULA: $cmd -V | --version"
            echo "----------------------------"
            $cmd --version
            ;;
        solana)
            echo "----------------------------"
            echo "FORMULA: $cmd -V | --version"
            echo "----------------------------"
            $cmd --version
            ;;
        *)
            echo "$cmd installed but not supported yet"
            exit -10
    esac
}

print_version $1

unset -f _check_cmd print_version
