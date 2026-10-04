'''
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------------- MYSQL CONNECTION ----------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="S@rvesh2702",
    database="SPORTS_CLUB"
)

cursor = db.cursor()


# ---------------- TABLE DETAILS ----------------

tables = {
    "COACH": [
        "COACH_ID", "COACH_NAME", "SPORT", "EXPERIENCE"
    ],

    "TEAM": [
        "TEAM_ID", "TEAM_NAME", "SPORT", "COACH_ID"
    ],

    "PLAYER": [
        "PLAYER_ID", "PLAYER_NAME", "AGE",
        "GENDER", "CONTACT", "TEAM_ID"
    ],

    "MATCHES": [
        "MATCH_ID", "TEAM_ID", "OPPONENT",
        "MATCH_DATE", "VENUE", "RESULT"
    ],

    "MEMBERSHIP": [
        "MEMBERSHIP_ID", "PLAYER_ID", "MEMBERSHIP_TYPE",
        "START_DATE", "END_DATE", "FEE"
    ],

    "PAYMENT": [
        "PAYMENT_ID", "MEMBERSHIP_ID", "TOTAL_FEE",
        "PAID", "BALANCE", "LAST_PAYMENT_DATE",
        "PAYMENT_STATUS"
    ]
}


# ---------------- MAIN WINDOW ----------------

window = tk.Tk()
window.title("Sports Club Management System")
window.geometry("1000x650")


title = tk.Label(
    window,
    text="SPORTS CLUB MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)


# ---------------- TABLE SELECTION ----------------

tk.Label(
    window,
    text="Select Table:",
    font=("Arial", 12)
).pack()

table_box = ttk.Combobox(
    window,
    values=list(tables.keys()),
    state="readonly",
    width=30
)

table_box.pack(pady=5)


# ---------------- INPUT AREA ----------------

input_frame = tk.Frame(window)
input_frame.pack(pady=15)

entries = {}


def create_fields():

    # Remove old fields
    for widget in input_frame.winfo_children():
        widget.destroy()

    entries.clear()

    selected_table = table_box.get()

    if selected_table == "":
        return

    columns = tables[selected_table]

    for i, column in enumerate(columns):

        label = tk.Label(
            input_frame,
            text=column,
            font=("Arial", 11)
        )

        label.grid(row=i, column=0, padx=10, pady=5)

        entry = tk.Entry(
            input_frame,
            width=30
        )

        entry.grid(row=i, column=1, padx=10, pady=5)

        entries[column] = entry


table_box.bind("<<ComboboxSelected>>", lambda event: create_fields())


# ---------------- VIEW DATA ----------------

def view_data():

    selected_table = table_box.get()

    if selected_table == "":
        messagebox.showwarning(
            "Warning",
            "Please select a table."
        )
        return

    try:
        query = "SELECT * FROM " + selected_table

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = tables[selected_table]

        # Clear old data
        for item in data_table.get_children():
            data_table.delete(item)

        data_table["columns"] = columns

        for column in columns:
            data_table.heading(column, text=column)
            data_table.column(column, width=120)

        for row in rows:
            data_table.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- INSERT DATA ----------------

def insert_data():

    selected_table = table_box.get()

    if selected_table == "":
        messagebox.showwarning(
            "Warning",
            "Please select a table."
        )
        return

    columns = tables[selected_table]

    values = []

    for column in columns:
        values.append(entries[column].get())

    try:

        placeholders = ", ".join(["%s"] * len(columns))

        query = (
            "INSERT INTO "
            + selected_table
            + " ("
            + ", ".join(columns)
            + ") VALUES ("
            + placeholders
            + ")"
        )

        cursor.execute(query, values)

        db.commit()

        messagebox.showinfo(
            "Success",
            "Record inserted successfully."
        )

        clear_fields()
        view_data()

    except Exception as e:

        db.rollback()

        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------- UPDATE DATA ----------------

def update_data():

    selected_table = table_box.get()

    if selected_table == "":
        messagebox.showwarning(
            "Warning",
            "Please select a table."
        )
        return

    columns = tables[selected_table]

    primary_key = columns[0]

    primary_value = entries[primary_key].get()

    if primary_value == "":
        messagebox.showwarning(
            "Warning",
            "Enter the Primary Key."
        )
        return

    set_values = []

    values = []

    for column in columns[1:]:

        set_values.append(column + " = %s")
        values.append(entries[column].get())

    values.append(primary_value)

    query = (
        "UPDATE "
        + selected_table
        + " SET "
        + ", ".join(set_values)
        + " WHERE "
        + primary_key
        + " = %s"
    )

    try:

        cursor.execute(query, values)

        db.commit()

        if cursor.rowcount > 0:

            messagebox.showinfo(
                "Success",
                "Record updated successfully."
            )

        else:

            messagebox.showwarning(
                "Warning",
                "Record not found."
            )

        view_data()

    except Exception as e:

        db.rollback()

        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------- DELETE DATA ----------------

def delete_data():

    selected_table = table_box.get()

    if selected_table == "":
        messagebox.showwarning(
            "Warning",
            "Please select a table."
        )
        return

    columns = tables[selected_table]

    primary_key = columns[0]

    primary_value = entries[primary_key].get()

    if primary_value == "":
        messagebox.showwarning(
            "Warning",
            "Enter the Primary Key."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this record?"
    )

    if not confirm:
        return

    query = (
        "DELETE FROM "
        + selected_table
        + " WHERE "
        + primary_key
        + " = %s"
    )

    try:

        cursor.execute(
            query,
            (primary_value,)
        )

        db.commit()

        if cursor.rowcount > 0:

            messagebox.showinfo(
                "Success",
                "Record deleted successfully."
            )

        else:

            messagebox.showwarning(
                "Warning",
                "Record not found."
            )

        clear_fields()
        view_data()

    except Exception as e:

        db.rollback()

        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------- CLEAR FIELDS ----------------

def clear_fields():

    for entry in entries.values():
        entry.delete(0, tk.END)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="INSERT",
    width=12,
    command=insert_data
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="UPDATE",
    width=12,
    command=update_data
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="DELETE",
    width=12,
    command=delete_data
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="VIEW",
    width=12,
    command=view_data
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="CLEAR",
    width=12,
    command=clear_fields
).grid(row=0, column=4, padx=5)


# ---------------- DATA TABLE ----------------

data_frame = tk.Frame(window)
data_frame.pack(fill="both", expand=True, padx=10, pady=10)

data_table = ttk.Treeview(
    data_frame,
    show="headings"
)

data_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar = ttk.Scrollbar(
    data_frame,
    orient="vertical",
    command=data_table.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

data_table.configure(
    yscrollcommand=scrollbar.set
)


# ---------------- RUN APPLICATION ----------------

window.mainloop()
'''
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# MYSQL CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="S@rvesh2702",
    database="SPORTS_CLUB"
)
cursor = con.cursor()

