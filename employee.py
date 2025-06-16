import tkinter as tk
import sqlite3
from tkinter import Scrollbar, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

database = "employees.db"

root = tk.Tk()
root.title("Employee Management")
root.geometry("1366x768+50+50")
root.resizable(False, False)
root.configure(bg="cyan")


def create_table():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            ID INTEGER PRIMARY KEY ,
            Name TEXT NOT NULL,
            WorkMail TEXT NOT NULL,
            PHONE INTEGER NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


def add_employee():
    name = entry_name.get()
    workmail = entry_workmail.get()
    PHONE = entry_phone.get()

    # name ve workmail girili ise işlemi gerçekleştir
    if name and workmail and PHONE:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        sql_query = (
            "INSERT OR IGNORE INTO employees (Name, WorkMail, PHONE) VALUES (?, ?, ?)"
        )
        values = (name, workmail, PHONE)

        cursor.execute(sql_query, values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Mesaj", "Çalışan eklendi!")
    else:
        messagebox.showwarning(
            "Uyarı!!!!!!", "İsim,Work mail veya Phone boş olamaz!!!!"
        )


def update_employee():
    selected_id = entry_id.get()
    name = entry_name.get()
    workmail = entry_workmail.get()
    PHONE = entry_phone.get()

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE employees SET Name = ?, WorkMail = ?, PHONE = ? WHERE ID = ?",
        (name, workmail, PHONE, selected_id),
    )
    messagebox.showwarning("Mesaj", "Çalışan bilgisi güncellendi!")
    conn.commit()
    conn.close()


def delete_employee():
    selected_id = entry_id.get()

    if selected_id.strip() == "":
        messagebox.showwarning("Uyarı", "Lütfen silinecek çalışanın ID'sini girin!")
        return

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE ID = ?", (selected_id,))
    messagebox.showwarning("Mesaj", "Çalışan silindi!")

    conn.commit()
    conn.close()


def show_employees():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    employee_list.delete(0, tk.END)
    for employee in employees:
        employee_list.insert(
            tk.END,
            f"ID: {employee[0]}, Name: {employee[1]}, WorkMail: {employee[2]}, Phone: {employee[3]}",
        )

    conn.close()


def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_workmail.delete(0, tk.END)
    entry_phone.delete(0, tk.END)


create_table()

label_id = tk.Label(root, text="ID:")
label_id.grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

label_name = tk.Label(root, text="Name:")
label_name.grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

label_workmail = tk.Label(root, text="WorkMail:")
label_workmail.grid(row=2, column=0, padx=10, pady=5)
entry_workmail = tk.Entry(root)
entry_workmail.grid(row=2, column=1, padx=10, pady=5)

label_phone = tk.Label(root, text="Phone Number:")
label_phone.grid(row=3, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=3, column=1, padx=10, pady=5)

button_add = tk.Button(root, text="Add Employee", command=add_employee)
button_add.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

button_update = tk.Button(root, text="Update Employee", command=update_employee)
button_update.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

button_delete = tk.Button(root, text="Delete Employee", command=delete_employee)
button_delete.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

button_show = tk.Button(root, text="Show Employees", command=show_employees)
button_show.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

button_clear = tk.Button(root, text="Clear Entries", command=clear_entries)
button_clear.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

employee_list = tk.Listbox(root, width=65)
employee_list.grid(row=0, column=2, rowspan=9, padx=10, pady=10)

scrollbar = tk.Scrollbar(root, orient="vertical")
scrollbar.grid(row=0, column=3, rowspan=9, sticky="ns")

employee_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=employee_list.yview)

root.mainloop()

## BUG REPORT
# Editleme yapar iken numara boş olursa numarayı siliyor(bug mı normal mi anlamadım)
# Arka plana hangi kod eklenirse eklensin resim ya farklı pencerede açılıyor yada butonları görmezden gelip sadece resim açılıyor
# Scrollbar hata veriyor sebebini anlamadım (FIXED)
# Scrollbar konumlandırılmasında sorun var sağ sola ilerliyor yukarı aşağı konumlanmıyor
