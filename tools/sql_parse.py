import re
from tools.tool import to_camel_case, map_column_type

'''
解析数据库表结构，返回表名和列信息
'''
def parse_table_structure(table_structure, is_camel_case = True):
    # 读取表名
    table_name_match = re.search(r'create table `(\w+)`', table_structure)
    if not table_name_match:
        raise ValueError("表结构中未找到表名")
    
    table_name = table_name_match.group(1)
    columns = []
    
    
    # 定义正则表达式模式
    name_type_pattern = r"`(\w+)`\s+(\w+\(\d+\)|\w+)\s*"
    attribute_pattern = r"((DEFAULT\s+\S+|null|not|auto_increment|unsigned|on|update|\w+\(\d*\))\s+)*"
    comment_pattern = r"(?:\s*comment\s+'([^']+)')*"

    # 匹配列信息
    pattern_str = name_type_pattern + attribute_pattern + comment_pattern
    field_pattern = re.compile(pattern_str, re.IGNORECASE)
    fields = field_pattern.findall(table_structure)
    if not fields:
        raise ValueError("表结构中未找到任何列")
    
    for column_name, column_type, _, _, comment in fields:
        if is_camel_case:
            column_name = to_camel_case(column_name)
        columns.append({'name': column_name, 'type': map_column_type(column_type), 'comment': comment if comment else ''})

    return table_name, columns
