FROM globaldigitalheritage/arches:4.3.5.1

ENV APP_DIR=${WEB_ROOT}/arches_3d/arches_3d
ENV YARN_DIR=${APP_DIR}
ENV ENTRYPOINT_DIR=/docker/entrypoint
ENV CICD_DIR=/ci-cd

COPY ./arches_3d/arches_3d/install/requirements.txt ${APP_DIR}/install/requirements.txt
RUN	. ${WEB_ROOT}/ENV/bin/activate &&\
	pip install -r ${APP_DIR}/install/requirements.txt

COPY ./arches_3d/arches_3d/package.json ${APP_DIR}/package.json
WORKDIR ${YARN_DIR}
RUN yarn install

COPY ./ci-cd/refresh_concepts_collections.sh ${CICD_DIR}/refresh_concepts_collections.sh
COPY ./docker/arches_3d_entrypoint.sh ${ENTRYPOINT_DIR}/arches_3d_entrypoint.sh
COPY ./docker/arches_setup_functions.sh ${ENTRYPOINT_DIR}/arches_setup_functions.sh
RUN chmod -R 700 ${ENTRYPOINT_DIR} ${CICD_DIR} &&\
    dos2unix ${ENTRYPOINT_DIR}/* ${CICD_DIR}/*

COPY ./arches_3d ${WEB_ROOT}/arches_3d



# Set default workdir
WORKDIR ${WEB_ROOT}/arches_3d