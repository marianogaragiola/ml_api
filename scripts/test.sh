#!/bin/bash

coverage run --source="src/thermal_settings_api" -m pytest
coverage html

while getopts oh opt; do
    case $opt in
        o) xdg-open ./htmlcov/index.html ;;
        h) echo "Use -o to open the test results in a browser" ;;
    esac
done