# TABLE INFORMATION
table_data = {
    "COACH": {
        "columns": ["COACH_ID", "COACH_NAME", "SPORT", "EXPERIENCE"]
    },
    "TEAM": {
        "columns": ["TEAM_ID", "TEAM_NAME", "SPORT", "COACH_ID"]
    },
    "PLAYER": {
        "columns": ["PLAYER_ID", "PLAYER_NAME", "AGE","GENDER", "CONTACT", "TEAM_ID"]
    },
    "MATCHES": {
        "columns": ["MATCH_ID", "TEAM_ID", "OPPONENT",
                    "MATCH_DATE", "VENUE", "RESULT" ]
    },
    "MEMBERSHIP": {
        "columns": ["MEMBERSHIP_ID", "PLAYER_ID","MEMBERSHIP_TYPE",
                    "START_DATE","END_DATE", "FEE"]
    },
    "PAYMENT": {
        "columns": ["PAYMENT_ID", "MEMBERSHIP_ID","TOTAL_FEE",
                    "PAID", "BALANCE", "LAST_PAYMENT_DATE", "PAYMENT_STATUS"]
    }
}


# MAIN WINDOW
root = tk.Tk()
root.title("Sports Club Management System")
root.geometry("1000x700")
root.configure(bg="black")

# TITLE
title = tk.Label(
    root,
    text="SPORTS CLUB MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="grey"
)
title.pack(pady=15)


# NOTEBOOK
notebook = ttk.Notebook(root)
notebook.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

# CREATE TAB
tabs = {}
for table in table_data:
    tab = tk.Frame(notebook)
    notebook.add(tab, text=table)
    tabs[table] = tab

