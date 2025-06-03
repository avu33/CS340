# ########################################
# ########## SETUP
PORT = 10233
from flask import Flask, render_template, request, redirect
import database.db_connector as db  

PORT = 10233
app = Flask(__name__)

# home page
@app.route("/", methods=["GET"])
def home():
    try:
        return render_template("home.j2")
    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500


# READ customers
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


# READ orders
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


# READ order details
@app.route('/order-details', methods=["GET", "POST"])
def order_details():
    results, orders, menu_items = [], [], []

    try:
        dbConnection = db.connectDB()
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

    except Exception as e:
        print("Error fetching order details:", e)
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

    return render_template(
        "order_details.j2",
        order_details=results,
        orders=orders,
        menu_items=menu_items
    )


# READ menu items
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


# CREATE menu item
@app.route("/create-menu-item", methods=["POST"])
def create_menu_item():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        item_name = request.form["itemName"]
        item_price = request.form["itemPrice"]
        item_description = request.form["itemDescription"]
        item_costOfFood = request.form["itemcostOfFood"]

        cursor.execute("SET @new_id = 0;")
        cursor.execute("CALL sp_CreateMenuItem(%s, %s, %s, %s, @new_id);", 
                    (item_name, item_description, item_price, item_costOfFood))
        cursor.execute("SELECT @new_id;")
        new_id = cursor.fetchone()[0]

        dbConnection.commit()
        print(f"Created menu item '{item_name}' with ID {new_id}")
        return redirect("/menu-items")
    
    except Exception as e:
        print(f"Error creating menu item: {e}")
        return "Failed to create menu item", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# UPDATE menu item
@app.route("/update-menu-item", methods=["POST"])
def update_menu_item():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        item_id = request.form["menuItemID"]
        item_price = request.form["itemPrice"]
        item_costOfFood = request.form["itemcostOfFood"]

        query = "CALL sp_UpdateMenuItem(%s, %s, %s);"
        cursor.execute(query, (item_id, item_price, item_costOfFood))

        dbConnection.commit()
        print(f"Updated menu item ID {item_id}")
        return redirect("/menu-items")
    except Exception as e:
        print(f"Error updating menu item: {e}")
        return "Failed to update menu item", 500
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# DELETE menu item
@app.route("/delete-menu-item", methods=["POST"])
def delete_menu_item():
    print("Route /delete-menu-item was hit!")  # DEBUG LINE

    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        item_id = request.form["menuItemID"]
        item_name = request.form["itemName"]

        query = "CALL sp_DeleteMenuItem(%s)";
        cursor.execute(query, (item_id,))
        dbConnection.commit()
        print(f"Deleted menu item: {item_name} (ID: {item_id})")

        return redirect("/menu-items")
    
    except Exception as e:
        print(f"Error deleting menu item: {e}")
        return "Failed to delete menu item", 500
    
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# READ Sales Page
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

# RESET db
@app.route("/reset-db", methods=["POST"])
def reset_db():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        cursor.callproc("sp_reset_PHOdatabase")
        dbConnection.commit()
        print("Database reset successfully.")

        return redirect(request.referrer)
    
    except Exception as e:
        print(f"Error resetting database: {e}")
        return "Failed to reset database", 500
    
    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# LISTENER
if __name__ == "__main__":
    import os
    os.environ['FLASK_ENV'] = 'development'
    app.run(host="0.0.0.0", port=10233, debug=True)
