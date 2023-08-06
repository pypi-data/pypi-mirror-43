#!/bin/bash
# pytest-rst.sh
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
if "${bin_dir}"/pytest ${posargs[@]} --collect-only --doctest-glob="*.rst" "${src_dir}" &> /dev/null; then
  "${sbin_dir}"/cprint.sh line cyan "Testing reStructuredText files"
  "${bin_dir}"/pytest ${posargs[@]} --doctest-glob="*.rst" "${src_dir}" || exit 1
fi
