#!/bin/bash

_MAIN_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_THIS_PATH="$(pwd)"

_MAIN_NAME="main"
_MAIN_FILE="${_MAIN_NAME}.py"

_MODULE_PATH="${_THIS_PATH#${_MAIN_PATH}/}"
_MODULE_NAME="${_MODULE_PATH//\//.}.${_MAIN_NAME}"

_MAKE () { PYTHONPATH="${_MAIN_PATH}" poetry run python -m "${_MODULE_NAME}" ; }

_MAKE
while inotifywait "${_THIS_PATH}/${_MAIN_FILE}"
do
    _MAKE
done
