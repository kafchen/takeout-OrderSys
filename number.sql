/*
 Navicat MySQL Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : dmanager

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 16/12/2020 09:49:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for number
-- ----------------------------
DROP TABLE IF EXISTS `number`;
CREATE TABLE `number`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sex` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `age` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `department` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `duty` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `job_title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `major` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `degree` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `employment_time` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of number
-- ----------------------------
INSERT INTO `number` VALUES (1, '张三', '男', '18', '护理部门', '护理', '护师', '护理专业', '大学本科', '2020/10/15-至今', '在职人员');
INSERT INTO `number` VALUES (3, '李四', '女', '19', '药学部门', '药学', '副主任药剂师', '药学专业', '大学本科', '2020/9/13-至今', '在职人员');
INSERT INTO `number` VALUES (4, '王五', '女', '56', '药学部门', '中药学', '主任药剂师', '药学专业', '博士', '1999/4/6-至今', '返聘人员');
INSERT INTO `number` VALUES (5, '胡六', '男', '22', '保安部门', '保安', '保安队长', '无', '初中', '2020/4/5-至今', '临时工');
INSERT INTO `number` VALUES (7, '子钊', '男', '16', '清洁部门', '清洁', '清洁员工', '无', '初中', '2020/6/7-至今', '临时工');
INSERT INTO `number` VALUES (8, '王浩', '男', '22', '清洁部门', '清洁', '清洁员工', '无', '高中', '2020/6/8-至今', '临时工');

SET FOREIGN_KEY_CHECKS = 1;
