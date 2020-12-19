-- phpMyAdmin SQL Dump
-- version 4.6.6deb5ubuntu0.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 18, 2020 at 03:49 PM
-- Server version: 5.7.32-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rdi_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `elements_rdi`
--

CREATE TABLE `elements_rdi` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Calcium (mg/d)` text COLLATE utf8mb4_bin,
  `Chromium (ug/d)` text COLLATE utf8mb4_bin,
  `Copper (ug/d)` text COLLATE utf8mb4_bin,
  `Fluoride (mg/d)` text COLLATE utf8mb4_bin,
  `Iodine (ug/d)` text COLLATE utf8mb4_bin,
  `Iron (mg/d)` text COLLATE utf8mb4_bin,
  `Magnesium (mg/d)` text COLLATE utf8mb4_bin,
  `Manganese (mg/d)` text COLLATE utf8mb4_bin,
  `Molybdenum (ug/d)` text COLLATE utf8mb4_bin,
  `Phosphorus (mg/d)` text COLLATE utf8mb4_bin,
  `Selenium (ug/d)` text COLLATE utf8mb4_bin,
  `Zinc (mg/d)` text COLLATE utf8mb4_bin,
  `Potassium (mg/d)` text COLLATE utf8mb4_bin,
  `Sodium (mg/d)` text COLLATE utf8mb4_bin,
  `Chloride (g/d)` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `elements_rdi`
--

INSERT INTO `elements_rdi` (`Life-Stage Group`, `Calcium (mg/d)`, `Chromium (ug/d)`, `Copper (ug/d)`, `Fluoride (mg/d)`, `Iodine (ug/d)`, `Iron (mg/d)`, `Magnesium (mg/d)`, `Manganese (mg/d)`, `Molybdenum (ug/d)`, `Phosphorus (mg/d)`, `Selenium (ug/d)`, `Zinc (mg/d)`, `Potassium (mg/d)`, `Sodium (mg/d)`, `Chloride (g/d)`) VALUES
('Infants', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('< 6 mo', '200', '0.2', '200', '0.01', '110', '0.27', '30', '0.003', '2', '100', '15', '2', '400', '110', '0.18'),
('< 12 mo', '260', '5.5', '220', '0.5', '130', '11', '75', '0.6', '3', '275', '20', '3', '860', '370', '0.57'),
('Children', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('1 to 3 y', '700', '11', '340', '0.7', '90', '7', '80', '1.2', '17', '460', '20', '3', '2000', '800', '1.5'),
('4 to 8 y', '1000', '15', '440', '1', '90', '10', '130', '1.5', '22', '500', '30', '5', '2300', '1000', '1.9'),
('Males', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', '1300', '25', '700', '2', '120', '8', '240', '1.9', '34', '1250', '40', '8', '2500', '1200', '2.3'),
('14 to 18 y', '1300', '35', '890', '3', '150', '11', '410', '2.2', '43', '1250', '55', '11', '3000', '1500', '2.3'),
('19 to 30 y', '1000', '35', '900', '4', '150', '8', '400', '2.3', '45', '700', '55', '11', '3400', '1500', '2.3'),
('31 to 50 y', '1000', '35', '900', '4', '150', '8', '420', '2.3', '45', '700', '55', '11', '3400', '1500', '2.3'),
('51 to 70', '1000', '30', '900', '4', '150', '8', '420', '2.3', '45', '700', '55', '11', '3400', '1500', '2.0'),
('> 70 y', '1200', '30', '900', '4', '150', '8', '420', '2.3', '45', '700', '55', '11', '3400', '1500', '1.8'),
('Females', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', '1300', '21', '700', '2', '120', '8', '240', '1.6', '34', '1250', '40', '8', '2300', '1200', '2.3'),
('14 to 18 y', '1300', '24', '890', '3', '150', '15', '360', '1.6', '43', '1250', '55', '9', '2300', '1500', '2.3'),
('19 to 30 y', '1000', '25', '900', '3', '150', '18', '310', '1.8', '45', '700', '55', '8', '2600', '1500', '2.3'),
('31 to 50 y', '1000', '25', '900', '3', '150', '18', '320', '1.8', '45', '700', '55', '8', '2600', '1500', '2.3'),
('51 to 70 y', '1200', '20', '900', '3', '150', '8', '320', '1.8', '45', '700', '55', '8', '2600', '1500', '2.0'),
('> 70 y', '1200', '20', '900', '3', '150', '8', '320', '1.8', '45', '700', '55', '8', '2600', '1500', '1.8'),
('Pregnancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', '1300', '29', '1000', '3', '220', '27', '400', '2.0', '50', '1250', '60', '12', '2600', '1500', '2.3'),
('19 to 30 y', '1000', '30', '1000', '3', '220', '27', '350', '2.0', '50', '700', '60', '11', '2900', '1500', '2.3'),
('31 to 50 y', '1000', '30', '1000', '3', '220', '27', '360', '2.0', '50', '700', '60', '11', '2900', '1500', '2.3'),
('Lacation', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', '1300', '44', '1300', '3', '290', '10', '360', '2.6', '50', '1250', '70', '13', '2500', '1500', '2.3'),
('19 to 30 y', '1000', '45', '1300', '3', '290', '9', '310', '2.6', '50', '700', '70', '12', '2800', '1500', '2.3'),
('31 to 50 y', '1000', '45', '1300', '3', '290', '9', '320', '2.6', '50', '700', '70', '12', '2800', '1500', '2.3');

-- --------------------------------------------------------

--
-- Table structure for table `elements_upper_rdi`
--

CREATE TABLE `elements_upper_rdi` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Arsenic` text COLLATE utf8mb4_bin,
  `Boron (mg/d)` text COLLATE utf8mb4_bin,
  `Calcium (mg/d)` text COLLATE utf8mb4_bin,
  `Chromium` text COLLATE utf8mb4_bin,
  `Copper (ug/d)` text COLLATE utf8mb4_bin,
  `Fluoride (mg/d)` text COLLATE utf8mb4_bin,
  `Iodine (ug/d)` text COLLATE utf8mb4_bin,
  `Iron (mg/d)` text COLLATE utf8mb4_bin,
  `Magnesium (mg/d)` text COLLATE utf8mb4_bin,
  `Manganese (mg/d)` text COLLATE utf8mb4_bin,
  `Molybdenum (ug/d)` text COLLATE utf8mb4_bin,
  `Nickel (mg/d)` text COLLATE utf8mb4_bin,
  `Phosphorus (g/d)` text COLLATE utf8mb4_bin,
  `Potassium` text COLLATE utf8mb4_bin,
  `Selenium (ug/d)` text COLLATE utf8mb4_bin,
  `Silicon` text COLLATE utf8mb4_bin,
  `Sulfate` text COLLATE utf8mb4_bin,
  `Vanadium (mg/d)` text COLLATE utf8mb4_bin,
  `Zinc (mg/d)` text COLLATE utf8mb4_bin,
  `Sodium` text COLLATE utf8mb4_bin,
  `Chloride (g/d)` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `elements_upper_rdi`
