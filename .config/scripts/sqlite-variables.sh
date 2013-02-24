# Options to adjust

sqlite_dir="../sqlite"
if_root_switch_to_user="www-data"
sqlite_bin=""

set_sqlite_bin_path () {
	if which sqlite; then
		sqlite_bin=`which sqlite`
		return
	fi

	if which sqlite3; then
		sqlite_bin=`which sqlite3`
		return
	fi

	if which sqlite2; then
		sqlite_bin=`which sqlite2`
		return
	fi
}

set_sqlite_bin_path
