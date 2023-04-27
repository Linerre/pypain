#!/bin/env  bash
#
# Clean all but PKGBUILD
#

echo "THIS SCRIPT WILL CLEAN ALL BUT 'PKGBUILD' FILES."

PDIR="${HOME}/projects/pkgbuilds/"

echo "Entering PKGBUILD dir ... "
cd ${PDIR}

for c in $( ls ${PDIR} ) ; do
    # category
    if [[ -d $c ]]; then
        cd $c
        echo "Now in CATEGORY: $c"
        for p in $( ls ) ; do
            echo "Now in PACKAGE dir: $p"
            # package
            if [[ -d $p ]] ; then
                cd $p
                for f in $( ls ); do
                    case $f in
                        PKGBUILD) ;;
                        *) echo "============= WARNING ==========="
                           echo "Removing >> $f <<"
                           rm -rf $f
                           echo "============= WARNING ==========="
                           ;;
                    esac
                done
                echo "Moving out of $p"
                cd ../
                echo "Now in CATEGORY dir: " $(pwd)
            fi
        done
    else
        echo "$p is not a directory, skipping ..."
    fi
done

unset PDIR
exit 0
