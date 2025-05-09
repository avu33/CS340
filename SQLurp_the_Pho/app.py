# ########################################
# ########## SETUP
PORT = 1027
from flask import Flask, render_template, request, redirect
import database.db_connector as db  # Adjust this if your path is different

PORT = 1027
app = Flask(__name__)

# Home page route
@app.route("/", methods=["GET"])
def home():
    try:
        return render_template("home.j2")
    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500

# READ: Customers Page
@app.route("/customers", methods=["GET"])
def customers():
    try:
        dbConnection = db.connectDB()
        query = "SELECT * FROM Customers;"
        customers = db.query(dbConnection, query).fetchall()
        return render_template("customers.j2", customers=customers)
    except Exception as e:
        print(f"Error executing customers query: {e}")
        return "An error occurred while executing the database queries.", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# # CREATE: Add a customer
# @app.route("/create-customer", methods=["POST"])
# def create_customer():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form

#         query = """
#             INSERT INTO Customers (firstName, lastName, email, marketingOptOut, customerType, visitCount)
#             VALUES (%s, %s, %s, %s, %s, %s);
#         """
#         values = (
#             data.get("firstName"),
#             data.get("lastName"),
#             data.get("email"),
#             int(data.get("marketingOptOut", 0)),
#             data.get("customerType"),
#             int(data.get("visitCount", 1)),
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/customers")
#     except Exception as e:
#         print(f"Error inserting customer: {e}")
#         return "An error occurred while creating the customer.", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # UPDATE: Modify a customer
# @app.route("/update-customer", methods=["POST"])
# def update_customer():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form

#         query = """
#             UPDATE Customers
#             SET email = %s,
#                 marketingOptOut = %s,
#                 customerType = %s,
#                 visitCount = %s
#             WHERE customerID = %s;
#         """
#         values = (
#             data.get("email"),
#             int(data.get("marketingOptOut", 0)),
#             data.get("customerType"),
#             int(data.get("visitCount", 1)),
#             int(data.get("customerID")),
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/customers")
#     except Exception as e:
#         print(f"Error updating customer: {e}")
#         return "An error occurred while updating the customer.", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # DELETE: Remove a customer
# @app.route("/delete-customer", methods=["POST"])
# def delete_customer():
#     try:
#         dbConnection = db.connectDB()
#         customer_id = request.form.get("customerID")
#         query = "DELETE FROM Customers WHERE customerID = %s;"
#         db.query(dbConnection, query, (customer_id,))
#         dbConnection.commit()
#         return redirect("/customers")
#     except Exception as e:
#         print(f"Error deleting customer: {e}")
#         return "An error occurred while deleting the customer.", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# READ: Orders Page
@app.route("/orders", methods=["GET"])
def orders():
    try:
        dbConnection = db.connectDB()
        orders_query = "SELECT * FROM Orders;"
        customers_query = "SELECT customerID, firstName, lastName FROM Customers;"
        orders = db.query(dbConnection, orders_query).fetchall()
        customers = db.query(dbConnection, customers_query).fetchall()
        print("Orders:", orders)
        print("Customers:", customers)
        return render_template("orders.j2", orders=orders, customers=customers)
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return "Failed to load orders", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# CREATE: Add an order
# @app.route("/create-order", methods=["POST"])
# def create_order():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form
#         query = "INSERT INTO Orders (customerID, timestamp, totalAmount) VALUES (%s, %s, %s);"
#         values = (
#             data.get("customerID"),
#             data.get("timestamp"),  # Expected format: YYYY-MM-DD HH:MM:SS
#             data.get("totalAmount")
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/orders")
#     except Exception as e:
#         print(f"Error creating order: {e}")
#         return "Failed to create order", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # UPDATE: Modify an order
# @app.route("/update-order", methods=["POST"])
# def update_order():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form
#         query = """
#             UPDATE Orders
#             SET customerID = %s,
#                 timestamp = %s,
#                 totalAmount = %s
#             WHERE orderID = %s;
#         """
#         values = (
#             data.get("customerID"),
#             data.get("timestamp"),
#             data.get("totalAmount"),
#             data.get("orderID")
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/orders")
#     except Exception as e:
#         print(f"Error updating order: {e}")
#         return "Failed to update order", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # DELETE: Remove an order
# @app.route("/delete-order", methods=["POST"])
# def delete_order():
#     try:
#         dbConnection = db.connectDB()
#         order_id = request.form.get("orderID")
#         query = "DELETE FROM Orders WHERE orderID = %s;"
#         db.query(dbConnection, query, (order_id,))
#         dbConnection.commit()
#         return redirect("/orders")
#     except Exception as e:
#         print(f"Error deleting order: {e}")
#         return "Failed to delete order", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# READ and UPDATE: Order Details Page
@app.route('/order-details', methods=["GET", "POST"])
def order_details():
    dbConnection = db.connectDB()

    if request.method == "POST":
        try:
            order_id = request.form["orderID"]
            menu_item_id = request.form["menuItemID"]
            quantityMenuItem = request.form["quantityMenuItem"]

            update_query = """
                UPDATE OrderDetails
                SET quantityMenuItem = %s
                WHERE orderID = %s AND menuItemID = %s;
            """
            db.query(dbConnection, update_query, (quantityMenuItem, order_id, menu_item_id))
        except Exception as e:
            print("Error updating order detail:", e)

    try:
        # Main view query
        select_query = """
            SELECT OrderDetails.orderID, OrderDetails.menuItemID, MenuItems.itemName, 
                   OrderDetails.quantityMenuItem, Orders.customerID, 
                   Customers.firstName, Customers.lastName
            FROM OrderDetails
            JOIN MenuItems ON OrderDetails.menuItemID = MenuItems.menuItemID
            JOIN Orders ON OrderDetails.orderID = Orders.orderID
            JOIN Customers ON Orders.customerID = Customers.customerID;
        """
        cursor = db.query(dbConnection, select_query)
        results = cursor.fetchall()

        # Dropdown data
        orders = db.query(dbConnection, "SELECT orderID FROM Orders;").fetchall()
        menu_items = db.query(dbConnection, "SELECT menuItemID, itemName FROM MenuItems;").fetchall()

    except Exception as e:
        print("Error fetching order details:", e)
        results, orders, menu_items = [], [], []
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

    return render_template(
        "order_details.j2",
        order_details=results,
        orders=orders,
        menu_items=menu_items
    )


