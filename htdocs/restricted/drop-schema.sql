CREATE TABLE `data_sets` (
  `data_ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_ID` int(11) DEFAULT NULL,
  `run_status` int(11) DEFAULT NULL,
  `job_title` varchar(50) NOT NULL,
  `job_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`data_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=944 DEFAULT CHARSET=latin1;
CREATE TABLE `users` (
  `user_ID` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `results_ID` varchar(45) DEFAULT NULL,
  `organization` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `city` varchar(25) NOT NULL,
  `state` varchar(35) NOT NULL,
  `zip` varchar(15) NOT NULL,
  `country` varchar(36) NOT NULL,
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=latin1;
