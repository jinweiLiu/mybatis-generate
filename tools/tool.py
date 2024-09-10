'''
将下划线分隔的字符串转换为驼峰形式
'''
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

'''
mysql类型映射为java类型
'''
def map_column_type(mysql_type):
    if 'bigint' in mysql_type:
        return 'Long'
    elif 'tinyint' in mysql_type:
        return 'Integer'
    elif 'varchar' in mysql_type or 'text' in mysql_type:
        return 'String'
    elif 'datetime' in mysql_type:
        return 'Date'
    elif 'double' in mysql_type or 'float' in mysql_type:
        return 'Double'
    elif 'int' in mysql_type:
        return 'Integer'
    # 添加其他类型映射
    else:
        return 'String'

'''
判断字符串是否为空
'''
def notBlank(string):
    return bool(string and string.strip())

'''
判断字符串是否为空
'''
def isBlank(string):
    return not notBlank(string)