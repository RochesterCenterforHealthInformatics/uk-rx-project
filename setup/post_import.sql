SET @a = 0;
CREATE TABLE practice_setting AS
SELECT @a := @a + 1 as id, a.name
FROM (SELECT DISTINCT prescribing_setting AS name FROM practice ORDER BY prescribing_setting) a;

ALTER TABLE practice
    ADD COLUMN practice_setting_id TINYINT NULL DEFAULT NULL AFTER prescribing_setting;

UPDATE practice p, practice_setting ps
SET p.practice_setting_id=ps.id
WHERE ps.name = p.prescribing_setting;

ALTER TABLE `rx_prescribed`
    ADD INDEX `practice` (`practice`),
    ADD INDEX `bnf_code_full` (`bnf_code_full`),
    ADD INDEX `bnf_code_9` (`bnf_code_9`),
    ADD INDEX `bnf_code_4` (`bnf_code_4`),
    ADD INDEX `period` (`period`),
    ADD INDEX `ignore_flag` (`ignore_flag`);

UPDATE rx_prescribed
SET ignore_flag=1
WHERE bnf_code_4 >= 1800;

CREATE TABLE practice_ccg as
SELECT DISTINCT practice, pct_ccg FROM rx_prescribed;

ALTER TABLE `practice_ccg`
	ADD INDEX `practice` (`practice`),
	ADD INDEX `pct_ccg` (`pct_ccg`);

SET @current_practice = '';
SET @practice_rank = 0;

DROP TABLE IF EXISTS top_10_by_practice;
CREATE TABLE top_10_by_practice AS
SELECT practice, bnf_code_9, total_items, practice_rank
FROM (SELECT a.practice,
             a.bnf_code_9,
             a.total_items,
             @practice_rank := IF(@current_practice = a.practice, @practice_rank + 1, 1) AS practice_rank,
             @current_practice := a.practice
      FROM (SELECT rp.practice, rp.bnf_code_9, sum(rp.items) AS total_items
            FROM rx_prescribed rp
            WHERE ignore_flag = '0'
            GROUP BY practice, bnf_code_9) a
      ORDER BY a.practice, a.total_items DESC) ranked
WHERE practice_rank <= 10;

ALTER TABLE `top_10_by_practice`
    ADD INDEX `practice` (`practice`),
    ADD INDEX `bnf_code_9` (`bnf_code_9`);

DROP TABLE IF EXISTS total_rx_by_month;
CREATE TABLE total_rx_by_month AS
SELECT a.*, a.total_items / a.num_practice AS items_per_practice
FROM (SELECT bnf_code_9, SUM(items) AS total_items, COUNT(bnf_code_9) AS num_practice, period
      FROM rx_prescribed
      WHERE ignore_flag = '0'
      GROUP BY bnf_code_9, period) a;

ALTER TABLE `total_rx_by_month`
    ADD INDEX `bnf_code_9` (`bnf_code_9`),
    ADD INDEX `period` (`period`);

# DROP TABLE IF EXISTS total_rx_class_by_month;
# CREATE TABLE total_rx_class_by_month AS
# SELECT a.*, a.total_items / a.num_practice AS items_per_practice
# FROM (SELECT bnf_code_4, SUM(items) AS total_items, COUNT(bnf_code_9) AS num_practice, period
#       FROM rx_prescribed
#       WHERE ignore_flag = '0'
#       GROUP BY bnf_code_4, period) a;
#
# ALTER TABLE `total_rx_class_by_month`
#     ADD INDEX `bnf_code_4` (`bnf_code_4`),
#     ADD INDEX `period` (`period`);

DROP TABLE IF EXISTS total_rx_by_practice_month;
CREATE TABLE total_rx_by_practice_month AS
SELECT practice, SUM(items) AS total_items, period
FROM rx_prescribed
WHERE ignore_flag = '0'
GROUP BY practice, period;

ALTER TABLE `total_rx_by_practice_month`
    ADD INDEX `practice` (`practice`),
    ADD INDEX `total_items` (`total_items`),
    ADD INDEX `period` (`period`);

DROP TABLE IF EXISTS rx_by_practice_2017;
CREATE TABLE rx_by_practice_2017 AS
SELECT practice, bnf_code_9, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201701 AND period <= 201712)
  and ignore_flag = '0'
GROUP BY practice, bnf_code_9;

DROP TABLE IF EXISTS rx_by_practice_2018;
CREATE TABLE rx_by_practice_2018 AS
SELECT practice, bnf_code_9, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201801 AND period <= 201812)
  and ignore_flag = '0'
GROUP BY practice, bnf_code_9;

DROP TABLE IF EXISTS rx_by_practice_combined;
CREATE TABLE rx_by_practice_combined AS
SELECT practice, bnf_code_9, SUM(items) AS total_items
FROM rx_prescribed
WHERE ignore_flag = '0'
GROUP BY practice, bnf_code_9;

DROP TABLE IF EXISTS rx_by_class_by_practice_2018;
CREATE TABLE rx_by_class_by_practice_2018 AS
SELECT practice, bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201801 AND period <= 201812)
  AND ignore_flag = 0
GROUP BY practice, bnf_code_4;

DROP TABLE IF EXISTS rx_by_class_by_practice_2017;
CREATE TABLE rx_by_class_by_practice_2017 AS
SELECT practice, bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201701 AND period <= 201712)
  AND ignore_flag = 0
GROUP BY practice, bnf_code_4;

DROP TABLE IF EXISTS rx_by_class_by_practice_combined;
CREATE TABLE rx_by_class_by_practice_combined AS
SELECT practice, bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE ignore_flag = 0
GROUP BY practice, bnf_code_4;

DROP TABLE IF EXISTS drug_class_2018;
CREATE TABLE drug_class_2018 AS
SELECT bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201801 AND period <= 201812)
  AND ignore_flag = 0
GROUP BY bnf_code_4;

DROP TABLE IF EXISTS drug_class_2017;
CREATE TABLE drug_class_2017 AS
SELECT bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE (period >= 201701 AND period <= 201712)
  AND ignore_flag = 0
GROUP BY bnf_code_4;

DROP TABLE IF EXISTS drug_class_combined;
CREATE TABLE drug_class_combined AS
SELECT bnf_code_4, SUM(items) AS total_items
FROM rx_prescribed
WHERE ignore_flag = 0
GROUP BY bnf_code_4;
