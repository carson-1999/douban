SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for douban
-- ----------------------------
DROP TABLE IF EXISTS `douban`;
CREATE TABLE `douban`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(50) COMMENT 'name',
  `author` varchar(50) COMMENT 'author',
  `publisher` varchar(50) COMMENT 'publisher',
  `publish_year` varchar(50) COMMENT 'publish_year',
  `pages` varchar(50) COMMENT 'pages',
  `price` varchar(50) COMMENT 'price',
  `binding` varchar(50) COMMENT 'binding',
  `series` varchar(50) COMMENT 'series',
  `ISBN` varchar(50) COMMENT 'ISBN',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'douban Top250' ROW_FORMAT = COMPACT;



