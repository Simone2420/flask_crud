/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tienda
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `ciudad` varchar(20) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES
(1,'a','carlos.perez@email.com','asas','2025-01-10 10:00:00'),
(2,'Ana Gómez','ana.gomez@email.com','Medellín','2025-01-12 11:30:00'),
(3,'Pedro López','pedro.lopez@email.com','Cali','2025-01-15 14:15:00'),
(4,'María Rodríguez','maria.rodriguez@email.com','Barranquilla','2025-01-20 09:00:00'),
(5,'Juan Martínez','juan.martinez@email.com','Bucaramanga','2025-02-01 16:45:00'),
(6,'Laura Torres','laura.torres@email.com','Bogotá','2025-02-10 08:20:00'),
(7,'Diego Morales','diego.morales@email.com','Cartagena','2025-02-15 12:00:00');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedidos`
--

DROP TABLE IF EXISTS `detalle_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedidos` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `fk_detalle_pedidos_pedidos_idx` (`id_pedido`),
  KEY `fk_detalle_pedidos_productos1_idx` (`id_producto`),
  CONSTRAINT `fk_detalle_pedidos_pedidos` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_pedidos_productos1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedidos`
--

LOCK TABLES `detalle_pedidos` WRITE;
/*!40000 ALTER TABLE `detalle_pedidos` DISABLE KEYS */;
INSERT INTO `detalle_pedidos` VALUES
(1,1,1,1,3500000.00),
(2,1,2,10,80000.00),
(3,2,4,2,1200000.00),
(4,3,3,2,250000.00),
(5,3,2,25,80000.00),
(6,4,2,15,80000.00),
(7,4,6,3,180000.00),
(8,5,1,1,3500000.00),
(9,6,5,1,850000.00),
(10,7,5,2,850000.00),
(11,7,3,3,250000.00),
(12,8,2,12,80000.00),
(13,9,4,1,1200000.00),
(14,10,6,2,180000.00),
(15,11,3,1,250000.00),
(16,12,2,2,80000.00);
/*!40000 ALTER TABLE `detalle_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `fecha_pedido` datetime DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `pedidos_ibfk_1` (`id_cliente`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES
(1,1,'2025-02-01 10:00:00',4300000.00,'Entregado'),
(2,1,'2025-02-05 11:00:00',2400000.00,'Enviado'),
(3,1,'2025-02-10 14:00:00',2500000.00,'Entregado'),
(4,1,'2025-02-15 16:30:00',1740000.00,'Pendiente'),
(5,2,'2025-02-02 09:15:00',3500000.00,'Entregado'),
(6,2,'2025-02-12 15:20:00',850000.00,'Cancelado'),
(7,3,'2025-02-03 13:40:00',2450000.00,'Entregado'),
(8,3,'2025-02-08 10:10:00',960000.00,'Enviado'),
(9,3,'2025-02-14 17:00:00',1200000.00,'Entregado'),
(10,3,'2025-02-18 11:25:00',360000.00,'Pendiente'),
(11,4,'2025-02-04 12:00:00',250000.00,'Entregado'),
(12,5,'2025-02-06 18:00:00',160000.00,'Cancelado');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(45) NOT NULL,
  `categoria` varchar(45) NOT NULL,
  `precio` varchar(45) NOT NULL,
  `stock` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES
(1,'Laptop Pro 15','Tecnología','3500000.00',20),
(2,'Mouse Inalámbrico','Accesorios','80000.00',100),
(3,'Teclado Mecánico','Accesorios','250000.00',50),
(4,'Monitor 27 Pulgadas','Tecnología','1200000.00',15),
(5,'Silla Gamer','Mobiliario','850000.00',10),
(6,'Auriculares Bluetooth','Audio','180000.00',40),
(7,'Cámara Web HD','Tecnología','150000.00',30),
(8,'Escritorio Elevable','Mobiliario','1500000.00',5);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-02 11:24:23
