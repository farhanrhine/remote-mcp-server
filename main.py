from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db") # create the database file in the same directory as this script to store expenses
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

# Initialize the database and create the expenses table if it doesn't exist
# its a sql query to create a table with columns: id, date, amount, category, subcategory, note
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
# Call the init_db function to ensure the database and table are set up
init_db()

# Define MCP tools for adding and listing expenses
@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid} # return the id of the newly added expense

# show all expenses between start_date and end_date   
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    

# Define MCP tool for deleting, editing, and crediting expenses
@mcp.tool()
def delete_expense(expense_id: int):
    '''Delete an expense entry by its ID.'''
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        return {"status": "deleted", "id": expense_id}
    
@mcp.tool()
def edit_expense(expense_id: int, date: str = None, amount: float = None, category: str = None, subcategory: str = None, note: str = None): # type: ignore
    '''Edit an existing expense entry. Only provided fields will be updated.'''
    fields = []
    params = []

    if date is not None:
        fields.append("date = ?")
        params.append(date)
    if amount is not None:
        fields.append("amount = ?")
        params.append(amount)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if subcategory is not None:
        fields.append("subcategory = ?")
        params.append(subcategory)
    if note is not None:
        fields.append("note = ?")
        params.append(note)

    params.append(expense_id)

    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?",
            params
        )
        return {"status": "updated", "id": expense_id}
    
@mcp.tool()
def credit_expense(expense_id: int, amount: float):
    '''Credit (reduce) an expense entry by its ID.'''
    with sqlite3.connect(DB_PATH) as c:
        # First, get the current amount
        cur = c.execute(
            "SELECT amount FROM expenses WHERE id = ?",
            (expense_id,)
        )
        row = cur.fetchone()
        if row is None:
            return {"status": "error", "message": "Expense not found"}

        current_amount = row[0]
        new_amount = current_amount - amount

        # Update the expense with the new amount
        c.execute(
            "UPDATE expenses SET amount = ? WHERE id = ?",
            (new_amount, expense_id)
        )
        return {"status": "credited", "id": expense_id, "new_amount": new_amount}
    


# ...existing code...

# add resource for categories.json 
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()