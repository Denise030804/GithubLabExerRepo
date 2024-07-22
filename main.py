import flet as ft
import sqlite3
from login import create_login_page
from register import create_register_page
from mainpage import create_main_page
from adminpage import create_admin_page

def main(page: ft.Page):
    page.title = "Login System"

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
        page.update()

    page.on_route_change = route_change
    page.go("/login")

# Initialize database and create admin user if not exists
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)''')
c.execute("SELECT * FROM users WHERE username=?", ("admin",))
if not c.fetchone():
    c.execute("INSERT INTO users VALUES (?, ?, ?)", ("admin", "ADMIN", 1))
    print("Admin user created. Username: admin, Password: ADMIN")
conn.commit()
conn.close()

ft.app(target=main)