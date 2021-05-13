/*
CS4400: Introduction to Database Systems
Spring 2021
Phase III Template
Team 105
Leonard Yi Xuen Thong (lthong3)
Chenxi Gao (cgao71)
Daniel Vidal (dvidal3)
Hyunwoo Yoo (hyoo73)

Directions:
Please follow all instructions from the Phase III assignment PDF.
This file must run without error for credit.
*/

-- ID: 2a
-- Author: asmith457
-- Name: register_customer
DROP PROCEDURE IF EXISTS register_customer;
DELIMITER //
CREATE PROCEDURE register_customer(
	   IN i_username VARCHAR(40),
       IN i_password VARCHAR(40),
	   IN i_fname VARCHAR(40),
       IN i_lname VARCHAR(40),
       IN i_street VARCHAR(40),
       IN i_city VARCHAR(40),
       IN i_state VARCHAR(2),
	   IN i_zipcode CHAR(5),
       IN i_ccnumber VARCHAR(40),
	   IN i_cvv CHAR(3),
       IN i_exp_date DATE
)
BEGIN

-- Type solution below

IF i_username NOT IN (SELECT Username FROM USERS) AND LENGTH(i_zipcode) = 5 THEN
    INSERT INTO USERS VALUES (i_username, MD5(i_password), i_fname, i_lname, i_street, i_city, i_state, i_zipcode);
    INSERT INTO CUSTOMER VALUES (i_username, i_ccnumber, i_cvv, i_exp_date);
END IF;

-- End of solution
END //
DELIMITER ;

-- ID: 2b
-- Author: asmith457
-- Name: register_employee
DROP PROCEDURE IF EXISTS register_employee;
DELIMITER //
CREATE PROCEDURE register_employee(
	   IN i_username VARCHAR(40),
       IN i_password VARCHAR(40),
	   IN i_fname VARCHAR(40),
       IN i_lname VARCHAR(40),
       IN i_street VARCHAR(40),
       IN i_city VARCHAR(40),
       IN i_state VARCHAR(2),
       IN i_zipcode CHAR(5)
)
BEGIN

-- Type solution below
IF i_username NOT IN (SELECT Username FROM USERS) AND LENGTH(i_zipcode) = 5 THEN
    INSERT INTO USERS VALUES (i_username, MD5(i_password), i_fname, i_lname, i_street, i_city, i_state, i_zipcode);
    INSERT INTO EMPLOYEE VALUES (i_username);
ELSEIF i_username NOT IN (SELECT Username FROM EMPLOYEE) AND i_username NOT IN (SELECT Username FROM CUSTOMER) AND i_username NOT IN (SELECT Username FROM `ADMIN`) THEN
    INSERT INTO EMPLOYEE VALUES (i_username);
END IF;


-- End of solution
END //
DELIMITER ;

-- ID: 4a
-- Author: asmith457
-- Name: admin_create_grocery_chain
DROP PROCEDURE IF EXISTS admin_create_grocery_chain;
DELIMITER //
CREATE PROCEDURE admin_create_grocery_chain(
        IN i_grocery_chain_name VARCHAR(40)
)
BEGIN

-- Type solution below
IF i_grocery_chain_name NOT IN (SELECT ChainName FROM CHAIN) THEN
    INSERT INTO CHAIN VALUES (i_grocery_chain_name);
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 5a
-- Author: ahatcher8
-- Name: admin_create_new_store
DROP PROCEDURE IF EXISTS admin_create_new_store;
DELIMITER //
CREATE PROCEDURE admin_create_new_store(
    	IN i_store_name VARCHAR(40),
        IN i_chain_name VARCHAR(40),
    	IN i_street VARCHAR(40),
    	IN i_city VARCHAR(40),
    	IN i_state VARCHAR(2),
    	IN i_zipcode CHAR(5)
)
BEGIN
-- Type solution below
    IF (i_store_name, i_chain_name) NOT IN (SELECT StoreName, ChainName FROM STORE) AND (i_chain_name, i_zipcode) NOT IN (SELECT ChainName, Zipcode FROM STORE) THEN
        INSERT INTO STORE VALUES (i_store_name, i_chain_name, i_street, i_city, i_state, i_zipcode);
    END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 6a
