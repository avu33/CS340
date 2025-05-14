-- Group 21 Lorine Mijares and Annabel Vu

-- get all customer information
SELECT * FROM Customers;

-- get all menu items
SELECT * FROM MenuItems;

-- get all order details M:M
SELECT OrderDetails.orderID, OrderDetails.menuItemID, MenuItems.itemName, OrderDetails.quantity, 
    Orders.customerID, Customers.firstName, Customers.lastName
FROM OrderDetails
JOIN MenuItems ON OrderDetails.menuItemID = MenuItems.menuItemID
JOIN Orders ON OrderDetails.orderID = Orders.orderID
JOIN Customers ON Orders.customerID = Customers.customerID;

-- get all orders
SELECT * FROM Orders;

-- get all sales
SELECT * FROM Sales;

-- create new Order
INSERT INTO Orders (customerID, timeStamp, totalAmount)
VALUES (@customerID, NOW(), @totalAmount);

-- create new OrderDetail (M:M relationship)
INSERT INTO OrderDetails (orderID, menuItemID, quantity)
VALUES (@orderID, @menuItemID_from_dropdown, @quantity);

-- update quantity in OrderDetails (M:M relationship)
UPDATE OrderDetails
SET quantity = newQty
WHERE orderID = @orderID AND menuItemID = @menuItemID;

-- delete an order from OrderDetails (M:M relationship)
DELETE FROM OrderDetails
WHERE orderID = @orderID AND menuItemID = @menuItemID;

-- RESET
DELETE FROM OrderDetails;
DELETE FROM Orders;
DELETE FROM Sales;
DELETE FROM Customers;
DELETE FROM MenuItems;

