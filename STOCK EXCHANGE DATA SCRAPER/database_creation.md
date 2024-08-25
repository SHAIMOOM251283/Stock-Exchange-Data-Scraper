# Create a database:
CREATE DATABASE stock_data;

# Create a user and grant privileges:
CREATE USER 'stock_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON stock_data.* TO 'stock_user'@'localhost';
FLUSH PRIVILEGES;

# Select the database:
USE stock_data;

# Create a table to store the scraped data:
CREATE TABLE stock_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255),
    date DATE,
    last_trading_price DECIMAL(10, 2),
    opening_price DECIMAL(10, 2),
    adjusted_opening_price DECIMAL(10, 2),
    yesterday_closing_price DECIMAL(10, 2),
    closing_price DECIMAL(10, 2),
    days_range VARCHAR(50),
    weeks_52_range VARCHAR(50),
    day_volume INT,
    day_trade INT,
    market_capitalization DECIMAL(15, 2)
);

# View databases:
SHOW DATABASES;

# Select databse:
USE stock_data;

# Verify table creation:
SHOW TABLES;

# View column definitions:
SHOW CREATE TABLE stock_info;

# View table Structure:
DESCRIBE stock_info;

# View data: 
SELECT * FROM stock_info;

# Vertical display: 
SELECT * FROM stock_info \G

# Limit number of rows:
SELECT * FROM stock_info LIMIT 10;

# Perform queries: 
SELECT * FROM stock_info WHERE company_name = 'LafargeHolcim Bangladesh Limited';

# Retrieve data for a specific date:
SELECT * FROM stock_info WHERE date = '2024-08-23';

# Retrieve all data for a specific company:
SELECT * FROM stock_info WHERE company_name = 'Company A';

# Retrieve data within a date range:
SELECT * FROM stock_info WHERE date BETWEEN '2024-08-01' AND '2024-08-31';

# Drop a table:
DROP TABLE table_name;

# Drop a database:
DROP DATABASE database_name;

# Delete rows for a specific company:
DELETE FROM stock_info
WHERE company_name = 'LafargeHolcim Bangladesh Limited';

# Delete rows for a specific date:
DELETE FROM stock_info
WHERE date = '2024-08-22';

# Delete all rows:
DELETE FROM stock_info;

# Truncate table (unlike DELETE, it resets any auto-increment counters): 
TRUNCATE TABLE stock_info;