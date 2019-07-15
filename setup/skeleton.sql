-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.26-0ubuntu0.18.04.1 - (Ubuntu)
-- Server OS:                    Linux
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table uk-data.bnf_chapter
DROP TABLE IF EXISTS `bnf_chapter`;
CREATE TABLE IF NOT EXISTS `bnf_chapter` (
  `bnf_code_2` varchar(2) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  KEY `bnf_code_2` (`bnf_code_2`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table uk-data.bnf_code_9
DROP TABLE IF EXISTS `bnf_code_9`;
CREATE TABLE IF NOT EXISTS `bnf_code_9` (
  `bnf_code_9` varchar(16) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  KEY `bnf_code_9` (`bnf_code_9`),
  KEY `name_short` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table uk-data.bnf_code_full
DROP TABLE IF EXISTS `bnf_code_full`;
CREATE TABLE IF NOT EXISTS `bnf_code_full` (
  `bnf_code` varchar(16) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  KEY `bnf_code` (`bnf_code`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table uk-data.bnf_section
DROP TABLE IF EXISTS `bnf_section`;
CREATE TABLE IF NOT EXISTS `bnf_section` (
  `bnf_code_4` varchar(4) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  KEY `bnf_code_4` (`bnf_code_4`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table uk-data.practice
DROP TABLE IF EXISTS `practice`;
CREATE TABLE IF NOT EXISTS `practice` (
  `org_code` varchar(8) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `nat_group` char(3) DEFAULT NULL,
  `hlhg` char(3) DEFAULT NULL,
  `addr_1` varchar(100) DEFAULT NULL,
  `addr_2` varchar(100) DEFAULT NULL,
  `addr_3` varchar(100) DEFAULT NULL,
  `addr_4` varchar(100) DEFAULT NULL,
  `addr_5` varchar(100) DEFAULT NULL,
  `post_code` varchar(10) DEFAULT NULL,
  `open_date` varchar(50) DEFAULT NULL,
  `close_date` varchar(50) DEFAULT NULL,
  `status_code` char(1) DEFAULT NULL,
  `prescribing_setting` varchar(50) DEFAULT NULL,
  `num_practitioners` tinyint(3) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table uk-data.rx_prescribed
DROP TABLE IF EXISTS `rx_prescribed`;
CREATE TABLE IF NOT EXISTS `rx_prescribed` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sha_at` varchar(3) DEFAULT NULL,
  `pct_ccg` varchar(3) DEFAULT NULL,
  `practice` varchar(8) DEFAULT NULL,
  `bnf_code_full` varchar(16) DEFAULT NULL,
  `bnf_code_9` varchar(9) DEFAULT NULL,
  `bnf_code_4` varchar(4) DEFAULT NULL,
  `items` smallint(6) unsigned DEFAULT NULL,
  `nic` float unsigned DEFAULT NULL,
  `cost` float unsigned DEFAULT NULL,
  `quantity` mediumint(9) unsigned DEFAULT NULL,
  `period` mediumint(9) unsigned DEFAULT NULL,
  `ignore_flag` tinyint(3) unsigned DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39125464 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
