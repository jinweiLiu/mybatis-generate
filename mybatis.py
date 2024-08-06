import re
import json
from jinja2 import Template

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
    
    column_matches = re.findall(r'`(\w+)`\s+(\w+)', table_structure)
    if not column_matches:
        raise ValueError("表结构中未找到任何列")
    
    for column_name, column_type in column_matches:
        if is_camel_case:
            column_name = to_camel_case(column_name)
        columns.append({'name': column_name, 'type': map_column_type(column_type)})

    return table_name, columns

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
    if 'int' in mysql_type:
        return 'Integer'
    elif 'varchar' in mysql_type or 'text' in mysql_type:
        return 'String'
    elif 'datetime' in mysql_type:
        return 'Date'
    elif 'double' in mysql_type or 'float' in mysql_type:
        return 'Double'
    elif 'tinyint' in mysql_type:
        return 'Integer'
    elif 'bigint' in mysql_type:
        return 'Long'
    # 添加其他类型映射
    else:
        return 'String'

'''
生成代码
'''
def generate_code(table_structure, package_name):
    table_name, columns = parse_table_structure(table_structure)
    
    default_class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    class_name = default_class_name if package_name.get('class_name') is None else package_name.get('class_name')
    entity_name = package_name.get('entity_name')
    mapper_name = package_name.get('mapper_name')
    service_name = package_name.get('service_name')
    service_impl_name = package_name.get('service_impl_name')
    
    bean_template, mapper_template, service_template, service_impl_template = template_read()

    bean_code = Template(bean_template).render(entity_name=entity_name, class_name=class_name, columns=columns)
    mapper_code = Template(mapper_template).render(mapper_name=mapper_name, entity_name=entity_name, class_name=class_name)
    service_code = Template(service_template).render(service_name=service_name, entity_name=entity_name, class_name=class_name)
    service_impl_code = Template(service_impl_template).render(service_impl_name=service_impl_name, entity_name=entity_name, 
                                                               mapper_name=mapper_name, service_name=service_name, class_name=class_name)

    with open(f"{class_name}.java", 'w') as f:
        print(f"Generated code for {class_name}:")
        f.write(bean_code)

    with open(f"{class_name}Mapper.java", 'w') as f:
        print(f"Generated code for {class_name}Mapper:")
        f.write(mapper_code)

    with open(f"{class_name}Service.java", 'w') as f:
        print(f"Generated code for {class_name}Service:")
        f.write(service_code)

    with open(f"{class_name}ServiceImpl.java", 'w') as f:
        print(f"Generated code for {class_name}ServiceImpl:")
        f.write(service_impl_code)
        
'''
从模板文件夹中读取所有模板
'''    
def template_read():
    bean_template = None
    mapper_template = None
    service_template = None
    service_impl_template = None
    
    with open('jinja_template/bean.jinja', 'r') as f:
        bean_template = f.read()
        
    with open('jinja_template/mapper.jinja', 'r') as f:
        mapper_template = f.read()
        
    with open('jinja_template/service.jinja', 'r') as f:
        service_template = f.read()
        
    with open('jinja_template/service_impl.jinja', 'r') as f:
        service_impl_template = f.read()
    
    return bean_template, mapper_template, service_template, service_impl_template

if __name__ == "__main__":
    # 读取表结构
    with open('input/table.sql', 'r') as f:
        table_structure = f.read()
    table_structure = table_structure.lower()
    
    # 读取包名配置
    with open('input/package.json', 'r') as f:
        data = json.load(f)
    
    # 生成代码
    generate_code(table_structure, data)
