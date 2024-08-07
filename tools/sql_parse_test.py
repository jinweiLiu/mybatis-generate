import re

sql = """
CREATE TABLE `user` ( 
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID', 
  `username` varchar(255) NOT NULL COMMENT '用户名' default '',
  `password` varchar(255) DEFAULT NULL COMMENT  '用户密码',
  `email` varchar(255) DEFAULT 'ddd'  COMMENT '邮件',
  `phone` char(32)  DEFAULT '',
  `created_at` datetime not null  default current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`)
);
"""

# 定义正则表达式模式
pattern_str = r"`(\w+)`\s+(\w+\(\d+\)|\w+)\s*((DEFAULT\s+\S+|null|not\s+null|default\s+null|auto_increment|unsigned)\s+)*(?:\s*comment\s+'([^']+)')*"

# 使用正则表达式查找匹配项
field_pattern = re.compile(pattern_str, re.IGNORECASE)
matches = field_pattern.findall(sql)

# 打印提取的信息
fields = [{'name': match[0], 'type': match[1], 'comment': match[4] if match[4] else ''} for match in matches]

for field in fields:
    print(field)
