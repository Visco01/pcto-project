-- pcto_db.buildings definition

CREATE TABLE `buildings` (
  `id_building` varchar(7) NOT NULL,
  `b_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `latitude` decimal(8,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`id_building`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.categories definition

CREATE TABLE `categories` (
  `id_category` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.tokens definition

CREATE TABLE `tokens` (
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(30) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.users definition

CREATE TABLE `users` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `birth_date` date NOT NULL,
  `email` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `registration_date` date NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.classrooms definition

CREATE TABLE `classrooms` (
  `id_classroom` varchar(10) NOT NULL,
  `c_name` varchar(255) NOT NULL,
  `capacity` int DEFAULT NULL,
  `id_building` varchar(7) NOT NULL,
  PRIMARY KEY (`id_classroom`),
  KEY `id_building` (`id_building`),
  CONSTRAINT `classrooms_ibfk_1` FOREIGN KEY (`id_building`) REFERENCES `buildings` (`id_building`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.courses definition

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.lessons definition

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.students definition

CREATE TABLE `students` (
  `id_student` int NOT NULL,
  PRIMARY KEY (`id_student`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.students_courses definition

CREATE TABLE `students_courses` (
  `id_student` int NOT NULL,
  `id_course` int NOT NULL,
  `registration_date` date NOT NULL,
  PRIMARY KEY (`id_student`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `students_courses_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `users` (`id_user`),
  CONSTRAINT `students_courses_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.students_lessons definition

CREATE TABLE `students_lessons` (
  `id_lesson` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_lesson`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `students_lessons_ibfk_1` FOREIGN KEY (`id_lesson`) REFERENCES `lessons` (`id_lesson`),
  CONSTRAINT `students_lessons_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.surveys definition

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


-- pcto_db.teachers definition

CREATE TABLE `teachers` (
  `id_teacher` int NOT NULL,
  PRIMARY KEY (`id_teacher`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`id_teacher`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.teachers_courses definition

CREATE TABLE `teachers_courses` (
  `id_teacher` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_teacher`,`id_course`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `teachers_courses_ibfk_1` FOREIGN KEY (`id_teacher`) REFERENCES `teachers` (`id_teacher`),
  CONSTRAINT `teachers_courses_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pcto_db.certificates definition

CREATE TABLE `certificates` (
  `id_certificate` int NOT NULL AUTO_INCREMENT,
  `certification_date` date NOT NULL,
  `id_student` int NOT NULL,
  `id_course` int NOT NULL,
  PRIMARY KEY (`id_certificate`),
  KEY `id_student` (`id_student`),
  KEY `id_course` (`id_course`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id_student`),
  CONSTRAINT `certificates_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `courses` (`id_course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;