# # CREATE: Add new Order Detail
# @app.route("/create-order-detail", methods=["POST"])
# def create_order_detail():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form

#         query = """
#             INSERT INTO OrderDetails (orderID, menuItemID, quantity)
#             VALUES (%s, %s, %s);
#         """
#         values = (
#             data.get("orderID"),
#             data.get("menuItemID"),
#             data.get("quantity")
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/order-details")
#     except Exception as e:
#         print(f"Error creating order detail: {e}")
#         return "Failed to create order detail", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()


# # DELETE: Remove Order Detail
# @app.route("/delete-order-detail", methods=["POST"])
# def delete_order_detail():
#     try:
#         dbConnection = db.connectDB()
#         order_id = request.form.get("orderID")
#         menu_item_id = request.form.get("menuItemID")

#         query = """
#             DELETE FROM OrderDetails
#             WHERE orderID = %s AND menuItemID = %s;
#         """
#         db.query(dbConnection, query, (order_id, menu_item_id))
#         dbConnection.commit()
#         return redirect("/order-details")
#     except Exception as e:
#         print(f"Error deleting order detail: {e}")
#         return "Failed to delete order detail", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()


# READ: Menu Items Page
@app.route("/menu-items", methods=["GET"])
def menu_items():
    try:
        dbConnection = db.connectDB()
        query = "SELECT * FROM MenuItems;"
        items = db.query(dbConnection, query).fetchall()
        return render_template("menu_items.j2", menu_items=items)
    except Exception as e:
        print(f"Error fetching menu items: {e}")
        return "Failed to load menu items", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# # CREATE: Add a menu item