# CREATE GUI FOR EACH TABLE
widgets = {}
def create_table_gui(table):
    tab = tabs[table]
    columns = table_data[table]["columns"]
    widgets[table] = {}

    # FORM
    form = tk.Frame(tab)
    form.pack(pady=15)
    entries = {}
    for i, column in enumerate(columns):
        label = tk.Label(
            form,
            text=column,
            font=("Arial", 11))

        label.grid(
            row=i // 2,
            column=(i % 2) * 2,
            padx=10,
            pady=7,
            sticky="e")

        entry = tk.Entry(
            form,
            width=25)

        entry.grid(
            row=i // 2,
            column=(i % 2) * 2 + 1,
            padx=10,
            pady=7)

        entries[column] = entry
    widgets[table]["entries"] = entries

    # BUTTONS 

    button_frame = tk.Frame(tab)
    button_frame.pack(pady=10)
    tk.Button(
        button_frame,
        text="ADD",
        width=12,
        command=lambda: add_record(table)
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="UPDATE",
        width=12,
        command=lambda: update_record(table)
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="DELETE",
        width=12,
        command=lambda: delete_record(table)
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="CLEAR",
        width=12,
        command=lambda: clear_form(table)
    ).grid(row=0, column=3, padx=5)

    tk.Button(
        button_frame,
        text="REFRESH",
        width=12,
        command=lambda: load_data(table)
    ).grid(row=0, column=4, padx=5)

    # TREEVIEW 

    tree_frame = tk.Frame(tab)

    tree_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10)

    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings")

    for column in columns:

        tree.heading(
            column,
            text=column)

        tree.column(
            column,
            width=130)

    tree.pack(
        side="left",
        fill="both",
        expand=True)

    scrollbar = ttk.Scrollbar(
        tree_frame,
        orient="vertical",
        command=tree.yview)

    scrollbar.pack(
        side="right",
        fill="y")

    tree.configure(
        yscrollcommand=scrollbar.set)

    widgets[table]["tree"] = tree

    # Select record from table
    tree.bind(
        "<ButtonRelease-1>",
        lambda event: select_record(table))


#ADD RECORD

def add_record(table):
    columns = table_data[table]["columns"]
    entries = widgets[table]["entries"]
    values = []
    for column in columns:
        value = entries[column].get()
        if value == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return
        values.append(value)
    placeholders = ", ".join(["%s"] * len(columns))
    query = (
        "INSERT INTO "
        + table
        + " ("
        + ", ".join(columns)
        + ") VALUES ("
        + placeholders
        + ")"
    )
    try:

        cursor.execute(query, values)
        con.commit()
        messagebox.showinfo(
            "Success",
            "Record added successfully."
        )
        clear_form(table)
        load_data(table)
    except Exception as e:
        con.rollback()
        messagebox.showerror(
            "Error",
            str(e)
        )

# LOAD DATA
def load_data(table):
    tree = widgets[table]["tree"]
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute(
        "SELECT * FROM " + table
    )
    records = cursor.fetchall()
    for record in records:
        tree.insert(
            "",
            tk.END,
            values=record
        )

# SELECT RECORD
def select_record(table):
    tree = widgets[table]["tree"]
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(
        selected[0]
    )["values"]
    columns = table_data[table]["columns"]
    entries = widgets[table]["entries"]
    for i, column in enumerate(columns):
        entries[column].delete(
            0,
            tk.END)
        entries[column].insert(
            0,
            values[i])

# UPDATE RECORD
def update_record(table):
    columns = table_data[table]["columns"]
    entries = widgets[table]["entries"]
    primary_key = columns[0]
    primary_value = entries[primary_key].get()
    if primary_value == "":
        messagebox.showwarning(
            "Warning",
            "Enter or select the Primary Key."
        )
        return
    set_values = []
    values = []
    for column in columns[1:]:
        set_values.append(
            column + " = %s"
        )
        values.append(
            entries[column].get()
        )
    values.append(primary_value)
    query = (
        "UPDATE "
        + table
        + " SET "
        + ", ".join(set_values)
        + " WHERE "
        + primary_key
        + " = %s"
    )
    try:
        cursor.execute(
            query,
            values
        )
        con.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Record updated successfully."
            )
        else:
            messagebox.showwarning(
                "Warning",
                "Record not found."
            )
        load_data(table)
    except Exception as e:
        con.rollback()
        messagebox.showerror(
            "Error",
            str(e)
        )


# DELETE RECORD
def delete_record(table):
    columns = table_data[table]["columns"]
    entries = widgets[table]["entries"]
    primary_key = columns[0]
    primary_value = entries[primary_key].get()
    if primary_value == "":
        messagebox.showwarning(
            "Warning",
            "Select a record first."
        )
        return
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Do you want to delete this record?"
    )
    if not confirm:
        return
    query = (
        "DELETE FROM "
        + table
        + " WHERE "
        + primary_key
        + " = %s"
    )
    try:
        cursor.execute(
            query,
            (primary_value,)
        )
        con.commit()
        messagebox.showinfo(
            "Success",
            "Record deleted successfully."
        )
        clear_form(table)
        load_data(table)
    except Exception as e:
        con.rollback()
        messagebox.showerror(
            "Error",
            str(e)
        )

# CLEAR FORM
def clear_form(table):
    entries = widgets[table]["entries"]
    for entry in entries.values():
        entry.delete(
            0,
            tk.END
        )

# CREATE ALL TABS
for table in table_data:
    create_table_gui(table)

# LOAD ALL DATA
for table in table_data:
    load_data(table)


# RUN APPLICATION
root.mainloop()

