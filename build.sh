#!/bin/bash -x

cur_dir=$(dirname $0)
cur_dir=$(cd ${cur_dir}; pwd)


function usage() {
    echo "$0 Usage: <python_cmd> <lib_dir> <dependency_1> [<dependency_2>...]"
}

if [ $# -le 2 ]; then
    echo 'Pass in arguments MUST greater than 2 !'
    usage
    exit 1
fi

python_cmd="$1"
shift
lib_dir="$1"
shift


py_install_dir="$($python_cmd setup.py develop | egrep '[a-z]+-packages' | tail -1 | awk '{print $2}')"
[ $? -ne 0 ] && echo "Parsing python dist-packages dir failed !" && exit 1
if [[ ! $py_install_dir =~ [a-z]+-packages$ ]]; then
    py_install_dir="$(dirname $py_install_dir)"
fi

declare -i num_dir=$(echo "$py_install_dir" | wc -l)
if [ $num_dir -ne 1 ]; then
    echo "Parsed python dist-packages dir:$py_install_dir failed !"
    exit 1
fi

while [ $# -ne 0 ]; do
    work_dir=$py_install_dir
    lib="$1"
    shift
    if [ ! -e $py_install_dir/$lib ]; then
        tmp_lib=$(ls $py_install_dir | egrep -i $lib)
        if [[ $tmp_lib =~ \.egg$ ]]; then
            tmp_src_lib=$py_install_dir/$tmp_lib
            [ ! -e $tmp_src_lib ] && echo "src lib:$tmp_src_lib does not exist !" && exit 1

            if [ -d $tmp_src_lib ]; then
                lib=$tmp_lib/$lib
            elif [ -f $tmp_src_lib ]; then
                tmp_dir=/tmp/$lib
                rm -rf $tmp_dir
                mkdir $tmp_dir
                cp $tmp_src_lib $tmp_dir/
                pushd $tmp_dir/
                unzip $tmp_lib
                [ $? -ne 0 ] && "Try unzip tmp_lib:$tmp_lib failed !" &&  popd && exit 1
                popd
                work_dir=$tmp_dir
            else
                echo 'Shall not be here !' && exit 1
            fi
        else
            echo "Operation undefined for tmp_lib:$tmp_lib" && exit 1
        fi
    fi
    src_lib_dir=$work_dir/$lib
    echo "cp lib:${src_lib_dir}* to lib_dir:$lib_dir"
    cp -r ${src_lib_dir}* $lib_dir/
    [ $? -ne 0 ] && echo "cp lib:$src_lib_dir to lib_dir:$lib_dir failed !" && exit 1
done

find $lib_dir -type f -name '*.pyc' -delete

exit 0
