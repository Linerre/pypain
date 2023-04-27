#!/bin/env  bash
#
# Clean all but PKGBUILD
#

echo "THIS SCRIPT WILL CLEAN ALL BUT 'PKGBUILD' FILES."

PDIR="${HOME}/projects/pkgbuilds/"

echo "Entering PKGBUILD dir ... "
cd ${PDIR}

for c in $( ls ${PDIR} ) ; do
    # category dir
    if [[ -d $c ]]; then
        cd $c
        echo "Entering CATEGORY: $c"
        for p in $( ls ) ; do
            echo "Entering PACKAGE dir: $p"
            # package dir
            if [[ -d $p ]] ; then
                cd $p
                for f in $( ls ); do
                    # file
                    case $f in
                        PKGBUILD) ;;
                        *) echo "============= WARNING ==========="
                           echo "Removing >> $f <<"
                           rm -rf $f
                           ;;
                    esac
                done
                echo "Leaving PACKAGE dir $p"
                cd ../
                echo "Entering CATEGORY dir: " $(pwd)
            fi
        done
    else
        echo "$p is not a directory, skipping ..."
    fi
done

unset PDIR
exit 0
