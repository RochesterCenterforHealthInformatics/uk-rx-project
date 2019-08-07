def make_values_sql(num):
    values_sql = '('
    for i in range(0, num):
        if i:
            values_sql += ','
        values_sql += '\'{}\''
    values_sql += ')'
    return values_sql


def make_like_condition(values):
    list_sql = '('
    for i, key in enumerate(values):
        if i:
            list_sql += ' OR '
        list_sql += key
    list_sql += ')'
    return list_sql


def make_insert_sql(table_name, fields):
    insert_sql = 'insert into {} ('.format(table_name)
    i = 0
    for key, value in fields.items():
        if i:
            insert_sql += ', '
        insert_sql += key
        i += 1
    insert_sql += ')'
    return insert_sql


def make_values_with_data(fields, data):
    list_sql = '('
    i = 0
    for key, value in fields.items():
        if i:
            list_sql += ', '
        if data[value] == '':
            list_sql += 'NULL'
        else:
            list_sql += '\'{}\''.format(data[value])
        i += 1
    list_sql += ')'
    return list_sql
