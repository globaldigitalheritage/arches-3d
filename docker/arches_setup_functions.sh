#!/bin/bash


APP_FOLDER=${WEB_ROOT}/${ARCHES_PROJECT}
THESAURI_FOLDER=${APP_FOLDER}/arches_3d/db/schemes/thesauri
COLLECTIONS_FOLDER=${APP_FOLDER}/arches_3d/db/schemes/collections


cd_app_folder() {
	cd ${APP_FOLDER}
	echo "Current work directory: ${APP_FOLDER}"
}


init_custom_db() {
	
	cd_app_folder

	# Import graphs
	if ! graphs_exist; then
		import_graphs
	else
		echo "Graphs already exist in the database. Skipping..."
	fi
	
	# Import concepts
	if ! concepts_exist; then
		import_concepts
	else
		echo "Concepts already exist in the database. Skipping..."
	fi
	
	# Import collections
	if ! collections_exist; then
		import_collections
	else
		echo "Collections already exist in the database. Skipping..."
	fi

	# Register widgets
	register_widgets
}

graphs_exist() {
	row_count=$(psql --host=${PGHOST} --port=${PGPORT} --user=${PGUSERNAME} --dbname=${PGDBNAME} -Atc "SELECT COUNT(*) FROM public.graphs")
	if [[ ${row_count} -le 3 ]]; then
		return 1
	else 
		return 0
	fi
}

concepts_exist() {
	row_count=$(psql --host=${PGHOST} --port=${PGPORT} --user=${PGUSERNAME} --dbname=${PGDBNAME} -Atc "SELECT COUNT(*) FROM public.concepts WHERE nodetype = 'Concept'")
	if [[ ${row_count} -le 2 ]]; then
		return 1
	else 
		return 0
	fi
}

collections_exist() {
	row_count=$(psql --host=${PGHOST} --port=${PGPORT} --user=${PGUSERNAME} --dbname=${PGDBNAME} -Atc "SELECT COUNT(*) FROM public.concepts WHERE nodetype = 'Collection'")
	if [[ ${row_count} -le 1 ]]; then
		return 1
	else 
		return 0
	fi
}

import_graphs() {
	echo "Running: python manage.py packages -o import_graphs"
	python manage.py packages -o import_graphs
}

import_concepts() {
	echo "Importing all concepts in ${THESAURI_FOLDER}"
	for file_path in ${THESAURI_FOLDER}/*.rdf; do
		import_reference_data ${file_path}
	done
}

import_collections() {
	echo "Importing all collections in ${COLLECTIONS_FOLDER}"
	for file_path in ${COLLECTIONS_FOLDER}/*.rdf; do
		import_reference_data ${file_path}
	done	
}

import_reference_data() {
	# Import example concept schemes
	local rdf_file="$1"
	echo "Running: python manage.py packages -o import_reference_data -s \"${rdf_file}\""
	python manage.py packages -o import_reference_data -s "${rdf_file}"
}

fix_static_paths() {
    echo "Running: python manage.py storage fix_static_paths"
    python manage.py storage fix_static_paths
}

compress_static_files() {
	echo "Running: python manage.py compress"
	python manage.py compress
}

register_widgets() {
	register_uri_widget
}

register_uri_widget() {
	if ! widget_exist "uri-widget"; then
		echo "Running: python manage.py widget register --source arches_3d/widgets/uri.json"
		python manage.py widget register --source arches_3d/widgets/uri.json
	else
		echo "Widget 'uri-widget' already exists, skipping..."
	fi
}

widget_exist() {
	local widget_name="$1"
	row_count=$(psql --host=${PGHOST} --port=${PGPORT} --user=${PGUSERNAME} --dbname=${PGDBNAME} -Atc "SELECT COUNT(*) FROM public.widgets WHERE name = '${widget_name}'")
	if [[ ${row_count} -eq 1 ]]; then
		return 0
	else 
		return 1
	fi
}