#!/bin/bash -x

cur_dir=$(dirname $0)
cur_dir=$(cd ${cur_dir}; pwd)
home_dir="$cur_dir/.."
tmp_dir='app'

rm -rf $tmp_dir
mkdir $tmp_dir

version=$(ls $home_dir/dist/aws-cicd-*.tar.gz| egrep -o 'aws-cicd-([0-9]+\.){2}[0-9]+' | cut -d '-' -f3)

cp $home_dir/dist/aws-cicd-*.tar.gz $tmp_dir/

cd $tmp_dir
tar xvf aws-cicd-*.tar.gz
rm aws-cicd-*.tar.gz
ln -s aws-cicd-* aws-cicd
cd -

docker build -t aws-cicd:$version -t aws-cicd:latest .
