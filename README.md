# mybatis-generate
生成mybatis-plus bean mapper service impl代码

# 配置
package.json配置
- entity_name: 实体类包名
- mapper_name: mapper类包名
- service_name: service类包名
- service_impl_name: service实现类包名
- class_name: 类名

table_sql配置
- 建表语句

jinja_tmplate配置
- bean 实体类模板
- mapper mapper类模板
- service service类模板
- service_impl service实现类模板