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

UPDATE rx_prescribed
SET ignore_flag=1
WHERE bnf_code_4 in ('');

SET @current_practice = '';
SET @practice_rank = 0;

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

CREATE TABLE total_rx_by_month AS
SELECT a.*, a.total_items / a.num_practice AS items_per_practice
FROM (SELECT bnf_code_9, SUM(items) AS total_items, COUNT(bnf_code_9) AS num_practice, period
      FROM rx_prescribed
      WHERE ignore_flag = '0'
      GROUP BY bnf_code_9, period) a;

ALTER TABLE `total_rx_by_month`
	ADD INDEX `bnf_code_9` (`bnf_code_9`),
	ADD INDEX `period` (`period`);
