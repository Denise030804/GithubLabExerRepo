import flet as ft
import sqlite3
import bcrypt
from login import create_login_page
from register import create_register_page
from mainpage import create_main_page
from adminpage import create_admin_page
from usersprofile import create_user_profile_page
from alarms import create_alarm_page

def main(page: ft.Page):
    page.title = "MemoryMentor"

    def route_change(route):
        page.views.clear()
        if page.route == "/" or page.route == "/login":
            page.views.append(create_login_page(page))
        elif page.route == "/register":
            page.views.append(create_register_page(page))
        elif page.route == "/main":
            page.views.append(create_main_page(page))
        elif page.route == "/admin":
            page.views.append(create_admin_page(page))
        elif page.route == "/profile":
            username = page.client_storage.get("username")
            if username:
                page.views.append(create_user_profile_page(page, username))
            else:
                page.go("/login")
        elif page.route == "/alarms":
            username = page.client_storage.get("username")
            if username:
                page.views.append(create_alarm_page(page, username))
            else:
                page.go("/login")
        page.update()

    page.on_route_change = route_change


    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER,
              full_name TEXT, age INTEGER, location TEXT)''')
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                  ("admin", hashed_password, 1, "Admin User", 0, "System"))
        print("Admin user created. Username: admin, Password: admin123")
    conn.commit()
    conn.close()


    conn = sqlite3.connect('alarms.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alarms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  time TEXT,
                  medication TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    conn.commit()
    conn.close()

    page.go("/login")

ft.app(target=main)
