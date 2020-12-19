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
-- Database: `dash_user`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `last` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `age` varchar(11) COLLATE utf8mb4_bin DEFAULT '35',
  `person_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `lifestage_grp` varchar(255) COLLATE utf8mb4_bin NOT NULL DEFAULT '31 to 50 y',
  `active_level` varchar(100) COLLATE utf8mb4_bin NOT NULL DEFAULT 'moderately_active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first`, `last`, `email`, `password`, `age`, `person_type`, `lifestage_grp`, `active_level`) VALUES
(1, 'Nobutaka', NULL, 'nobu.kim66@gmail.com', 'Tennis33!', '45', 'male', '31 to 50 y', 'active'),
(2, NULL, NULL, 'test@test.com', 'test', NULL, NULL, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `user_alt_ingreds`
--

CREATE TABLE `user_alt_ingreds` (
  `user_id` int(10) NOT NULL,
  `alt_ingred_id` int(100) NOT NULL,
  `prev_ingred` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `alt_ingred` varchar(255) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `user_alt_ingreds`
--

INSERT INTO `user_alt_ingreds` (`user_id`, `alt_ingred_id`, `prev_ingred`, `alt_ingred`) VALUES
(1, 1, 'Asparagus Bean', 'tuna'),
(1, 2, 'Frozen Passion Fruit', 'octopus'),
(1, 3, 'Hazelnut Butter', 'squid');

-- --------------------------------------------------------

--
-- Table structure for table `user_ingreds`
--

CREATE TABLE `user_ingreds` (
  `meal_id` int(20) NOT NULL,
  `ingred_id` int(50) NOT NULL,
  `ingred_name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `ingred_amt` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `ingred_units` varchar(20) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `user_ingreds`
--

INSERT INTO `user_ingreds` (`meal_id`, `ingred_id`, `ingred_name`, `ingred_amt`, `ingred_units`) VALUES
(1, 1, 'Beans, kidney, sprouted, raw', '333', 'g'),
(1, 2, 'Snacks, potato chips, dried potatoes, plain', '333', 'g'),
(1, 3, 'Peach nectar, canned', '333', 'ml'),
(4, 5, 'Orange juice, chilled, includes from concentrate', '333', 'ml'),
(5, 6, 'Beans, kidney, sprouted, raw', '333', 'g'),
(5, 7, 'Chinese dish, chow mein, vegetable, without meat or noodles, restaurant prepared', '333', 'ml'),
(6, 8, 'Sushi with vegetables, without fish', '20', 'piece'),
(6, 9, 'Soybean, fermented products, miso', '20', 'g'),
(7, 10, 'Grains, wheat germ, toasted, plain', '150', 'g'),
(8, 11, 'Grains, wheat germ, toasted, plain', '150', 'g'),
(8, 12, 'Sushi with vegetables, without fish', '20', 'piece'),
(9, 13, 'Orange juice, raw', '300', 'ml');

-- --------------------------------------------------------

--
-- Table structure for table `user_meals`
--

CREATE TABLE `user_meals` (
  `user_id` int(11) NOT NULL,
  `meal_id` int(11) NOT NULL,
  `meal_type` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `meal_desc` text COLLATE utf8mb4_bin NOT NULL,
  `timestamp` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `user_meals`
--

INSERT INTO `user_meals` (`user_id`, `meal_id`, `meal_type`, `meal_desc`, `timestamp`) VALUES
(1, 1, 'lunch', '', '2020-12-13'),
(1, 4, 'breakfast', '', '2020-12-13'),
(1, 5, 'breakfast', '', '2020-12-11'),
(1, 6, 'breakfast', 'sushi at Kamei Richmond and me ordering tempura udon', '2020-12-14'),
(1, 7, 'breakfast', 'plain toast, whole wheat bread', '2020-12-15'),
(1, 8, 'breakfast', 'Tuesday breakfast Japanese and Western fusion', '2020-12-15'),
(1, 9, 'dessert', 'orange juice before bedtime', '2020-12-15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_alt_ingreds`
--
ALTER TABLE `user_alt_ingreds`
  ADD PRIMARY KEY (`alt_ingred_id`);

--
-- Indexes for table `user_ingreds`
--
ALTER TABLE `user_ingreds`
  ADD PRIMARY KEY (`ingred_id`);

--
-- Indexes for table `user_meals`
--
ALTER TABLE `user_meals`
  ADD PRIMARY KEY (`meal_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `user_alt_ingreds`
--
ALTER TABLE `user_alt_ingreds`
  MODIFY `alt_ingred_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `user_ingreds`
--
ALTER TABLE `user_ingreds`
  MODIFY `ingred_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `user_meals`
--
ALTER TABLE `user_meals`
  MODIFY `meal_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_meals`
--
ALTER TABLE `user_meals`
  ADD CONSTRAINT `meals_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
