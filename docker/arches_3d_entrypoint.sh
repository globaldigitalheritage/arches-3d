#!/bin/bash

source ${ENTRYPOINT_DIR}/arches_setup_functions.sh

init_custom_db

if [[ "${DJANGO_MODE}" == "PROD" ]] && [[ ! -z ${AZURE_ACCOUNT_NAME} ]] && [[ ! -z ${STATIC_URL} ]]; then
    fix_static_paths
fi

if [[ ! -z ${CPUS} ]] && [[ -z ${GUNICORN_WORKERS} ]]; then
    export GUNICORN_WORKERS=${CPUS}*2+1
    echo "Setting gunicorn workers to: ${GUNICORN_WORKERS}"
fi