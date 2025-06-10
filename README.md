# SQLurp the Pho
CS340 Project Group 21 - SQLurp the Pho
Lorine Kaye Mijares and Annabel Vu

This is a Flask-based web application submitted as a requirement for CS340 that connects to a MySQL database and displays tables such as `Customers`, `Orders`, `MenuItems`, `Sales`, and `OrderDetails` in a simple UI. To use the web app, users need to input their login details in the db_connector.py file. Users can browse data and perform basic CRUD operations on the Menu Items page and the Order Details page.

## Citations

### app.py
Citation for the code in app.py (all routes):
Date: 6/5/2025
All code for routes based on the the starter code in Module 8, Exploration "Implementing CUD operations in your app" 
Source URl: https://canvas.oregonstate.edu/courses/1999601/pages/exploration-implementing-cud-operations-in-your-app?module_item_id=25352968

Citation for use of AI Tools on app.py:
Date: 6/5/2025
Summary of prompts used on app.py
AI used to troubleshoot errors in routes for Order Details causing blank dropdown menus on the add and update forms,
duplication of IDs in the dropdown menus, and newly-added Order Details resetting the display table upon submitting the Add form
AI Source URL: https://chatgpt.com

### DDL.sql
Citation for the code below (May 21 2025):
Code based on the the starter code in Module 8, Exploration "Implementing CUD operations in your app" 
Source URl: https://canvas.oregonstate.edu/courses/1999601/pages/exploration-implementing-cud-operations-in-your-app?module_item_id=25352968

### plsql.sql
Citation for the code below (May 21 2025):
All code for SPs based on the the starter code in Module 8, Exploration "Implementing CUD operations in your app" 
Source URl: https://canvas.oregonstate.edu/courses/1999601/pages/exploration-implementing-cud-operations-in-your-app?module_item_id=25352968

Citation for use of AI Tools:
Date: 6/5/2025
Summary of prompts used on PL for stored procedures
ChatGPT used to troubleshoot errors on OrderDetails SPs, to raise an error when adding an existing OrderDetail
and when updating a nonexistent OrderDetail. Also used to troubleshoot an error on OrderDetails page when a MenuItem currently in use is deleted.
AI Source URL: https://chatgpt.com

### template files
Citation for the code below:
Date: 6/9/2025
All code for jinja files based on the starter code in Module 6, Exploration "Web Application Technology"
Source URl: https://canvas.oregonstate.edu/courses/1999601/pages/exploration-web-application-technology-2?module_item_id=25352948