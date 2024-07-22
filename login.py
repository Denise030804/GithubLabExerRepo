import flet as ft
import sqlite3

def create_login_page(page: ft.Page):
    def login(e):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username.value, password.value))
        user = c.fetchone()
        conn.close()

        if user:
            if user[2]:  # is_admin
                page.go("/admin")
            else:
                page.go("/main")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials"))
            page.snack_bar.open = True
            page.update()

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)

    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
            username,
            password,
            ft.ElevatedButton("Login", on_click=login),
            ft.ElevatedButton("Register", on_click=lambda _: page.go("/register")),
        ],
    )