--

INSERT INTO `elements_upper_rdi` (`Life-Stage Group`, `Arsenic`, `Boron (mg/d)`, `Calcium (mg/d)`, `Chromium`, `Copper (ug/d)`, `Fluoride (mg/d)`, `Iodine (ug/d)`, `Iron (mg/d)`, `Magnesium (mg/d)`, `Manganese (mg/d)`, `Molybdenum (ug/d)`, `Nickel (mg/d)`, `Phosphorus (g/d)`, `Potassium`, `Selenium (ug/d)`, `Silicon`, `Sulfate`, `Vanadium (mg/d)`, `Zinc (mg/d)`, `Sodium`, `Chloride (g/d)`) VALUES
('Infants', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('< 6 mo', 'ND', 'ND', '1000', 'ND', 'ND', '0.7', 'ND', '40', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', '45', 'ND', 'ND', 'ND', '4', 'ND', 'ND'),
('< 12 mo', 'ND', 'ND', '1500', 'ND', 'ND', '0.9', 'ND', '40', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', '60', 'ND', 'ND', 'ND', '5', 'ND', 'ND'),
('Children', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('1 to 3 y', 'ND', '3', '2500', 'ND', '1000', '1.3', '200', '40', '65', '2', '300', '0.2', '3', 'ND', '90', 'ND', 'ND', 'ND', '7', 'ND', '2.3'),
('4 to 8 y', 'ND', '6', '2500', 'ND', '3000', '2.2', '300', '40', '110', '3', '600', '0.3', '3', 'ND', '150', 'ND', 'ND', 'ND', '12', 'ND', '2.9'),
('Males', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 'ND', '11', '3000', 'ND', '5000', '10', '600', '40', '350', '6', '1100', '0.6', '4', 'ND', '280', 'ND', 'ND', 'ND', '23', 'ND', '3.4'),
('14 to 18 y', 'ND', '17', '3 000', 'ND', '8 000', '10', '900', '45', '350', '9', '1 700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('51 to 70', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('> 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('Females', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 'ND', '11', '3000', 'ND', '5000', '10', '600', '40', '350', '6', '1100', '0.6', '4', 'ND', '280', 'ND', 'ND', 'ND', '23', 'ND', '3.4'),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('51 to 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('> 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('Pregnancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('Lacation', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6');

-- --------------------------------------------------------

--
-- Table structure for table `females_calories`
--

CREATE TABLE `females_calories` (
  `age` text COLLATE utf8mb4_bin,
  `sedentary` text COLLATE utf8mb4_bin,
  `moderately_active` text COLLATE utf8mb4_bin,
  `active` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `females_calories`
--

INSERT INTO `females_calories` (`age`, `sedentary`, `moderately_active`, `active`) VALUES
('2', '1,000', '1,000', '1,000'),
('3', '1,000', '1,200', '1,400'),
('4', '1,200', '1,400', '1,400'),
('5', '1,200', '1,400', '1,600'),
('6', '1,200', '1,400', '1,600'),
('7', '1,200', '1,600', '1,800'),
('8', '1,400', '1,600', '1,800'),
('9', '1,400', '1,600', '1,800'),
('10', '1,400', '1,800', '2,000'),
('11', '1,600', '1,800', '2,000'),
('12', '1,600', '2,000', '2,200'),
('13', '1,600', '2,000', '2,200'),
('14', '1,800', '2,000', '2,400'),
('15', '1,800', '2,000', '2,400'),
('16', '1,800', '2,000', '2,400'),
('17', '1,800', '2,000', '2,400'),
('18', '1,800', '2,000', '2,400'),
('19-20', '2,000', '2,200', '2,400'),
('21-25', '2,000', '2,200', '2,400'),
('26-30', '1,800', '2,000', '2,400'),
('31-35', '1,800', '2,000', '2,200'),
('36-40', '1,800', '2,000', '2,200'),
('41-45', '1,800', '2,000', '2,200'),
('46-50', '1,800', '2,000', '2,200'),
('51-55', '1,600', '1,800', '2,200'),
('56-60', '1,600', '1,800', '2,200'),
('61-65', '1,600', '1,800', '2,000'),
('66-70', '1,600', '1,800', '2,000'),
('71-75', '1,600', '1,800', '2,000'),
('76 and up', '1,600', '1,800', '2,000');

-- --------------------------------------------------------

--
-- Table structure for table `macronutrients_dist_range`
--

CREATE TABLE `macronutrients_dist_range` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Fat` bigint(20) DEFAULT NULL,
  `Linoleic Acid` bigint(20) DEFAULT NULL,
  `alpha-Linolenic Acid` double DEFAULT NULL,
  `Carbohydrate` bigint(20) DEFAULT NULL,
  `Protein` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `macronutrients_dist_range`
--

INSERT INTO `macronutrients_dist_range` (`Life-Stage Group`, `Fat`, `Linoleic Acid`, `alpha-Linolenic Acid`, `Carbohydrate`, `Protein`) VALUES
('child <= 3 y', 30, 5, 0.6, 45, 5),
('child <= 18 y', 25, 5, 0.6, 45, 10),
('adults', 20, 5, 0.6, 45, 10);

-- --------------------------------------------------------

--
-- Table structure for table `macronutrients_rdi`
--

CREATE TABLE `macronutrients_rdi` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Total Water (L/d)` double DEFAULT NULL,
  `Carbohydrates (g/d)` double DEFAULT NULL,
  `Total Fiber (g/d)` text COLLATE utf8mb4_bin,
  `Fat (g/d)` text COLLATE utf8mb4_bin,
  `Linoleic Acid (g/d)` double DEFAULT NULL,
  `alpha-Linolenic Acid (g/d)` double DEFAULT NULL,
  `Protein (g/d)` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `macronutrients_rdi`
--

INSERT INTO `macronutrients_rdi` (`Life-Stage Group`, `Total Water (L/d)`, `Carbohydrates (g/d)`, `Total Fiber (g/d)`, `Fat (g/d)`, `Linoleic Acid (g/d)`, `alpha-Linolenic Acid (g/d)`, `Protein (g/d)`) VALUES
('Infants', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('< 6 mo', 0.7, 60, 'ND', '31', 4.4, 0.5, 9.1),
('< 12 mo', 0.8, 95, 'ND', '30', 4.6, 0.5, 11),
('Children', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('1 to 3 y', 1.3, 130, '19', 'ND', 7, 0.7, 13),
('4 to 8 y', 1.7, 130, '25', 'ND', 10, 0.9, 19),
('Males', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 2.4, 130, '31', 'ND', 12, 1.2, 34),
('14 to 18 y', 3.3, 130, '38', 'ND', 16, 1.6, 52),
('19 to 30 y', 3.7, 130, '38', 'ND', 17, 1.6, 56),
('31 to 50 y', 3.7, 130, '38', 'ND', 17, 1.6, 56),
('51 to 70', 3.7, 130, '30', 'ND', 14, 1.6, 56),
('> 70 y', 3.7, 130, '30', 'ND', 14, 1.6, 56),
('Females', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 2.1, 130, '26', 'ND', 10, 1, 34),
('14 to 18 y', 2.3, 130, '26', 'ND', 11, 1.1, 46),
('19 to 30 y', 2.7, 130, '25', 'ND', 12, 1.1, 46),
('31 to 50 y', 2.7, 130, '25', 'ND', 12, 1.1, 46),
('51 to 70 y', 2.7, 130, '21', 'ND', 11, 1.1, 46),
('> 70 y', 2.7, 130, '21', 'ND', 11, 1.1, 46),
('Pregnancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 3, 175, '28', 'ND', 13, 1.4, 71),
('19 to 30 y', 3, 175, '28', 'ND', 13, 1.4, 71),
('31 to 50 y', 3, 175, '28', 'ND', 13, 1.4, 71),
('Lacation', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 3.8, 210, '29', 'ND', 13, 1.3, 71),
('19 to 30 y', 3.8, 210, '29', 'ND', 13, 1.3, 71),
('31 to 50 y', 3.8, 210, '29', 'ND', 13, 1.3, 71);

-- --------------------------------------------------------

--
-- Table structure for table `males_calories`
--

CREATE TABLE `males_calories` (
  `age` text COLLATE utf8mb4_bin,
  `sedentary` text COLLATE utf8mb4_bin,
  `moderately_active` text COLLATE utf8mb4_bin,
  `active` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `males_calories`
--

INSERT INTO `males_calories` (`age`, `sedentary`, `moderately_active`, `active`) VALUES
('2', '1,000', '1,000', '1,000'),
('3', '1,000', '1,400', '1,400'),
('4', '1,200', '1,400', '1,600'),
('5', '1,200', '1,400', '1,600'),
('6', '1,400', '1,600', '1,800'),
('7', '1,400', '1,600', '1,800'),
('8', '1,400', '1,600', '2,000'),
('9', '1,600', '1,800', '2,000'),
('10', '1,600', '1,800', '2,200'),
('11', '1,800', '2,000', '2,200'),
('12', '1,800', '2,200', '2,400'),
('13', '2,000', '2,200', '2,600'),
('14', '2,000', '2,400', '2,800'),
('15', '2,200', '2,600', '3,000'),
('16', '2,400', '2,800', '3,200'),
('17', '2,400', '2,800', '3,200'),
('18', '2,400', '2,800', '3,200'),
('19-20', '2,600', '2,800', '3,000'),
('21-25', '2,400', '2,800', '3,000'),
('26-30', '2,400', '2,600', '3,000'),
('31-35', '2,400', '2,600', '3,000'),
('36-40', '2,400', '2,600', '2,800'),
('41-45', '2,200', '2,600', '2,800'),
('46-50', '2,200', '2,400', '2,800'),
('51-55', '2,200', '2,400', '2,800'),
('56-60', '2,200', '2,400', '2,600'),
('61-65', '2,000', '2,400', '2,600'),
('66-70', '2,000', '2,200', '2,600'),
('71-75', '2,000', '2,200', '2,600'),
('76 and up', '2,000', '2,200', '2,400');

-- --------------------------------------------------------

--
-- Table structure for table `vitamins_rdi`
--

CREATE TABLE `vitamins_rdi` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Vitamin A (ug/d)` double DEFAULT NULL,
  `Vitamin C (mg/d)` double DEFAULT NULL,
  `Vitamin D (ug/d)` double DEFAULT NULL,
  `Vitamin E (mg/d)` double DEFAULT NULL,
  `Vitamin K (ug/d)` double DEFAULT NULL,
  `Thiamin (mg/d)` double DEFAULT NULL,
  `Riboflavin (mg/d)` double DEFAULT NULL,
  `Niacin (mg/d)` double DEFAULT NULL,
  `Vitamin B6 (mg/d)` double DEFAULT NULL,
  `Folate (ug/d)` double DEFAULT NULL,
  `Vitamin B12 (ug/d)` double DEFAULT NULL,
  `Pantothenic Acid (mg/d)` double DEFAULT NULL,
  `Biotin (ug/d)` double DEFAULT NULL,
  `Choline (mg/d)` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `vitamins_rdi`
--

INSERT INTO `vitamins_rdi` (`Life-Stage Group`, `Vitamin A (ug/d)`, `Vitamin C (mg/d)`, `Vitamin D (ug/d)`, `Vitamin E (mg/d)`, `Vitamin K (ug/d)`, `Thiamin (mg/d)`, `Riboflavin (mg/d)`, `Niacin (mg/d)`, `Vitamin B6 (mg/d)`, `Folate (ug/d)`, `Vitamin B12 (ug/d)`, `Pantothenic Acid (mg/d)`, `Biotin (ug/d)`, `Choline (mg/d)`) VALUES
('Infants', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('< 6 mo', 400, 40, 10, 4, 2, 0.2, 0.3, 2, 0.1, 65, 0.4, 1.7, 5, 125),
('< 12 mo', 500, 50, 10, 5, 2.5, 0.3, 0.4, 4, 0.3, 80, 0.5, 1.8, 6, 150),
('Children', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('1 to 3 y', 300, 15, 15, 6, 30, 0.5, 0.5, 6, 0.5, 150, 0.9, 2, 8, 200),
('4 to 8 y', 400, 25, 15, 7, 55, 0.6, 0.6, 8, 0.6, 200, 1.2, 3, 12, 250),
('Males', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 600, 45, 15, 11, 60, 0.9, 0.9, 12, 1, 300, 1.8, 4, 20, 375),
('14 to 18 y', 900, 75, 15, 15, 75, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 25, 550),
('19 to 30 y', 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 30, 550),
('31 to 50 y', 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 30, 550),
('51 to 70', 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.7, 400, 2.4, 5, 30, 550),
('> 70 y', 900, 90, 20, 15, 120, 1.2, 1.3, 16, 1.7, 400, 2.4, 5, 30, 550),
('Females', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 600, 45, 15, 11, 60, 0.9, 0.9, 12, 1, 300, 1.8, 4, 20, 375),
('14 to 18 y', 700, 65, 15, 15, 75, 1, 1, 14, 1.2, 400, 2.4, 5, 25, 400),
('19 to 30 y', 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.3, 400, 2.4, 5, 30, 425),
('31 to 50 y', 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.3, 400, 2.4, 5, 30, 425),
('51 to 70 y', 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.5, 400, 2.4, 5, 30, 425),
('> 70 y', 700, 75, 20, 15, 90, 1.1, 1.1, 14, 1.5, 400, 2.4, 5, 30, 425),
('Pregnancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 750, 80, 15, 15, 75, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450),
('19 to 30 y', 770, 85, 15, 15, 90, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450),
('31 to 50 y', 770, 85, 15, 15, 90, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450),
('Lacation', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 1200, 115, 15, 19, 75, 1.4, 1.6, 17, 2, 500, 2.8, 7, 35, 550),
('19 to 30 y', 1300, 120, 15, 19, 90, 1.4, 1.6, 17, 2, 500, 2.8, 7, 35, 550),
('31 to 50 y', 1300, 120, 15, 19, 90, 1.4, 1.6, 17, 2, 500, 2.8, 7, 35, 550);

-- --------------------------------------------------------

--
-- Table structure for table `vitamins_upper_rdi`
--

CREATE TABLE `vitamins_upper_rdi` (
  `Life-Stage Group` text COLLATE utf8mb4_bin,
  `Arsenic` text COLLATE utf8mb4_bin,
  `Boron (mg/d)` text COLLATE utf8mb4_bin,
  `Calcium (mg/d)` text COLLATE utf8mb4_bin,
  `Chromium` text COLLATE utf8mb4_bin,
  `Copper (ug/d)` text COLLATE utf8mb4_bin,
  `Fluoride (mg/d)` text COLLATE utf8mb4_bin,
  `Iodine (ug/d)` text COLLATE utf8mb4_bin,
  `Iron (mg/d)` text COLLATE utf8mb4_bin,
  `Magnesium (mg/d)` text COLLATE utf8mb4_bin,
  `Manganese (mg/d)` text COLLATE utf8mb4_bin,
  `Molybdenum (ug/d)` text COLLATE utf8mb4_bin,
  `Nickel (mg/d)` text COLLATE utf8mb4_bin,
  `Phosphorus (g/d)` text COLLATE utf8mb4_bin,
  `Potassium` text COLLATE utf8mb4_bin,
  `Selenium (ug/d)` text COLLATE utf8mb4_bin,
  `Silicon` text COLLATE utf8mb4_bin,
  `Sulfate` text COLLATE utf8mb4_bin,
  `Vanadium (mg/d)` text COLLATE utf8mb4_bin,
  `Zinc (mg/d)` text COLLATE utf8mb4_bin,
  `Sodium` text COLLATE utf8mb4_bin,
  `Chloride (g/d)` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `vitamins_upper_rdi`
--

INSERT INTO `vitamins_upper_rdi` (`Life-Stage Group`, `Arsenic`, `Boron (mg/d)`, `Calcium (mg/d)`, `Chromium`, `Copper (ug/d)`, `Fluoride (mg/d)`, `Iodine (ug/d)`, `Iron (mg/d)`, `Magnesium (mg/d)`, `Manganese (mg/d)`, `Molybdenum (ug/d)`, `Nickel (mg/d)`, `Phosphorus (g/d)`, `Potassium`, `Selenium (ug/d)`, `Silicon`, `Sulfate`, `Vanadium (mg/d)`, `Zinc (mg/d)`, `Sodium`, `Chloride (g/d)`) VALUES
('Infants', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('< 6 mo', 'ND', 'ND', '1000', 'ND', 'ND', '0.7', 'ND', '40', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', '45', 'ND', 'ND', 'ND', '4', 'ND', 'ND'),
('< 12 mo', 'ND', 'ND', '1500', 'ND', 'ND', '0.9', 'ND', '40', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', '60', 'ND', 'ND', 'ND', '5', 'ND', 'ND'),
('Children', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('1 to 3 y', 'ND', '3', '2500', 'ND', '1000', '1.3', '200', '40', '65', '2', '300', '0.2', '3', 'ND', '90', 'ND', 'ND', 'ND', '7', 'ND', '2.3'),
('4 to 8 y', 'ND', '6', '2500', 'ND', '3000', '2.2', '300', '40', '110', '3', '600', '0.3', '3', 'ND', '150', 'ND', 'ND', 'ND', '12', 'ND', '2.9'),
('Males', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 'ND', '11', '3000', 'ND', '5000', '10', '600', '40', '350', '6', '1100', '0.6', '4', 'ND', '280', 'ND', 'ND', 'ND', '23', 'ND', '3.4'),
('14 to 18 y', 'ND', '17', '3 000', 'ND', '8 000', '10', '900', '45', '350', '9', '1 700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('51 to 70', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('> 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('Females', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('9 to 13 y', 'ND', '11', '3000', 'ND', '5000', '10', '600', '40', '350', '6', '1100', '0.6', '4', 'ND', '280', 'ND', 'ND', 'ND', '23', 'ND', '3.4'),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('51 to 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('> 70 y', 'ND', '20', '2000', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3', 'ND', '400', 'ND', 'ND', '1.8', '40', 'ND', '3.6'),
('Pregnancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '3.5', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('Lacation', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('14 to 18 y', 'ND', '17', '3000', 'ND', '8000', '10', '900', '45', '350', '9', '1700', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '34', 'ND', '3.6'),
('19 to 30 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6'),
('31 to 50 y', 'ND', '20', '2500', 'ND', '10000', '10', '1100', '45', '350', '11', '2000', '1.0', '4', 'ND', '400', 'ND', 'ND', 'ND', '40', 'ND', '3.6');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
