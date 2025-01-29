import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Создание базы данных
def init_db():
    conn = sqlite3.connect('business_orders.db')  # Подключение к базе
    cur = conn.cursor()  # Создание курсора
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_tel TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Добавление заказа в базу
def add_order():
    customer_name = customer_name_entry.get()
    customer_tel = customer_tel_entry.get()
    order_details = order_details_entry.get()

    if customer_name and order_details and customer_tel:
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (customer_name, customer_tel, order_details, status) VALUES (?, ?, ?, ?)",
            (customer_name, customer_tel, order_details, 'Новый'))
        conn.commit()
        conn.close()

        customer_name_entry.delete(0, tk.END)  # Очищаем поля ввода
        order_details_entry.delete(0, tk.END)
        customer_tel_entry.delete(0, tk.END)

        view_orders()
    else:
        messagebox.showwarning("Ошибка", "Заполните все поля!")

# Отображение заказов в таблице
def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)  # Вставляем ряд в конец таблицы

    conn.close()

# Завершение заказа
def complete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")

# Удаление заказа
def delete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для удаления")

# Редактирование заказа
def edit_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        customer_name = tree.item(selected_item, 'values')[1]
        customer_tel = tree.item(selected_item, 'values')[2]
        order_details = tree.item(selected_item, 'values')[3]

        # Окно редактирования
        edit_window = tk.Toplevel(app)
        edit_window.title("Редактирование заказа")
        edit_window.configure(background="DarkSeaGreen1")

        tk.Label(edit_window, text="Имя клиента:", bg="DarkSeaGreen1", font=("Cambria", 12)).pack(pady=5)
        edit_customer_name_entry = tk.Entry(edit_window, width=40, bg="cornsilk")
        edit_customer_name_entry.insert(0, customer_name)
        edit_customer_name_entry.pack(pady=5)

        tk.Label(edit_window, text="Телефон клиента:", bg="DarkSeaGreen1", font=("Cambria", 12)).pack(pady=5)
        edit_customer_tel_entry = tk.Entry(edit_window, width=40, bg="cornsilk")
        edit_customer_tel_entry.insert(0, customer_tel)
        edit_customer_tel_entry.pack(pady=5)

        tk.Label(edit_window, text="Детали заказа:", bg="DarkSeaGreen1", font=("Cambria", 12)).pack(pady=5)
        edit_order_details_entry = tk.Entry(edit_window, width=40, bg="cornsilk")
        edit_order_details_entry.insert(0, order_details)
        edit_order_details_entry.pack(pady=5)

        def save_changes():
            new_customer_name = edit_customer_name_entry.get()
            customer_tel = edit_customer_tel_entry.get()
            new_order_details = edit_order_details_entry.get()

            if new_customer_name and new_order_details:
                conn = sqlite3.connect('business_orders.db')
                cur = conn.cursor()
                cur.execute(
                    "UPDATE orders SET customer_name=?, customer_tel=?,order_details=? WHERE id=?",
                    (new_customer_name, customer_tel, new_order_details, order_id))
                conn.commit()
                conn.close()
                view_orders()
                edit_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля!")

        save_button = tk.Button(edit_window, text="Сохранить", bg="dark salmon", fg="white",
                                font=("Arial Black", 12), command=save_changes)
        save_button.pack(pady=10)
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для редактирования")

# Отметить заказ "В работе"
def mark_in_progress():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='В работе' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для отметки")

# Основное окно приложения
app = tk.Tk()
app.title("Система управления заказами")
app.configure(background="DarkSeaGreen1")
app.geometry('1000x800')

# Поля ввода
tk.Label(app, text="Имя клиента:", bg="DarkSeaGreen1", font=("Cambria", 18)).pack(pady=5)
customer_name_entry = tk.Entry(app, width=40, bg="cornsilk")
customer_name_entry.pack(pady=5)

tk.Label(app, text="Телефон клиента:", bg="DarkSeaGreen1", font=("Cambria", 18)).pack(pady=5)
customer_tel_entry = tk.Entry(app, width=40, bg="cornsilk")
customer_tel_entry.pack(pady=5)

tk.Label(app, text="Детали заказа:", bg="DarkSeaGreen1", font=("Cambria", 18)).pack(pady=5)
order_details_entry = tk.Entry(app, width=40, bg="cornsilk")
order_details_entry.pack(pady=5)

# Кнопки для добавления, редактирования, удаления и завершения заказа
button_frame = tk.Frame(app, bg="DarkSeaGreen1")
button_frame.pack(pady=15)

# Размещение кнопок в одном ряду
add_button = tk.Button(button_frame, text="Добавить заказ", bg="light blue", font=("Cambria", 16), command=add_order)
add_button.grid(row=0, column=0, padx=10)

edit_button = tk.Button(button_frame, text="Редактировать заказ", bg="light blue",  font=("Cambria", 16), command=edit_order)
edit_button.grid(row=0, column=1, padx=10)

complete_button = tk.Button(button_frame, text="Завершить заказ", bg="light blue",  font=("Cambria", 16), command=complete_order)
complete_button.grid(row=0, column=2, padx=10)

delete_button = tk.Button(button_frame, text="Удалить заказ", bg="light blue",  font=("Cambria", 16), command=delete_order)
delete_button.grid(row=0, column=3, padx=10)

in_progress_button = tk.Button(button_frame, text="В работе", bg="light blue",  font=("Cambria", 16), command=mark_in_progress)
in_progress_button.grid(row=0, column=4, padx=10)

style = ttk.Style()
style.theme_use("default")  # Установить стандартную тему

# Настройка заголовков столбцов
style.configure("Treeview.Heading", font=("Cambria", 17), foreground="black")
style.map("Treeview.Heading", background=[("active", "light blue"), ("!active", "cornsilk")])

# Настройка строк таблицы
style.configure("Treeview", font=("Cambria", 15), rowheight=30)


# Таблица для отображения заказов
columns = ("ID", "Имя клиента", "Телефон клиента", "Детали заказа", "Статус")
tree = ttk.Treeview(app, columns=columns, show="headings", height=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(pady=15)

# Инициализация базы данных
init_db()

# Отображение заказов
view_orders()

# Запуск приложения
app.mainloop()
