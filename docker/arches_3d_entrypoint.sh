#!/bin/bash

source ${ENTRYPOINT_DIR}/arches_setup_functions.sh

init_custom_db

if [[ "${DJANGO_MODE}" == "PROD" ]] && [[ ! -z ${AZURE_ACCOUNT_NAME} ]] && [[ ! -z ${STATIC_URL} ]]; then
    fix_static_paths
fi

if [[ -z ${GUNICORN_WORKERS} ]]; then
    CPUS=$(grep -c ^processor /proc/cpuinfo)
    echo "CPUS in current system: ${CPUS}"
    export GUNICORN_WORKERS=$((${CPUS}*2+1))
    echo "Setting gunicorn workers to: ${GUNICORN_WORKERS}"
fi

if [[ ! "${DJANGO_DEBUG}" == "True" ]]; then
    compress_static_files
fi