# @app.route("/create-menu-item", methods=["POST"])
# def create_menu_item():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form
#         query = """
#             INSERT INTO MenuItems (itemName, description, price, costOfFood)
#             VALUES (%s, %s, %s, %s);
#         """
#         values = (
#             data.get("itemName"),
#             data.get("description"),
#             data.get("price"),
#             data.get("costOfFood")  # now a string like '20%' or '50%'
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/menu-items")
#     except Exception as e:
#         print(f"Error creating menu item: {e}")
#         return "Failed to create menu item", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # # UPDATE: Modify a menu item
# @app.route("/update-menu-item", methods=["POST"])
# def update_menu_item():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form
#         query = """
#             UPDATE MenuItems
#             SET description = %s,
#                 price = %s,
#                 costOfFood = %s
#             WHERE menuItemID = %s;
#         """
#         values = (
#             data.get("description"),
#             data.get("price"),
#             data.get("costOfFood"),  # string ENUM value
#             data.get("menuItemID")
#         )
#         db.query(dbConnection, query, values)
#         dbConnection.commit()
#         return redirect("/menu-items")
#     except Exception as e:
#         print(f"Error updating menu item: {e}")
#         return "Failed to update menu item", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # DELETE: Remove a menu item
# @app.route("/delete-menu-item", methods=["POST"])
# def delete_menu_item():
#     try:
#         dbConnection = db.connectDB()
#         item_id = request.form.get("menuItemID")
#         query = "DELETE FROM MenuItems WHERE menuItemID = %s;"
#         db.query(dbConnection, query, (item_id,))
#         dbConnection.commit()
#         return redirect("/menu-items")
#     except Exception as e:
#         print(f"Error deleting menu item: {e}")
#         return "Failed to delete menu item", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# READ: Sales Page
@app.route("/sales", methods=["GET"])
def sales():
    try:
        dbConnection = db.connectDB()
        sales_query = "SELECT * FROM Sales;"
        items_query = "SELECT * FROM MenuItems;"
        sales = db.query(dbConnection, sales_query).fetchall()
        menu_items = db.query(dbConnection, items_query).fetchall()
        return render_template("sales.j2", sales=sales, menu_items=menu_items)
    except Exception as e:
        print(f"Error fetching sales: {e}")
        return "Failed to load sales", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# # CREATE: Add a sale
# @app.route("/create-sale", methods=["POST"])
# def create_sale():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form

#         menu_item_id = int(data.get("menuItemID"))
#         quantity = int(data.get("quantitySold"))

#         # Fetch price and costOfFood % from MenuItems
#         query = "SELECT price, costOfFood FROM MenuItems WHERE menuItemID = %s;"
#         result = db.query(dbConnection, query, (menu_item_id,)).fetchone()
#         price = float(result["price"])
#         cost_pct = 0.2 if result["costOfFood"] == "20%" else 0.5

#         # Calculate totals
#         total_revenue = round(price * quantity, 2)
#         total_cost = round(total_revenue * cost_pct, 2)
#         total_profit = round(total_revenue - total_cost, 2)

#         # Insert sale
#         insert_query = """
#             INSERT INTO Sales (menuItemID, totalRevenue, totalCost, totalProfit, quantitySold)
#             VALUES (%s, %s, %s, %s, %s);
#         """
#         values = (menu_item_id, total_revenue, total_cost, total_profit, quantity)
#         db.query(dbConnection, insert_query, values)
#         dbConnection.commit()

#         return redirect("/sales")
#     except Exception as e:
#         print(f"Error creating sale: {e}")
#         return "Failed to create sale", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # UPDATE: Modify a sale
# @app.route("/update-sale", methods=["POST"])
# def update_sale():
#     try:
#         dbConnection = db.connectDB()
#         data = request.form

#         sale_id = int(data.get("saleID"))
#         new_quantity = int(data.get("quantitySold"))

#         # Get menuItemID from sale
#         sale_query = "SELECT menuItemID FROM Sales WHERE saleID = %s;"
#         menu_item_id = db.query(dbConnection, sale_query, (sale_id,)).fetchone()["menuItemID"]

#         # Fetch price and cost from MenuItems
#         item_query = "SELECT price, costOfFood FROM MenuItems WHERE menuItemID = %s;"
#         item = db.query(dbConnection, item_query, (menu_item_id,)).fetchone()
#         price = float(item["price"])
#         cost_pct = 0.2 if item["costOfFood"] == "20%" else 0.5

