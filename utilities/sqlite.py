import sqlite3

connection = None

def query(query, args=()):
    connection = _get_connection()
    result_object = connection.execute(query, args)
    columns = _get_columns(result_object.description)
    results = []
    for row in result_object.fetchall():
        result = []
        for column_index, value in enumerate(row):
            column = columns[column_index]
            result.append({column: value})
        results.append(result)
    return results

def _get_connection():
    global connection
    if connection is None:
        return sqlite3.connect('rsvp.db')

def _get_columns(description):
    columns = []
    if not description:
        return columns
    for item in description:
        column_name = item[0]
        columns.append(column_name)
    return columns

def return_row(query, args=()):
    results = query(query, args)
    if not results:
        return []
    return results[0]
