DROP USER IF EXISTS 'graphomania'@'%';

CREATE USER 'graphomania'@'%' IDENTIFIED BY 'update_me';
GRANT ALL PRIVILEGES ON dictionary.* TO 'graphomania'@'%' WITH GRANT OPTION;