#         # Recalculate
#         total_revenue = round(price * new_quantity, 2)
#         total_cost = round(total_revenue * cost_pct, 2)
#         total_profit = round(total_revenue - total_cost, 2)

#         update_query = """
#             UPDATE Sales
#             SET quantitySold = %s,
#                 totalRevenue = %s,
#                 totalCost = %s,
#                 totalProfit = %s
#             WHERE saleID = %s;
#         """
#         values = (new_quantity, total_revenue, total_cost, total_profit, sale_id)
#         db.query(dbConnection, update_query, values)
#         dbConnection.commit()

#         return redirect("/sales")
#     except Exception as e:
#         print(f"Error updating sale: {e}")
#         return "Failed to update sale", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# # DELETE: Remove a sale
# @app.route("/delete-sale", methods=["POST"])
# def delete_sale():
#     try:
#         dbConnection = db.connectDB()
#         sale_id = request.form.get("saleID")
#         query = "DELETE FROM Sales WHERE saleID = %s;"
#         db.query(dbConnection, query, (sale_id,))
#         dbConnection.commit()
#         return redirect("/sales")
#     except Exception as e:
#         print(f"Error deleting sale: {e}")
#         return "Failed to delete sale", 500
#     finally:
#         if "dbConnection" in locals() and dbConnection:
#             dbConnection.close()

# RESET ALL TABLES
@app.route("/reset-all", methods=["POST"])
def reset_all():
    try:
        dbConnection = db.connectDB()

        # Delete from child-to-parent order
        db.query(dbConnection, "DELETE FROM OrderDetails;")
        db.query(dbConnection, "DELETE FROM Sales;")
        db.query(dbConnection, "DELETE FROM Orders;")
        db.query(dbConnection, "DELETE FROM MenuItems;")
        db.query(dbConnection, "DELETE FROM Customers;")

        # Insert default data
        db.query(dbConnection, """
            INSERT INTO Customers (customerID, firstName, lastName, email, marketingOptOut, customerType, visitCount)
            VALUES 
                (1, 'Jane', 'Doe', 'jdoe@hello.com', 1, 'New', 1),
                (2, 'Mike', 'Roberts', NULL, 0, 'Returning', 5),
                (3, 'Emily', 'King', 'eking@hello.com', 1, 'Returning', 2);
        """)

        db.query(dbConnection, """
            INSERT INTO MenuItems (menuItemID, itemName, description, price, costOfFood)
            VALUES 
                (1, 'Fried Egg Rolls', 'Crispy fried veggie egg rolls', 7.99, '20%%'),
                (2, 'Vietnamese Iced Coffee', 'Traditional phin drip coffee with condensed milk', 5.00, '20%%'),
                (3, 'Combo Pho', 'Traditional beef bone noodle soup with 4 meats', 16.99, '50%%'),
                (4, 'Tofu Vermicelli Bowl', 'Lemongrass grilled tofu with herbs and noodles', 14.99, '50%%');
        """)

        db.query(dbConnection, """
            INSERT INTO Orders (orderID, customerID, timestamp, totalAmount)
            VALUES 
                (1, 1, '2025-05-01 12:00:00', 16.99),
                (2, 2, '2025-05-02 13:30:00', 5.00),
                (3, 3, '2025-05-03 14:45:00', 34.98);
        """)

        db.query(dbConnection, """
            INSERT INTO OrderDetails (orderID, menuItemID, quantityMenuItem)
            VALUES 
                (2, 4, 2),
                (1, 3, 1),
                (3, 4, 1),
                (3, 2, 1);
        """)

        db.query(dbConnection, """
            INSERT INTO Sales (saleID, menuItemID, totalRevenue, totalCost, totalProfit, quantitySold)
            VALUES 
                (1, 2, 1090.00, 218.00, 872.00, 218),
                (2, 3, 3398.00, 1699.00, 1699.00, 200),
                (3, 4, 2268.00, 453.60, 1814.40, 189);
        """)

        dbConnection.commit()
        return redirect("/")  # ✅ Redirect to home page
    except Exception as e:
        print(f"Error resetting all tables: {e}")
        return "Failed to reset all tables", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# LISTENER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1027, debug=True)
