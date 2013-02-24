#!/usr/bin/env bash

# Version 0.2.0
#
# Creates SQLite database and loads schema if it does not already exist.

this_file=`basename "$0"`
this_dir=`dirname "$0"`
cd "$this_dir"

source sqlite-variables.sh
sqlite_filename=`cat "${sqlite_dir}/filename"`
sqlite_filepath="../../${sqlite_filename}"
sqlite_data_file="${sqlite_dir}/data.sql"
sqlite_schema="${sqlite_dir}/schema.sql"
user=""

set -o nounset
set -o errtrace
set -o errexit
set -o pipefail

log () {
	printf "$*\n"
}

error () {
	log "ERROR: " "$*\n"
	exit 1
}

help () {
	echo "Usage is './${this_file}'"
}

# Application functions

switch_user () {
	if [[ $EUID -eq 0 ]]; then
		user="$if_root_switch_to_user"
	else
		user=`id -u -n`
	fi
}

load_data_if_exists () {
	if [[ -f "$sqlite_data_file" ]]; then
		$sqlite_bin "$sqlite_filepath" < "$sqlite_data_file"
	fi
}

load_schema () {
	$sqlite_bin "$sqlite_filepath" < "$sqlite_schema"
}

switch_user
load_data_if_exists
load_schema
