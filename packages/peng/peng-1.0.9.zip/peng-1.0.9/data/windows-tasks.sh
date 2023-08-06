#!/bin/bash
# windows-tasks.sh
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
echo "Performing Windows-specific CI tasks"
sed -r -i -e "s/disable=(.*)/disable=\1,C0103/g" "${EXTRA_DIR}"/.pylintrc
cat "${EXTRA_DIR}"/.pylintrc
