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
