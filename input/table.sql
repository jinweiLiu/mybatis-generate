CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) DEFAULT NULL COMMENT '用户密码',
  `email` varchar(255)  DEFAULT '' COMMENT '邮件' ,
  `created_at` datetime DEFAULT '',
  PRIMARY KEY (`id`)
)