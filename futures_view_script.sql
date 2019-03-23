CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `futures_view` AS
    SELECT 
        `gc`.`datadate` AS `datadate`,
        `gc`.`CME_GC1` AS `cme_gc1`,
        `gc`.`CME_GC2` AS `cme_gc2`,
        `gc`.`CME_GC3` AS `cme_gc3`,
        `gc`.`CME_GC4` AS `cme_gc4`,
        `cl`.`CME_CL1` AS `cme_cl1`,
        `cl`.`CME_CL2` AS `cme_cl2`,
        `cl`.`CME_CL3` AS `cme_cl3`,
        `cl`.`CME_CL4` AS `cme_cl4`,
        `ng`.`CME_NG1` AS `cme_ng1`,
        `ng`.`CME_NG2` AS `cme_ng2`,
        `ng`.`CME_NG3` AS `cme_ng3`,
        `ng`.`CME_NG4` AS `cme_ng4`,
        `es`.`CME_ES1` AS `cme_es1`,
        `es`.`CME_ES2` AS `cme_es2`,
        `es`.`CME_ES3` AS `cme_es3`,
        `es`.`CME_ES4` AS `cme_es4`,
        `nq`.`CME_NQ1` AS `cme_nq1`,
        `nq`.`CME_NQ2` AS `cme_nq2`
    FROM
        ((((`cme_gc` `gc`
        LEFT JOIN `cme_cl` `cl` ON ((`gc`.`datadate` = `cl`.`datadate`)))
        LEFT JOIN `cme_ng` `ng` ON ((`cl`.`datadate` = `ng`.`datadate`)))
        LEFT JOIN `cme_es` `es` ON ((`ng`.`datadate` = `es`.`datadate`)))
        LEFT JOIN `cme_nq` `nq` ON ((`es`.`datadate` = `nq`.`datadate`)))