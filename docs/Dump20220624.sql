CREATE DATABASE  IF NOT EXISTS `pcto_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pcto_db`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: pcto_db
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `buildings`
--

DROP TABLE IF EXISTS `buildings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildings` (
  `id_building` varchar(7) NOT NULL,
  `b_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id_building`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id_category` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id_category`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id_certificate` int NOT NULL AUTO_INCREMENT,
  `cartification_date` date NOT NULL,
  `id_student` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_certificate`),
  KEY `id_student` (`id_student`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id_student`),
  CONSTRAINT `certificates_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `classrooms`
--

DROP TABLE IF EXISTS `classrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classrooms` (
  `id_classroom` varchar(10) NOT NULL,
  `c_name` varchar(255) NOT NULL,
  `capacity` int DEFAULT NULL,
  `id_building` varchar(7) NOT NULL,
  PRIMARY KEY (`id_classroom`),
  KEY `id_building` (`id_building`),
  CONSTRAINT `classrooms_ibfk_1` FOREIGN KEY (`id_building`) REFERENCES `buildings` (`id_building`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id_course` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(30) NOT NULL,
  `description` longtext,
  `creation_date` date NOT NULL,
  `max_partecipants` int DEFAULT NULL,
  `min_partecipants` int DEFAULT NULL,
  `min_lessons` int NOT NULL,
  `duration` int NOT NULL,
  `id_category` int NOT NULL,
  PRIMARY KEY (`id_course`),
  KEY `id_category` (`id_category`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`id_category`) REFERENCES `categories` (`id_category`),
  CONSTRAINT `courses_chk_1` CHECK ((`max_partecipants` > 0)),
  CONSTRAINT `courses_chk_2` CHECK ((`min_partecipants` > 0)),
  CONSTRAINT `courses_chk_3` CHECK ((`min_lessons` >= 0)),
  CONSTRAINT `courses_chk_4` CHECK ((`duration` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lessons`
--

DROP TABLE IF EXISTS `lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lessons` (
  `id_lesson` int NOT NULL AUTO_INCREMENT,
  `token` varchar(10) NOT NULL,
  `l_date` datetime NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `mode` enum('Online','Presenza','Duale') NOT NULL,
  `id_course` int NOT NULL,
  `id_classroom` varchar(10) NOT NULL,
  PRIMARY KEY (`id_lesson`),
  KEY `id_course` (`id_course`),
  KEY `id_classroom` (`id_classroom`),
  CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`),
  CONSTRAINT `lessons_ibfk_2` FOREIGN KEY (`id_classroom`) REFERENCES `classrooms` (`id_classroom`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id_student` int NOT NULL,
  `registration_date` date NOT NULL,
  PRIMARY KEY (`id_student`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_courses`
--

DROP TABLE IF EXISTS `students_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_courses` (
  `id_student` int NOT NULL,
  `id_course` int NOT NULL,
  `registration_date` date NOT NULL,
  PRIMARY KEY (`id_student`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `students_courses_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `users` (`id_user`),
  CONSTRAINT `students_courses_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_lessons`
--

DROP TABLE IF EXISTS `students_lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_lessons` (
  `id_lesson` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_lesson`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `students_lessons_ibfk_1` FOREIGN KEY (`id_lesson`) REFERENCES `lessons` (`id_lesson`),
  CONSTRAINT `students_lessons_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `surveys`
--

DROP TABLE IF EXISTS `surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surveys` (
  `id_survey` int NOT NULL AUTO_INCREMENT,
  `vote` int NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `id_student` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_survey`),
  KEY `id_student` (`id_student`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id_student`),
  CONSTRAINT `surveys_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`),
  CONSTRAINT `surveys_chk_1` CHECK (((`vote` >= 0) and (`vote` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id_teacher` int NOT NULL,
  PRIMARY KEY (`id_teacher`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`id_teacher`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers_courses`
--

DROP TABLE IF EXISTS `teachers_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers_courses` (
  `id_teacher` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_teacher`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `teachers_courses_ibfk_1` FOREIGN KEY (`id_teacher`) REFERENCES `teachers` (`id_teacher`),
  CONSTRAINT `teachers_courses_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokens` (
  `email` varchar(30) NOT NULL,
  `token` varchar(255) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `birth_date` date NOT NULL,
  `email` varchar(30) NOT NULL,
  `is_active` tinyint NOT NULL DEFAULT '0',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-24 19:58:38
