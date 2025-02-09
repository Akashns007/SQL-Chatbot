# import sqlite3

# file = "sqlite.db"

# try:
#     conn = sqlite3.connect(file)
#     print("Opened database successfully")
# except:
#     print("Error creating database")

# def create_table():
    
#     cursor_obj = conn.cursor()

#     # Drop tables if they exist
#     cursor_obj.execute("DROP TABLE IF EXISTS Employees")
#     cursor_obj.execute("DROP TABLE IF EXISTS Departments")

#     # Create Employees Table
#     employees_table = """ 
#     CREATE TABLE Employees (
#         Id INTEGER PRIMARY KEY NOT NULL,
#         Name TEXT NOT NULL,
#         Department TEXT NOT NULL,
#         Salary INTEGER NOT NULL,
#         Hire_Date DATE NOT NULL
#     );
#     """

#     # Create Departments Table with Correct Foreign Key
#     departments_table = """ 
#     CREATE TABLE Departments (
#         Id INTEGER PRIMARY KEY NOT NULL,
#         Name TEXT NOT NULL,
#         Manager INTEGER NOT NULL,
#         FOREIGN KEY (Manager) REFERENCES Employees(Name) ON DELETE SET NULL
#     );
#     """

#     # Execute Table Creations
#     cursor_obj.execute(employees_table)
#     cursor_obj.execute(departments_table)

#     print("Tables are Ready")


# def insert_data():
#     cursor_obj = conn.cursor()
    
#     # Insert Employees  
#     cursor_obj.executemany(
#         "INSERT INTO Employees (Id, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)",
#         [
#             (1, "Alice", "Sales", 50000, "2021-01-15"),
#             (2, "Bob", "Engineering", 70000, "2020-06-10"),
#             (3, "Charlie", "Marketing", 60000, "2022-03-20"),
#         ],
#     )

#     # Insert Department Data (Manager references Employee ID)
#     cursor_obj.executemany(
#         "INSERT INTO Departments (Id, Name, Manager) VALUES (?, ?, ?)",
#         [
#             (1, "Sales", "Alice"),
#             (2, "Engineering", "Bob"),
#             (3, "Marketing", "Charlie"),
#         ],
#     )
    
import sqlite3
import random
from datetime import datetime, timedelta

file = "sqlite_large.db"

def create_connection():
    try:
        conn = sqlite3.connect(file)
        print("Opened database successfully")
        return conn
    except Exception as e:
        print("Error creating database:", e)
        return None


def create_table(conn):
    cursor_obj = conn.cursor()

    # Drop tables if they exist
    cursor_obj.execute("DROP TABLE IF EXISTS Employees")
    cursor_obj.execute("DROP TABLE IF EXISTS Departments")

    # Create Employees Table
    employees_table = """ 
    CREATE TABLE Employees (
        Id INTEGER PRIMARY KEY NOT NULL,
        Name TEXT UNIQUE NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date DATE NOT NULL
    );
    """

    # Create Departments Table with Name as Foreign Key
    departments_table = """ 
    CREATE TABLE Departments (
        Id INTEGER PRIMARY KEY NOT NULL,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL,
        FOREIGN KEY (Manager) REFERENCES Employees(Name) ON DELETE SET NULL
    );
    """

    # Execute Table Creations
    cursor_obj.execute(employees_table)
    cursor_obj.execute(departments_table)

    print("Tables are Ready")


def insert_data(conn):
    cursor_obj = conn.cursor()

    # Sample data for names and departments
    employee_names = [
        f"Employee{i}" for i in range(1, 1001)
    ]
    departments = ["Sales", "Engineering", "Marketing", "Finance", "HR"]
    
    # Generate random employee records
    employees = []
    for i, name in enumerate(employee_names, start=1):
        department = random.choice(departments)
        salary = random.randint(40000, 150000)
        hire_date = (datetime.now() - timedelta(days=random.randint(30, 3000))).strftime("%Y-%m-%d")
        employees.append((i, name, department, salary, hire_date))

    # Insert Employees
    cursor_obj.executemany(
        "INSERT INTO Employees (Id, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)",
        employees,
    )

    # Generate department data with random managers
    department_data = [
        (i, dept, random.choice(employee_names)) for i, dept in enumerate(departments, start=1)
    ]

    # Insert Departments
    cursor_obj.executemany(
        "INSERT INTO Departments (Id, Name, Manager) VALUES (?, ?, ?)",
        department_data,
    )

    conn.commit()
    print("Data inserted successfully")


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_table(conn)
        insert_data(conn)
        conn.close()

# if __name__ == "__main__":
#     create_table()
#     insert_data()    
#     print("Tables and data inserted successfully")
#     conn.commit()
    
