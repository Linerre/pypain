#!/usr/bin/env bash
#
# Ask me about the `version' of any given argument
#

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

# If it exits, print its `version' usage and then its current version info
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
        git)
            echo "-----------------------------"
            echo "FORMULA: $cmd -v | --version"
            echo "-----------------------------"
            $cmd version
            ;;
        gcc|g++|cc)
            echo "-----------------------------"
            echo "FORMULA: $cmd --version"
            echo "-----------------------------"
            $cmd --version
            ;;
        ghc*)
            echo "-----------------------------"
            echo "FORMULA: $cmd --version"
            echo "-----------------------------"
            $cmd --version
            ;;
        hugo|go)
            echo "----------------------------"
            echo "FORMULA: $cmd version"
            echo "----------------------------"
            $cmd version
            ;;
        java)
            echo "-------------------------------FORMULA-----------------------------------"
            echo "-version      print product version to the error stream and exit"
            echo "--version     print product version to the output stream and exit"
            echo "-showversion  print product version to the error stream and continue"
            echo "--show-version"
            echo "              print product version to the output stream and continue"
            echo "-------------------------------------------------------------------------"
            $cmd --version
            ;;
        clojure|clj)
            echo "----------------------FORMULA------------------------"
            echo "--version  Print the version to stdout and exit"
            echo "-version   Print the version to stderr and exit"
            echo "-----------------------------------------------------"
            $cmd --version
            ;;
        rustc|rustup)
            echo "-----------------------------"
            echo "FORMULA: $cmd -V | --version"
            echo "-----------------------------"
            $cmd --version
            ;;
        rust-analyzer)
            echo "---------------------------------"
            echo "FORMULA: $cmd --version"
            echo "---------------------------------"
            $cmd --version
            ;;
        solana)
            echo "-----------------------------"
            echo "FORMULA: $cmd -V | --version"
            echo "-----------------------------"
            $cmd --version
            ;;
        tree)
            echo "-----------------------------"
            echo "FORMULA: $cmd --version"
            echo "-----------------------------"
            $cmd --version
            ;;
        tree-sitter)
            echo "-------------------------------------"
            echo "FORMULA: $cmd -V | --version"
            echo "-------------------------------------"
            $cmd --version
            ;;
        *)
            echo "$cmd installed but not supported yet"
            exit -10
    esac
}

print_version $1

unset -f _check_cmd print_version
