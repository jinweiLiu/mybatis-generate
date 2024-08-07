import re

sql = """
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) DEFAULT NULL COMMENT '用户密码',
  `email` varchar(255)   COMMENT '邮件' DEFAULT '' ,
  `created_at` datetime DEFAULT CURRENT_TIME() COMMENT '创建时间',
  PRIMARY KEY (`id`)
)
"""

# 定义正则表达式模式
name_type_pattern = r"`(\w+)`\s+(\w+\(\d+\)|\w+)\s*"
attribute_pattern = r"((DEFAULT\s+\S+|null|not|auto_increment|unsigned|on|update|\w+\(\d*\))\s+)*"
comment_pattern = r"(?:\s*comment\s+'([^']+)')*"

pattern_str = name_type_pattern + attribute_pattern + comment_pattern

# 使用正则表达式查找匹配项
field_pattern = re.compile(pattern_str, re.IGNORECASE)
matches = field_pattern.findall(sql)

# 打印提取的信息
fields = [{'name': match[0], 'type': match[1], 'comment': match[4] if match[4] else ''} for match in matches]

for field in fields:
    print(field)