-- Author: ahatcher8
-- Name: admin_create_drone
DROP PROCEDURE IF EXISTS admin_create_drone;
DELIMITER //
CREATE PROCEDURE admin_create_drone(
	   IN i_drone_id INT,
       IN i_zip CHAR(5),
       IN i_radius INT,
       IN i_drone_tech VARCHAR(40)
)
BEGIN
-- Type solution below
IF i_zip IN (SELECT Zipcode FROM STORE AS S JOIN DRONE_TECH AS DT ON (DT.StoreName, DT.ChainName) = (S.StoreName, S.ChainName) WHERE DT.Username = i_drone_tech) THEN
    INSERT INTO DRONE VALUES (i_drone_id, "available", i_zip, i_radius, i_drone_tech);
END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 7a
-- Author: ahatcher8
-- Name: admin_create_item
DROP PROCEDURE IF EXISTS admin_create_item;
DELIMITER //
CREATE PROCEDURE admin_create_item(
        IN i_item_name VARCHAR(40),
        IN i_item_type VARCHAR(40),
        IN i_organic VARCHAR(3),
        IN i_origin VARCHAR(40)
)
BEGIN
-- Type solution below
IF i_item_name NOT IN (SELECT ItemName FROM ITEM) AND (i_organic in ("Yes", "No")) AND (i_item_type in ("Dairy", "Bakery", "Meat", "Produce", "Personal Care", "Paper Goods", "Beverages", "Other")) THEN
    INSERT INTO ITEM VALUES (i_item_name, i_item_type, i_origin, i_organic);
END IF;

-- End of solution
END //
DELIMITER ;

