docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=Hello_21! -e MYSQL_DATABASE=13dtp -p 3306:3306 -v ~/13dtp/main/app/mysql-data:/var/lib/mysql -d mysql:latest
