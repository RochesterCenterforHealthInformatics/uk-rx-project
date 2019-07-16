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