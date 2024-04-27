CREATE TABLE `Account` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `account_name` varchar(45) DEFAULT NULL,
  `account_type` varchar(45) DEFAULT NULL,
  `customer_id` varchar(45) DEFAULT NULL,
  `pin` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Customer` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `is_admin` varchar(45) NOT NULL DEFAULT '0',
  `customer_user_id` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transaction_amt` varchar(45) DEFAULT NULL,
  `transaction_type` varchar(45) DEFAULT NULL,
  `transaction_date` varchar(45) DEFAULT NULL,
  `account_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
