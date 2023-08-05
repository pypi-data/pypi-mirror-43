#!/bin/bash
# pytest-doctests.sh
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details

sbin_dir=$1
bin_dir=$2
src_dir=$3
args=("$@")
if [ "${#args[@]}" -gt 3 ];then
    posargs=(${args[@]:3})
else
    posargs=()
fi

# shellcheck disable=SC2068
if "${bin_dir}"/pytest ${posargs[@]} --collect-only --doctest-modules "${src_dir}" &> /dev/null; then
  "${sbin_dir}"/cprint.sh line cyan "Testing docstrings"
  "${bin_dir}"/pytest ${posargs[@]} --doctest-modules "${src_dir}" || exit 1
fi
