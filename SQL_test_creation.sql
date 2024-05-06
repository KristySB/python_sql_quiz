CREATE DATABASE test_database;
USE test_database;

CREATE SCHEMA test;
GO

CREATE TABLE test.sql_test(
	quest_id INT IDENTITY (1, 1) PRIMARY KEY,
	question VARCHAR (1000) NOT NULL,
	answer VARCHAR (1000) NOT NULL
);

ALTER TABLE test.sql_test
ADD category VARCHAR(255) NOT NULL;

INSERT INTO test.sql_test VALUES
	('Find the customer (first_name, last_name) whose last name is Berg and the first name is Monika. (table sales.customers)', 'SELECT first_name, last_name FROM sales.customers WHERE last_name = ''Berg'' AND first_name = ''Monika''', 'WHERE'),
	('List customer id and the order year(transform the order date to order year) in which the customer made orders. Order the result by customer id, order year. (table sales.orders)', 'SELECT customer_id, YEAR(order_date) AS order_year FROM sales.orders GROUP BY customer_id, YEAR(order_date) ORDER BY customer_id, YEAR(order_date);', 'GROUP BY'),
	('Return the customer id, order year and number of orders placed by the customer by year. Order the result by customer id and order year. (table sales.orders)', 'SELECT customer_id, YEAR(order_date) AS order_year, COUNT(*) AS [number of orders] FROM sales.orders GROUP BY customer_id, YEAR(order_date) ORDER BY customer_id, YEAR(order_date);', 'GROUP BY'),
	('Return the city and  number of customers in every city. Order the rows by city. (table sales.customers)', 'SELECT city, COUNT(customer_id) AS [number of customers] FROM sales.customers GROUP BY city ORDER BY city;', 'GROUP BY'),
	('Return the brand id, minimum and maximum list prices of all products with the model 2018. Group and order the result by brand.(table production.products)', 'SELECT brand_id, MAX(list_price) AS max_price, MIN(list_price) AS min_price FROM production.products WHERE model_year = 2018 GROUP BY brand_id ORDER BY brand_id;', 'GROUP BY'),
	('Return the brand nam and average list price by brand name for all products with the model year 2018.(tables production.brands, production.products)', 'SELECT brand_name, AVG(p.list_price) AS avg_price FROM production.brands AS b JOIN production.products AS p ON p.brand_id = b.brand_id WHERE p.model_year = 2018 GROUP BY brand_name ORDER BY brand_name;', 'GROUP BY'),
	('Find the order id of the sales orders whose net values are greater than 20,000. Order the result by order id. (table sales.order_items)', 'SELECT order_id, SUM(list_price * quantity * (1 - discount)) AS net_value FROM sales.order_items GROUP BY order_id HAVING SUM(list_price * quantity * (1 - discount)) > 20000 ORDER BY order_id;', 'GROUP BY'),
	('Select store_id and product_id. Find the producs that has no sales across the stores. (tables production.products, sales.stores, sales.order_items)', 'SELECT s.store_id, p.product_id FROM production.products AS p CROSS JOIN sales.stores AS s LEFT JOIN(SELECT p.product_id, o.store_id, i.quantity AS quantity FROM sales.order_items AS i JOIN production.products AS p ON p.product_id = i.product_id JOIN sales.orders AS o ON o.order_id = i.order_id ) AS c ON p.product_id = c.product_id AND s.store_id = c.store_id WHERE quantity IS NULL ORDER BY s.store_id, p.product_id;', 'CROSS JOIN, JOIN'),
	('Select city, state and number of customers by state and city. Order the result by city, state. (table sales.customers)', 'SELECT city, state, COUNT(customer_id) AS [number od customers] FROM sales.customers GROUP BY city, state ORDER BY city, state;', 'GROUP BY'),
	('Select category_id and the maximum and minimum list prices in each product category. Select only the categories with maximum list price greater than 4,000 or the minimum list price less than 500. (table production.products)', 'SELECT category_id, MAX(list_price) AS max_price, MIN(list_price) AS min_price FROM production.products GROUP BY category_id HAVING MAX(list_price) > 4000 OR MIN(list_price) < 500;', 'GROUP BY'),
	('Find category_id and average list prices that are between 500 and 1,000. (table production.products)', 'SELECT category_id, AVG(list_price) AS avg_price FROM production.products GROUP BY category_id HAVING AVG(list_price) BETWEEN 500 AND 1000;', 'GROUP BY, HAVING'),
	('Find all the orders that customers placed between January 15, 2017 and January 17, 2017. (sales.orders table)', 'SELECT * FROM sales.orders WHERE shipped_date BETWEEN ''2017-01-15'' AND ''2017-01-17'';', 'BETWEEN'),
	('Find all the customers where the first character in the last name is the letter in the range A through C. (sales.customers table)', 'SELECT * FROM sales.customers WHERE last_name LIKE ''[a-c]%'' ORDER BY last_name;', 'LIKE'),
	('Find all the customers where the first character in the last name is not the letter in the range A through X (sales.customers table).', 'SELECT * FROM sales.customers WHERE last_name LIKE ''[^a-x]%'' ORDER BY last_name;', 'LIKE'),
	('List product name and list price of the products ordered by the price from less to most expensive. Skip first 10 rows and list only next 10 rows. (production.product table)', ' SELECT product_name, list_price FROM production.products ORDER BY list_price, product_name OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;', 'OFFSET, FETCH'),
	('In production.product table select 10 most expensive products. List product_name and list_price only.', 'SELECT TOP 10 product_name, list_price FROM production.products ORDER BY list_price DESC, product_name;', 'TOP 10'),
	('List 1 percent of products - product_name, list_price (production.productS table) ordered them from more expensive to less expensive.', 'SELECT TOP 1 PERCENT product_name, list_price FROM production.products ORDER BY list_price DESC;', 'SELECT TOP'),
	('List 3 most expensive products- product_name, list_price (production.products table) if the 3rd has the same price as some others, list even the other products.', 'SELECT TOP 3 WITH TIES product_name, list_price FROM production.products ORDER BY list_price DESC;', 'WITH TIES'),
	('List all the customers from which we dont have the phone number (sales.customers table).', 'SELECT * FROM sales.customers WHERE phone IS NULL;', 'IS NULL'),
	('List the products whose brand id is one or two and list price is larger than 1,000 (production.products table).', 'SELECT * FROM production.products WHERE (brand_id = 1 OR brand_id = 2) AND list_price > 1000 ORDER BY list_price DESC, product_name;','WHERE');

CREATE TABLE test.player(
	player_id INT IDENTITY (1, 1) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	surname VARCHAR(255) NOT NULL,
	points INT
);
ALTER TABLE test.player
ADD answered_questions INT;

CREATE TABLE test.answer(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	player_id INT NOT NULL,
	quest_id INT NOT NULL,
	answer CHAR(1) NOT NULL,
	CONSTRAINT FK_player_answer FOREIGN KEY(player_id) REFERENCES test.player(player_id) ON DELETE CASCADE,
	CONSTRAINT FK_question_answer FOREIGN KEY(quest_id) REFERENCES test.sql_test(quest_id) ON DELETE CASCADE
);