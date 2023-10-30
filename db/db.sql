-- MySQL Script generated by MySQL Workbench
-- Sun Jul 10 07:14:35 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema xrzqx
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema xrzqx
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `xrzqx` DEFAULT CHARACTER SET utf8 ;
USE `xrzqx` ;

-- -----------------------------------------------------
-- Table `xrzqx`.`history`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `xrzqx`.`history` ;

CREATE TABLE IF NOT EXISTS `xrzqx`.`history` (
  `idhistory` INT NOT NULL AUTO_INCREMENT,
  `nomor` VARCHAR(45) NULL,
  `waktu_masuk` VARCHAR(45) NULL,
  `waktu_keluar` VARCHAR(45) NULL,
  `img_emb` JSON NULL,
  PRIMARY KEY (`idhistory`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
