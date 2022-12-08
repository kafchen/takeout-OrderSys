# takeout-OrderSys

## Description

**main.py**: integrated user interface;

**head.gif, head1.gif, tip.gif, tips.gif**: logo picture;

## Overview

Begin Page:

![image](https://user-images.githubusercontent.com/89956877/206331487-56891964-cb2f-4145-82e0-e960461d2928.png)


Registration Page:

![image](https://user-images.githubusercontent.com/89956877/206330876-11cafc7f-2064-4ae8-9aaf-aaba6ce53638.png)

Login Page:

![image](https://user-images.githubusercontent.com/89956877/206330916-0321cf00-e92a-43ac-a989-8a08c599b086.png)

User information Page:

![image](https://user-images.githubusercontent.com/89956877/206330994-834330ae-dd7f-496c-be49-ab628590b484.png)

Seller Page:

![image](https://user-images.githubusercontent.com/89956877/206331298-b6094f16-3295-4103-a935-b38a49d9d0e7.png)

Order-checking Page:

![image](https://user-images.githubusercontent.com/89956877/206331337-7dda3880-63e4-4330-9f4b-4c9b478eb96e.png)

Customer Page:

![image](https://user-images.githubusercontent.com/89956877/206331452-b8e9c148-cbd3-4a30-aed3-8878f0c5f627.png)



Commodity Management Page:

![image](https://user-images.githubusercontent.com/89956877/206331017-3f8b5668-120c-4749-af4c-3992755f1963.png)


Entity Relationship Diagram:

![image](https://user-images.githubusercontent.com/89956877/206330722-5452f482-b092-4667-aa59-7775ba0cf907.png)

SQL Design:

'''
·建立商家表
CREATE TABLE `seller_info` (
  `seller_id` varchar(20) COLLATE utf8_bin NOT NULL,
  `seller_pass` varchar(20) COLLATE utf8_bin NOT NULL,
  `seller_phone` char(11) COLLATE utf8_bin NOT NULL,
  `seller_name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `seller_address` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `seller_gain` int(11) DEFAULT '0',
  PRIMARY KEY (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

·创建客户表
CREATE TABLE `customer_info` (
  `customer_id` varchar(20) COLLATE utf8_bin NOT NULL,
  `customer_pass` varchar(20) COLLATE utf8_bin NOT NULL,
  `customer_phone` char(11) COLLATE utf8_bin NOT NULL,
  `customer_name` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `customer_address` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `customer_budget` int(11) DEFAULT '0',
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

·创建商品表
CREATE TABLE `food` (
  `food_id` varchar(20) COLLATE utf8_bin NOT NULL,
  `seller_id` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `food_name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `food_price` int(11) DEFAULT NULL,
  `food_stock` int(11) DEFAULT NULL,
  `food_type` enum('主食','小吃','饮料') COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`food_id`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `seller_id` FOREIGN KEY (`seller_id`) REFERENCES `seller_info` (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

·创建订单表
CREATE TABLE `order_info` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_time` datetime DEFAULT NULL,
  `customer_id` varchar(20) COLLATE utf8_bin NOT NULL,
  `sellerid` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `food_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `order_tol` int(11) NOT NULL,
  `order_state` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `sellerid` (`sellerid`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer_info` (`customer_id`),
  CONSTRAINT `sellerid` FOREIGN KEY (`sellerid`) REFERENCES `seller_info` (`seller_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COLLATE=utf8_bin

·创建客户浏览商品视图
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_buy` AS
    SELECT 
        `seller_info`.`seller_name` AS `店名`,
        `food`.`food_name` AS `商品`,
        `food`.`food_price` AS `价格`,
        `food`.`food_type` AS `种类`,
        `seller_info`.`seller_id` AS `商店号`
    FROM
        (`food`
        JOIN `seller_info`)
    WHERE
        (`food`.`seller_id` = `seller_info`.`seller_id`)
    ORDER BY `seller_info`.`seller_id`

·创建商家接单视图
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_sell` AS
    SELECT 
        `order_info`.`order_id` AS `订单号`,
        `customer_info`.`customer_name` AS `客户姓名`,
        `customer_info`.`customer_address` AS `客户地址`,
        `customer_info`.`customer_phone` AS `客户电话`,
        `order_info`.`order_tol` AS `订单总额`
    FROM
        ((`seller_info`
        JOIN `customer_info`)
        JOIN `order_info`)
    WHERE
        ((`order_info`.`order_state` = '正在出餐')
            AND (`order_info`.`sellerid` = `seller_info`.`seller_id`)
            AND (`order_info`.`customer_id` = `customer_info`.`customer_id`))
    ORDER BY `order_info`.`order_time` DESC

·创建订单详情视图
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `order_details` AS
    SELECT 
        `order_info`.`order_id` AS `订单编号`,
        `seller_info`.`seller_name` AS `商家名称`,
        `order_info`.`food_name` AS `商品名称`,
        `order_info`.`order_tol` AS `总额`,
        `order_info`.`order_state` AS `订单状态`,
        `order_info`.`customer_id` AS `客户账号`,
        `customer_info`.`customer_name` AS `客户姓名`,
        `customer_info`.`customer_phone` AS `电话`,
        `customer_info`.`customer_address` AS `地址`,
        `order_info`.`order_time` AS `时间`,
        `seller_info`.`seller_id` AS `商家账号`
    FROM
        ((`order_info`
        JOIN `customer_info` ON ((`order_info`.`customer_id` = `customer_info`.`customer_id`)))
        JOIN `seller_info` ON ((`order_info`.`sellerid` = `seller_info`.`seller_id`)))

·创建下订单扣款数据库存储过程
CREATE DEFINER=`root`@`localhost` PROCEDURE `alter_cus_money`(IN user_id VARCHAR(20),IN amount INT)
BEGIN
	update customer_info set customer_budget=amount WHERE customer_id=user_id;
END

·创建完成订单赚钱数据库存储过程
CREATE DEFINER=`root`@`localhost` PROCEDURE `alter_seller_money`(IN user_id VARCHAR(20),IN amount INT)
BEGIN
	update seller_info set seller_gain=amount WHERE seller_id=user_id;
END
'''