-- ID: 8a
-- Author: dvaidyanathan6
-- Name: admin_view_customers
DROP PROCEDURE IF EXISTS admin_view_customers;
DELIMITER //
CREATE PROCEDURE admin_view_customers(
	   IN i_first_name VARCHAR(40),
       IN i_last_name VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS admin_view_customers_result;
CREATE TABLE admin_view_customers_result (
	Username VARCHAR(40) NOT NULL,
    FullName VARCHAR(80) NOT NULL,
    Address VARCHAR(87) NOT NUll,
    PRIMARY KEY (Username)
);
INSERT INTO admin_view_customers_result (Username, FullName, Address)
    SELECT CUSTOMER.Username, CONCAT(Firstname, " ", LastName) AS FullName, CONCAT(Street, ", ", City, ", ", State, " ", Zipcode) AS Address 
    FROM CUSTOMER JOIN USERS ON CUSTOMER.Username = USERS.Username WHERE (i_first_name IS NULL OR i_first_name = FirstName) AND (i_last_name IS NULL OR i_last_name = LastName);
-- End of solution
END //
DELIMITER ;

-- ID: 9a
-- Author: dvaidyanathan6
-- Name: manager_create_chain_item
DROP PROCEDURE IF EXISTS manager_create_chain_item;
DELIMITER //
CREATE PROCEDURE manager_create_chain_item(
        IN i_chain_name VARCHAR(40),
    	IN i_item_name VARCHAR(40),
    	IN i_quantity INT, 
    	IN i_order_limit INT,
    	IN i_PLU_number INT,
    	IN i_price DECIMAL(4, 2)
)
BEGIN



insert into chain_item (ChainItemName , ChainName, PLUNumber , Orderlimit,Quantity , Price) 
values(i_item_name , i_chain_name, i_PLU_number , i_order_limit ,i_quantity, i_price);

END //
DELIMITER ;

-- ID: 10a
-- Author: dvaidyanathan6
-- Name: manager_view_drone_technicians
DROP PROCEDURE IF EXISTS manager_view_drone_technicians;
DELIMITER //
CREATE PROCEDURE manager_view_drone_technicians(
	   IN i_chain_name VARCHAR(40),
       IN i_drone_tech VARCHAR(40),
       IN i_store_name VARCHAR(40)
)
BEGIN
DROP TABLE IF EXISTS manager_view_drone_technicians_result;
CREATE TABLE manager_view_drone_technicians_result (
    Username VARCHAR(40) NOT NULL,
    FullName VARCHAR(80) NOT NULL,
    Location VARCHAR(87) NOT NUll,
    PRIMARY KEY (Username)
);

INSERT INTO manager_view_drone_technicians_result (Username, FullName, Location)
    SELECT DRONE_TECH.Username, CONCAT(USERS.FirstName , ' ', USERS.LastName) AS FullName, DRONE_TECH.StoreName AS Location FROM DRONE_TECH
    JOIN USERS ON USERS.Username = DRONE_TECH.Username 
    WHERE (i_drone_tech IS NULL OR DRONE_TECH.Username = i_drone_tech) AND (i_store_name IS NULL OR DRONE_TECH.StoreName = i_store_name) AND DRONE_TECH.ChainName = i_chain_name;

END //
DELIMITER ;

-- ID: 11a
-- Author: vtata6
-- Name: manager_view_drones
DROP PROCEDURE IF EXISTS manager_view_drones;
DELIMITER //
CREATE PROCEDURE manager_view_drones(
     IN i_mgr_username varchar(40), 
     IN i_drone_id int, drone_radius int
)
BEGIN

DROP TABLE IF EXISTS manager_view_drones_result;
CREATE TABLE manager_view_drones_result (
    ID INT NOT NULL,
    Operator VARCHAR(80) NOT NULL,
    Radius int NOT NUll,
    Zip VARCHAR(40) NOT NULL,
    DroneStatus VARCHAR(87) NOT NUll,
    PRIMARY KEY (ID)
);

INSERT INTO manager_view_drones_result (ID , Operator, Radius , Zip , DroneStatus)
SELECT ID , DroneTech AS Operator , Radius , Zip , DroneStatus FROM DRONE JOIN DRONE_TECH ON DRONE_TECH.Username = DRONE.DroneTech JOIN MANAGER ON MANAGER.ChainName = DRONE_TECH.ChainName
WHERE MANAGER.Username = i_mgr_username AND (i_drone_id IS NULL OR DRONE.ID = i_drone_id) AND (drone_radius IS NULL OR DRONE.Radius >= drone_radius);

END //
DELIMITER ;

-- ID: 12a
-- Author: vtata6
-- Name: manager_manage_stores
DROP PROCEDURE IF EXISTS manager_manage_stores;
DELIMITER //
CREATE PROCEDURE manager_manage_stores(
     IN i_mgr_username varchar(50), 
     IN i_storeName varchar(50), 
     IN i_minTotal int, 
     IN i_maxTotal int
)
BEGIN
DROP TABLE IF EXISTS manager_manage_stores_result;
CREATE TABLE manager_manage_stores_result (
    StoreName VARCHAR(80) NOT NULL,
    Address VARCHAR(80) NOT NULL,
    Orders INT NOT NUll,
    Employees INT,
    Total DECIMAL(10,2) NOT NUll,
    PRIMARY KEY (StoreName)
);

SELECT OI.StoreName, OI.Address, OI.Orders, EI.Employees, OI.Total FROM (
        SELECT STORE.StoreName, Store.ChainName, CONCAT(STORE.Street, " ",STORE.City, ", ", STORE.State, " ", STORE.Zipcode) AS Address, COUNT(DISTINCT `CONTAINS`.orderID) AS Orders, SUM(`CONTAINS`.Quantity * CHAIN_ITEM.Price) AS Total
        FROM STORE
            JOIN MANAGER ON (STORE.ChainName = MANAGER.ChainName)
            JOIN DRONE_TECH ON (DRONE_TECH.StoreName = STORE.StoreName AND STORE.ChainName = DRONE_TECH.ChainName)
            JOIN DRONE ON (DRONE.Zip = STORE.Zipcode AND DRONE.DroneTech = DRONE_TECH.Username)
            JOIN ORDERS ON (DRONE.ID = ORDERS.DroneID)
            JOIN `CONTAINS` ON (ORDERS.ID = `CONTAINS`.OrderID)
            JOIN CHAIN_ITEM ON (`CONTAINS`.ItemName = CHAIN_ITEM.ChainItemName AND `CONTAINS`.ChainName = CHAIN_ITEM.ChainName AND `CONTAINS`.PLUNumber = CHAIN_ITEM.PLUNumber)
            -- RIGHT JOIN DRONE_TECH AS DT ON (DT.StoreName = STORE.StoreName AND STORE.ChainName = DT.ChainName)
            WHERE (i_storeName IS NULL OR i_storeName = STORE.StoreName)
                AND (MANAGER.Username = i_mgr_username)
            GROUP BY STORE.StoreName
                 HAVING (i_minTotal IS NULL OR SUM(`CONTAINS`.Quantity * CHAIN_ITEM.Price) >= i_minTotal)
                 AND (i_minTotal IS NULL OR SUM(`CONTAINS`.Quantity * CHAIN_ITEM.Price) <= i_maxTotal)) AS OI
        JOIN (SELECT COUNT(DISTINCT DRONE_TECH.Username) + COUNT(DISTINCT MANAGER.Username) AS Employees, STORE.StoreName, STORE.ChainName
            FROM STORE
            JOIN MANAGER ON (STORE.ChainName = MANAGER.ChainName)
            JOIN DRONE_TECH ON (DRONE_TECH.StoreName = STORE.StoreName AND STORE.ChainName = DRONE_TECH.ChainName)
                GROUP BY STORE.StoreName) AS EI
        ON (EI.StoreName = OI.StoreName AND EI.ChainName = OI.ChainName);

END //
DELIMITER ;
-- ID: 13a
-- Author: vtata6
-- Name: customer_change_credit_card_information
DROP PROCEDURE IF EXISTS customer_change_credit_card_information;
DELIMITER //
CREATE PROCEDURE customer_change_credit_card_information(
	   IN i_custUsername varchar(40), 
	   IN i_new_cc_number varchar(19), 
	   IN i_new_CVV int, 
	   IN i_new_exp_date date
)
BEGIN
update customer 
set CcNumber = i_new_cc_number ,
CVV = i_new_CVV ,
EXP_DATE = i_new_exp_date where username = i_custUsername;
END //
DELIMITER ;

-- ID: 14a
-- Author: ftsang3
-- Name: customer_view_order_history
DROP PROCEDURE IF EXISTS customer_view_order_history;
DELIMITER //
CREATE PROCEDURE customer_view_order_history(
	   IN i_username VARCHAR(40),
       IN i_orderid INT
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS customer_view_order_history_result;
Create table customer_view_order_history_result( 
	total_amount DECIMAL(6,2) NOT NULL,
    total_items INT NOT NULL,
    orderdate DATE NOT NULL,
    droneID INT,
    dronetech VARCHAR(20),
    orderstatus VARCHAR(20) NOT NULL
);


INSERT INTO customer_view_order_history_result (total_amount, total_items, orderdate, droneID, dronetech, orderstatus)
    SELECT SUM((C.Quantity * I.Price)) AS total_amount, SUM(C.Quantity) AS total_items, O.OrderDate AS orderdate, D.ID AS droneID, D.DroneTech AS dronetech, O.OrderStatus AS orderstatus
    FROM ORDERS AS O 
        JOIN CONTAINS AS C 
            ON (O.ID = C.OrderID AND O.OrderStatus NOT LIKE "Creating")
        JOIN CHAIN_ITEM AS I
            ON (I.ChainItemName, I.ChainName, I.PLUNumber) = (C.ItemName, C.ChainName, C.PLUNumber)
        LEFT JOIN DRONE AS D
            ON (O.DroneID = D.ID)
        WHERE O.CustomerUsername = i_username AND O.ID = i_orderid
        GROUP BY O.ID;
/*
INSERT INTO customer_view_order_history_result (total_amount, total_items, orderdate, droneID, dronetech, orderstatus)
    SELECT * -- (OI.total_amount, OI.total_items, OI.orderDate, DI.ID, DI.Username, OI.orderstatus)
	FROM (
        SELECT SUM(`CONTAINS`.Quantity * CHAIN_ITEM.Price) AS total_amount, COUNT(*) AS total_items, ORDERS.OrderDate, ORDERS.DroneID, ORDERS.OrderStatus FROM ORDERS
        JOIN `CONTAINS`
            ON (ORDERS.ID = `CONTAINS`.OrderID)
        JOIN CHAIN_ITEM
            ON ((CHAIN_ITEM.ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (`CONTAINS`.ItemName, `CONTAINS`.ChainName, `CONTAINS`.PLUNumber))
             WHERE ORDERS.ID = 10001
            AND ORDERS.CustomerUsername = 'hpeterson55') AS OI
        LEFT JOIN
        (SELECT DRONE.ID, DRONE_TECH.Username FROM DRONE_TECH
            LEFT JOIN DRONE
            ON (DRONE_TECH.Username = DRONE.DroneTech)) AS DI
        ON (OI.DroneID = DI.ID);
            */
    
-- End of solution
END //
DELIMITER ;

-- ID: 15a
-- Author: ftsang3
-- Name: customer_view_store_items
DROP PROCEDURE IF EXISTS customer_view_store_items;
DELIMITER //
CREATE PROCEDURE customer_view_store_items(
	   IN i_username VARCHAR(40),
       IN i_chain_name VARCHAR(40),
       IN i_store_name VARCHAR(40),
       IN i_item_type VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS customer_view_store_items_result;
CREATE TABLE customer_view_store_items_result (
    chainitemname VARCHAR(40),
    orderlimit INT
);

INSERT INTO customer_view_store_items_result (chainitemname, orderlimit)
    SELECT CHAIN_ITEM.ChainItemName, CHAIN_ITEM.OrderLimit FROM CHAIN_ITEM
        JOIN ITEM ON (CHAIN_ITEM.ChainItemName = ITEM.ItemName)
        JOIN CHAIN ON (CHAIN_ITEM.ChainName = CHAIN.ChainName)
        JOIN STORE ON (CHAIN.ChainName = STORE.ChainName)
        JOIN USERS ON (USERS.Zipcode = STORE.Zipcode)
        WHERE (CHAIN.ChainName = i_chain_name)
            AND (StoreName = i_store_name)
            AND (ItemType = i_item_type OR i_item_type = "ALL")
            AND (USERS.Username = i_username);

-- End of solution
END //
DELIMITER ;

-- ID: 15b
-- Author: ftsang3
-- Name: customer_select_items
DROP PROCEDURE IF EXISTS customer_select_items;
DELIMITER //
CREATE PROCEDURE customer_select_items(
	    IN i_username VARCHAR(40),
    	IN i_chain_name VARCHAR(40),
    	IN i_store_name VARCHAR(40),
    	IN i_item_name VARCHAR(40),
    	IN i_quantity INT
)
BEGIN
-- Type solution below
-- If possible, go back to this query and make sure procedure can be run wtice on the same item (If item already exists in contains, can't add it / updates it)
CREATE VIEW customer_select_items_result AS SELECT * FROM ORDERS JOIN CONTAINS ON ID = OrderID;

IF (SELECT Zipcode FROM STORE WHERE (StoreName, ChainName) = (i_store_name, i_chain_name)) = (SELECT Zipcode FROM USERS WHERE Username = i_username) THEN
	IF (i_username, "Creating") NOT IN (SELECT CustomerUsername, OrderStatus FROM ORDERS)  THEN
        INSERT INTO ORDERS (OrderStatus, OrderDate, CustomerUsername, DroneID) VALUES ("Creating", CURDATE(), i_username, NULL);
		IF i_quantity <= (SELECT Orderlimit FROM CHAIN_ITEM WHERE (i_chain_name, i_item_name) = (ChainName, ChainItemName)) THEN
			INSERT INTO CONTAINS (OrderID, ItemName, ChainName, PLUNumber, Quantity) VALUES (
			(SELECT ID FROM ORDERS WHERE (CustomerUsername, OrderStatus) = (i_username, "Creating")),
			i_item_name,
			i_chain_name,
			(SELECT PLUNumber FROM CHAIN_ITEM AS C WHERE (i_chain_name, i_item_name) = (C.ChainName, C.ChainItemName)),
			i_quantity
			);
		END IF;
	ELSE
		IF i_quantity <= (SELECT Orderlimit FROM CHAIN_ITEM WHERE (i_chain_name, i_item_name) = (ChainName, ChainItemName)) THEN
			IF ((SELECT ID FROM ORDERS WHERE (CustomerUsername, OrderStatus) = (i_username, "Creating")), i_item_name, i_chain_name)
			IN (SELECT OrderID, ItemName, ChainName FROM CONTAINS) THEN
				SET @temp := (SELECT Quantity FROM CONTAINS WHERE (OrderID, ItemName, ChainName) = ((SELECT ID FROM ORDERS WHERE (CustomerUsername, OrderStatus) = (i_username, "Creating")), i_item_name, i_chain_name));
				UPDATE CONTAINS SET Quantity = i_quantity + @temp WHERE 
				(OrderID, ItemName, ChainName) = ((SELECT ID FROM ORDERS WHERE (CustomerUsername, OrderStatus) = (i_username, "Creating")), i_item_name, i_chain_name);
			ELSE
				INSERT INTO CONTAINS (OrderID, ItemName, ChainName, PLUNumber, Quantity) VALUES (
				(SELECT ID FROM ORDERS WHERE (CustomerUsername, OrderStatus) = (i_username, "Creating")),
				i_item_name,
				i_chain_name,
				(SELECT PLUNumber FROM CHAIN_ITEM AS C WHERE (i_chain_name, i_item_name) = (C.ChainName, C.ChainItemName)),
				i_quantity
				);
			END IF;
		END IF;
	END IF;
END IF;
-- End of solution
END //
DELIMITER ;
         
-- ID: 16a
-- Author: jkomskis3
-- Name: customer_review_order
DROP PROCEDURE IF EXISTS customer_review_order;
DELIMITER //
CREATE PROCEDURE customer_review_order(
	   IN i_username VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS customer_review_order_result;
CREATE TABLE customer_review_order_result (
    ItemName VARCHAR(40),
    Quantity INT,
    Price DECIMAL(4, 2),
    PRIMARY KEY (ItemName, Quantity, Price)
);
	INSERT INTO customer_review_order_result
    SELECT C.ItemName, C.Quantity, I.Price FROM ORDERS AS O
    JOIN CONTAINS AS C ON C.OrderID = O.ID
    JOIN CHAIN_ITEM AS I ON (I.ChainItemName, I.ChainName, I.PLUNumber) = (C.ItemName, C.ChainName, C.PLUNumber)
    WHERE (i_username, "Creating") = (O.CustomerUsername, O.OrderStatus);
-- End of solution
END //
DELIMITER ;


-- ID: 16b
-- Author: jkomskis3
-- Name: customer_update_order
DROP PROCEDURE IF EXISTS customer_update_order;
DELIMITER //
CREATE PROCEDURE customer_update_order(
	   IN i_username VARCHAR(40),
       IN i_item_name VARCHAR(40),
       IN i_quantity INT
)
BEGIN
-- Type solution below
IF i_quantity > 0 THEN
	UPDATE `CONTAINS`
	JOIN ORDERS
	ON (ORDERS.ID = CONTAINS.OrderID)
	SET `CONTAINS`.Quantity = i_quantity
	WHERE ORDERS.CustomerUsername = i_username AND CONTAINS.ItemName = i_item_name AND OrderStatus = "Creating";
ELSE
	DELETE `CONTAINS` FROM ORDERS JOIN `CONTAINS` ON (ORDERS.ID = CONTAINS.OrderID)
	WHERE ORDERS.CustomerUsername = i_username AND CONTAINS.ItemName = i_item_name AND OrderStatus = "Creating";
END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 17a
-- Author: jkomskis3
-- Name: customer_update_order
DROP PROCEDURE IF EXISTS drone_technician_view_order_history;
DELIMITER //
CREATE PROCEDURE drone_technician_view_order_history(
        IN i_username VARCHAR(40),
    	IN i_start_date DATE,
    	IN i_end_date DATE
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS drone_technician_view_order_history_result;
Create table drone_technician_view_order_history_result( 
	ID INT,
    Operator VARCHAR(40), 
    OrderDate DATE, 
    DroneID INT,
	OrderStatus VARCHAR(20), 
    Total DECIMAL(6, 2),
    PRIMARY KEY (ID) 
);

INSERT INTO drone_technician_view_order_history_result (SELECT CONTAINS.OrderID, CONCAT(FirstName, " ", LastName) AS Operator, OrderDate, DroneID, OrderStatus, sum(CONTAINS.Quantity * Price) AS Total FROM CHAIN_ITEM JOIN CONTAINS ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN (SELECT ORDERS.ID, OrderStatus, OrderDate, CustomerUsername, DroneID, DroneTech, Zipcode as CustomerZip FROM ORDERS JOIN USERS ON CustomerUsername = Username AND OrderDate BETWEEN i_start_date and i_end_date LEFT JOIN DRONE ON DroneID = Drone.ID) AS temp ON CONTAINS.OrderID = ID AND (CONTAINS.ChainName, temp.CustomerZip) = (SELECT DRONE_TECH.ChainName, Store.Zipcode as StoreZip FROM DRONE_TECH JOIN STORE ON (DRONE_TECH.StoreName, DRONE_TECH.ChainName) = (STORE.StoreName, STORE.ChainName) AND Drone_Tech.Username = i_username) LEFT JOIN USERS ON Username = DroneTech group by OrderID);
-- End of solution
END //
DELIMITER ;

-- ID: 17b
-- Author: agoyal89
-- Name: dronetech_assign_order
DROP PROCEDURE IF EXISTS dronetech_assign_order;
DELIMITER //
CREATE PROCEDURE dronetech_assign_order(
	   IN i_username VARCHAR(40),
       IN i_droneid INT,
       IN i_status VARCHAR(20),
       IN i_orderid INT
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS temp;
Create table temp( 
	ID INT,
    Operator VARCHAR(40), 
    OrderDate DATE, 
    DroneID INT,
	OrderStatus VARCHAR(20), 
    Total DECIMAL(6, 2),
    PRIMARY KEY (ID) 
);
-- insert into results (select OrderID, Operator, OrderDate, DroneID, OrderStatus, sum(temp6.Quantity * Price) as Total from CHAIN_ITEM join (select * from CONTAINS join (SELECT ID, CONCAT(FirstName, " ", LastName) as Operator, OrderDate, DroneID, OrderStatus from (SELECT ID, Username, OrderDate, DroneID, OrderStatus From (SELECT * FROM DRONE_TECH JOIN (SELECT DroneID, DroneTech, temp.ID, OrderStatus, OrderDate, DroneStatus FROM DRONE JOIN ORDERS AS temp ON DroneID = DRONE.ID) AS temp2 ON DroneTech=DRONE_TECH.Username) AS temp3 WHERE (StoreName, ChainName) = (SELECT StoreName, ChainName FROM DRONE_TECH WHERE Username = i_username)) as temp4 join USERS ON temp4.Username = USERS.Username) as temp5 on ID = OrderID) as temp6 on (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, temp6.ChainName, temp6.PLUNumber) group by OrderID);
INSERT INTO temp (SELECT CONTAINS.OrderID, CONCAT(FirstName, " ", LastName) AS Operator, OrderDate, DroneID, OrderStatus, sum(CONTAINS.Quantity * Price) AS Total FROM CHAIN_ITEM JOIN CONTAINS ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN (SELECT ORDERS.ID, OrderStatus, OrderDate, CustomerUsername, DroneID, DroneTech, Zipcode as CustomerZip FROM ORDERS JOIN USERS ON CustomerUsername = Username LEFT JOIN DRONE ON DroneID = Drone.ID) AS temp ON CONTAINS.OrderID = ID AND (CONTAINS.ChainName, temp.CustomerZip) = (SELECT DRONE_TECH.ChainName, Store.Zipcode as StoreZip FROM DRONE_TECH JOIN STORE ON (DRONE_TECH.StoreName, DRONE_TECH.ChainName) = (STORE.StoreName, STORE.ChainName) AND Drone_Tech.Username = i_username) LEFT JOIN USERS ON Username = DroneTech group by OrderID);

-- IF i_orderid = (select ID FROM results) AND IFNULL((select ID FROM results), 1) THEN
-- select 0;
-- end if;
select * from temp;
IF (i_droneid, i_orderid) IN (select DroneID, ID FROM temp) AND (i_username, i_droneid) IN (SELECT DroneTech, ID FROM DRONE) THEN 
    UPDATE ORDERS SET OrderStatus = i_status WHERE i_orderid = ID;
	IF i_status = "Delivered" THEN
		UPDATE DRONE SET DroneStatus = "Available" WHERE ID = i_droneid;
	END IF;
END IF;

IF i_orderid IN (SELECT ID FROM temp) AND IFNULL((SELECT ID FROM temp WHERE i_orderid = ID), 1) AND (i_username, i_droneid) IN (SELECT DroneTech, ID FROM DRONE) THEN 
    UPDATE ORDERS SET OrderStatus = i_status, DroneID = i_droneid WHERE i_orderid = ID;
	UPDATE DRONE SET DroneStatus = "Busy" WHERE i_droneid = ID;
    
 	IF i_status = "Delivered" THEN
		UPDATE DRONE SET DroneStatus = "Available" WHERE ID = i_droneid;
	END IF;
END IF;


-- End of solution
END //
DELIMITER ;

-- ID: 18a
-- Author: agoyal89
-- Name: dronetech_order_details
DROP PROCEDURE IF EXISTS dronetech_order_details;
DELIMITER //
CREATE PROCEDURE dronetech_order_details(
	   IN i_username VARCHAR(40),
       IN i_orderid VARCHAR(40)
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS temp;
Create table temp( 
	ID INT,
    Operator VARCHAR(40), 
    OrderDate DATE, 
    DroneID INT,
	OrderStatus VARCHAR(20), 
    Total DECIMAL(6, 2),
    PRIMARY KEY (ID) 
);
Drop TABLE IF EXISTS dronetech_order_details_result;
Create table dronetech_order_details_result( 
Customer_Name VARCHAR(80), 
Order_ID INT NOT NULL,
Total_Amount DECIMAL(6, 2), 
Total_Items INT, 
Date_Of_Purchase DATE,
Drone_ID INT, 
Store_Associate VARCHAR(80), 
Order_Status VARCHAR(20), 
Address VARCHAR(100),
PRIMARY KEY (Order_ID)
);

INSERT INTO temp (SELECT CONTAINS.OrderID, Username, OrderDate, DroneID, OrderStatus, sum(CONTAINS.Quantity * Price) AS Total FROM CHAIN_ITEM JOIN CONTAINS ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN (SELECT ORDERS.ID, OrderStatus, OrderDate, CustomerUsername, DroneID, DroneTech, Zipcode as CustomerZip FROM ORDERS JOIN USERS ON CustomerUsername = Username LEFT JOIN DRONE ON DroneID = Drone.ID) AS temp ON CONTAINS.OrderID = ID AND (CONTAINS.ChainName, temp.CustomerZip) = (SELECT DRONE_TECH.ChainName, Store.Zipcode as StoreZip FROM DRONE_TECH JOIN STORE ON (DRONE_TECH.StoreName, DRONE_TECH.ChainName) = (STORE.StoreName, STORE.ChainName) AND Drone_Tech.Username = i_username) LEFT JOIN USERS ON Username = DroneTech group by OrderID);

IF (i_username, i_orderid) in (SELECT Operator, ID FROM temp) THEN
	INSERT INTO dronetech_order_details_result (SELECT concat(cust.FirstName, " ", cust.LastName) AS "Customer Name", i_orderid AS "Order ID", sum(CONTAINS.Quantity * Price) AS "Total Amount", sum(CONTAINS.Quantity) AS "Total Items", OrderDate AS "Date Of Purchase", DroneID AS "Drone ID", concat(emp.FirstName, " ", emp.LastName) AS "Store Associate", OrderStatus AS "Status", concat(cust.Street, ", ", cust.City, ", ", cust.State, " ", cust.Zipcode) AS Address FROM ORDERS LEFT JOIN DRONE ON DroneID = Drone.ID JOIN USERS AS cust ON CustomerUsername = Username AND ORDERS.ID = i_orderid JOIN CONTAINS ON CONTAINS.OrderID = i_orderid JOIN CHAIN_ITEM ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN USERS AS emp ON DroneTech = emp.Username);
END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 18b
-- Author: agoyal89
-- Name: dronetech_order_items
DROP PROCEDURE IF EXISTS dronetech_order_items;
DELIMITER //
CREATE PROCEDURE dronetech_order_items(
        IN i_username VARCHAR(40),
    	IN i_orderid INT
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS temp;
Create table temp( 
	ID INT,
    Operator VARCHAR(40), 
    OrderDate DATE, 
    DroneID INT,
	OrderStatus VARCHAR(20), 
    Total DECIMAL(6, 2),
    PRIMARY KEY (ID) 
);
Drop TABLE IF EXISTS dronetech_order_items_result;
Create table dronetech_order_items_result( 
Item VARCHAR(40) NOT NULL, 
Count INT,
PRIMARY KEY (Item)
);

INSERT INTO temp (SELECT CONTAINS.OrderID, Username, OrderDate, DroneID, OrderStatus, sum(CONTAINS.Quantity * Price) AS Total FROM CHAIN_ITEM JOIN CONTAINS ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN (SELECT ORDERS.ID, OrderStatus, OrderDate, CustomerUsername, DroneID, DroneTech, Zipcode as CustomerZip FROM ORDERS JOIN USERS ON CustomerUsername = Username LEFT JOIN DRONE ON DroneID = Drone.ID) AS temp ON CONTAINS.OrderID = ID AND (CONTAINS.ChainName, temp.CustomerZip) = (SELECT DRONE_TECH.ChainName, Store.Zipcode as StoreZip FROM DRONE_TECH JOIN STORE ON (DRONE_TECH.StoreName, DRONE_TECH.ChainName) = (STORE.StoreName, STORE.ChainName) AND Drone_Tech.Username = i_username) LEFT JOIN USERS ON Username = DroneTech group by OrderID);

IF (i_username, i_orderid) in (SELECT Operator, ID FROM temp) THEN
	INSERT INTO dronetech_order_items_result (SELECT ItemName, CONTAINS.Quantity FROM ORDERS LEFT JOIN DRONE ON DroneID = Drone.ID JOIN CONTAINS ON CONTAINS.OrderID = i_orderid JOIN CHAIN_ITEM ON ORDERS.ID = i_orderid AND (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber));
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 19a
-- Author: agoyal89
-- Name: dronetech_assigned_drones
DROP PROCEDURE IF EXISTS dronetech_assigned_drones;
DELIMITER //
CREATE PROCEDURE dronetech_assigned_drones(
        IN i_username VARCHAR(40),
    	IN i_droneid INT,
    	IN i_status VARCHAR(20)
)
BEGIN
-- Type solution below
Drop TABLE IF EXISTS dronetech_assigned_drones_result;
Create table dronetech_assigned_drones_result( 
	Drone_ID INT, 
	Status VARCHAR(20), 
	Radius INT
); 
IF ifnull(i_droneid, 1) THEN
	SET i_droneid := (SELECT ID FROM DRONE WHERE DroneTech = i_username);
END IF;
IF i_status = "All" OR ifnull(i_status, 1) THEN
	SET i_status := (SELECT DroneStatus FROM DRONE WHERE DroneTech = i_username);
END IF;
INSERT INTO dronetech_assigned_drones_result (SELECT ID, DroneStatus, Radius FROM DRONE WHERE DroneTech = i_username AND ID IN (i_droneid) AND DroneStatus IN (i_status));
-- End of solution
END //
DELIMITER ;
