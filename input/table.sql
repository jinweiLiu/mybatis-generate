CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) DEFAULT NULL COMMENT '用户密码',
  `email` varchar(255)   COMMENT '邮件' DEFAULT '' ,
  `created_at` datetime DEFAULT CURRENT_TIME() COMMENT '创建时间',
  PRIMARY KEY (`id`)
)