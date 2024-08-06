import re
import json
import os
from jinja2 import Template
from tools.parse import to_camel_case, map_column_type, isBlank, notBlank

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
        columns.append({'name': column[0], 'type': map_column_type(column[1]), 'comment': comment or ''})

    return table_name, columns

'''
生成代码
'''
def generate_code(table_structure, config_data):
    table_name, columns = parse_table_structure(table_structure)
    # 读取类名、包名配置
    class_name, entity_name, mapper_name, service_name, service_impl_name = name_read(table_name, config_data)
    
    # 读取模板文件夹中的所有模板并渲染
    codeContent = template_read(class_name, columns, entity_name, mapper_name, service_name, service_impl_name)

    # 检查输出目录是否存在，如果不存在则创建
    output_dir = str(config_data.get('output_dir'))
    print("代码输出目录：", output_dir)
    if notBlank(output_dir) :
        if not os.path.exists(output_dir):
            print("输出目录不存在，正在创建...")
            os.makedirs(output_dir)
            
    # 将生成的代码写入文件
    code_list = ["{class_name}.java", "{class_name}Mapper.java", "{class_name}Service.java", "{class_name}ServiceImpl.java"]
    for code, content in zip(code_list, codeContent):
        file_path = code.format(class_name=class_name)
        if notBlank(output_dir):
            file_path = os.path.join(output_dir, file_path)
        with open(file_path, 'w') as f:
            f.write(content)
 
'''
从配置文件中读取类名、包名等信息
'''    
def name_read(table_name, package_name):
    default_class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    class_name = default_class_name if isBlank(package_name.get('class_name')) else package_name.get('class_name')
    entity_name = package_name.get('entity_name')
    mapper_name = package_name.get('mapper_name')
    service_name = package_name.get('service_name')
    service_impl_name = package_name.get('service_impl_name')
    
    return class_name, entity_name, mapper_name, service_name, service_impl_name
   
'''
从模板文件夹中读取所有模板
'''    
def template_read(class_name, columns, entity_name, mapper_name, service_name, service_impl_name):
    jinja_files = ['bean.jinja', 'mapper.jinja', 'service.jinja', 'service_impl.jinja']
    templates = []
    for jinja_file in jinja_files:
        with open(f'jinja_template/{jinja_file}', 'r') as f:
            content = f.read()
            templates.append(content)
        
    bean_code = Template(templates[0]).render(entity_name=entity_name, class_name=class_name, columns=columns)
    mapper_code = Template(templates[1]).render(mapper_name=mapper_name, entity_name=entity_name, class_name=class_name)
    service_code = Template(templates[2]).render(service_name=service_name, entity_name=entity_name, class_name=class_name)
    service_impl_code = Template(templates[3]).render(service_impl_name=service_impl_name, entity_name=entity_name, 
                                                               mapper_name=mapper_name, service_name=service_name, class_name=class_name)
    
    return [bean_code, mapper_code, service_code, service_impl_code]

if __name__ == "__main__":
    # 读取表结构
    with open('input/table.sql', 'r') as f:
        table_structure = f.read()
    table_structure = table_structure.lower()
    
    # 读取包名配置
    with open('input/package.json', 'r') as f:
        config_data = json.load(f)
    
    # 生成代码
    generate_code(table_structure, config_data)
