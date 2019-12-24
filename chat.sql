-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: concurrent_communion
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `base_info`
--

DROP TABLE IF EXISTS `base_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `password` varchar(32) NOT NULL,
  `register_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_info`
--

LOCK TABLES `base_info` WRITE;
/*!40000 ALTER TABLE `base_info` DISABLE KEYS */;
INSERT INTO `base_info` VALUES (1,'Tom','123','2019-11-20 19:57:23'),(2,'Lily','456','2019-11-23 10:14:47'),(3,'caocao','caocao','2019-11-28 08:46:22'),(4,'Jame','789','2019-11-29 18:36:37'),(5,'liubei','liubei','2019-12-12 21:35:11');
/*!40000 ALTER TABLE `base_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `content` varchar(128) DEFAULT NULL,
  `send_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_history`
--

LOCK TABLES `chat_history` WRITE;
/*!40000 ALTER TABLE `chat_history` DISABLE KEYS */;
INSERT INTO `chat_history` VALUES (1,'Lily','hello','2019-11-29 19:22:50'),(2,'Tom','my name is Tom','2019-11-29 19:25:38'),(3,'Jame','how are you','2019-11-29 19:25:51'),(4,'Tom','hi,Jame','2019-11-29 19:26:37'),(5,'Lily','nihao','2019-11-29 19:29:09'),(6,'Lily','hello','2019-12-01 19:35:50'),(7,'caocao','my name is caocao','2019-12-01 19:36:01'),(8,'Tom','nice to meet you','2019-12-01 19:36:19'),(9,'Lily','hello','2019-12-01 19:45:27'),(10,'caocao','my name is caocao','2019-12-01 19:45:40'),(11,'Tom','nice to meet you','2019-12-01 19:45:51'),(12,'Tom','hi','2019-12-02 20:25:29'),(13,'Tom','good game','2019-12-02 20:43:23'),(14,'Lily','hehe','2019-12-02 20:43:33'),(15,'Tom','4354354','2019-12-03 10:05:09'),(16,'Lily','hello','2019-12-05 08:41:11'),(17,'Tom','hi','2019-12-05 08:41:18'),(18,'caocao','my name is caocao','2019-12-05 08:41:25'),(19,'Lily','haha','2019-12-05 08:44:07'),(20,'Lily','the project is best','2019-12-05 09:16:39'),(21,'caocao','I can not agree more','2019-12-05 09:17:12'),(22,'Jame','hello,everyone','2019-12-11 09:02:47'),(23,'Tom','hi,Jame','2019-12-11 09:02:57'),(24,'Lily','nice to meet you','2019-12-11 09:03:12'),(25,'Tom','haha','2019-12-11 21:25:34'),(26,'Jame','hello , everyone','2019-12-11 21:25:45'),(27,'Lily','so happy to meet you','2019-12-11 21:26:00'),(28,'Tom','123','2019-12-11 21:39:19'),(29,'Tom','hello','2019-12-12 21:36:08'),(30,'Lily','hi','2019-12-12 21:36:24'),(31,'Jame','our project is best','2019-12-13 10:33:01'),(32,'caocao','I can not agree more','2019-12-13 10:33:20'),(33,'Jame','Good Game','2019-12-13 10:37:25'),(34,'Lily','my name is Lily','2019-12-13 11:16:44'),(35,'Jame','nice to meet you','2019-12-13 11:16:56');
/*!40000 ALTER TABLE `chat_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_put_record`
--

DROP TABLE IF EXISTS `file_put_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `file_put_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `file_name` varchar(16) DEFAULT NULL,
  `send_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_put_record`
--

LOCK TABLES `file_put_record` WRITE;
/*!40000 ALTER TABLE `file_put_record` DISABLE KEYS */;
INSERT INTO `file_put_record` VALUES (2,'Lily','view.gif','2019-12-13 10:34:09');
/*!40000 ALTER TABLE `file_put_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_record`
--

DROP TABLE IF EXISTS `game_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `result` varchar(8) DEFAULT NULL,
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_record`
--

LOCK TABLES `game_record` WRITE;
/*!40000 ALTER TABLE `game_record` DISABLE KEYS */;
INSERT INTO `game_record` VALUES (1,'Lily','victory','2019-12-05 21:08:06'),(2,'Tom','defeat','2019-12-05 21:08:06'),(3,'Tom','victory','2019-12-11 09:04:12'),(4,'Jame','defeat','2019-12-11 09:04:12'),(5,'Lily','defeat','2019-12-11 21:32:24'),(6,'Lily','victory','2019-12-11 21:33:59'),(7,'Jame','defeat','2019-12-11 21:33:59'),(8,'caocao','defeat','2019-12-12 21:39:47'),(9,'caocao','victory','2019-12-12 21:44:25'),(10,'Tom','defeat','2019-12-12 21:44:25'),(11,'caocao','victory','2019-12-13 10:37:04'),(12,'Jame','defeat','2019-12-13 10:37:05');
/*!40000 ALTER TABLE `game_record` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-13 11:19:02
