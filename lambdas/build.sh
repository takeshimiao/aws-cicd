#!/usr/bin/env bash

function print_usage() {
    echo "$0 <src-lib-dir> <dest-lib-dir> <dist-dir> <version>"
}

if [ $# -ne 4 ]; then
    echo '# of argument MUST be 4 !'
    print_usage
    exit 1
fi

src_lib_dir="$1"
dest_lib_dir="$2"
dist_dir="$3"
version="$4"

if ! [ -d $src_lib_dir ]; then
    echo "src_lib_dir:$src_lib_dir does not exist !"
    exit -1
fi

if ! [ -d $dest_lib_dir ]; then
    mkdir $dest_lib_dir
fi

if ! [ -d $dist_dir ]; then
    mkdir $dist_dir
fi

# cp needed libs
cp -r $src_lib_dir/* $dest_lib_dir/


# packaging each lambda functions
src_lib_dir_name=`echo "$src_lib_dir" | awk -F '/' '{print $NF}'`
dist_lib_dir_name=`echo "$dist_dir" | awk -F '/' '{print $NF}'`
for l_dir in `find . -maxdepth 1 -type d | tail -n +2 | awk -F '/' '{print $NF}'`; do
    if [ "$l_dir" == "$src_lib_dir_name" ] || [ "$l_dir" == "$dist_lib_dir_name" ] ; then
        continue
    fi
    z_f="$l_dir-$version.zip"
    pushd $dest_lib_dir/
    zip -r $z_f *
    [ $? -ne 0 ] && echo "make zip file for lambda:$l_dir failed !" && exit 1
    mv $z_f ../$l_dir/
    popd
    pushd $l_dir/
    zip -r $z_f *
    mv $z_f $dist_dir/
    popd
done
