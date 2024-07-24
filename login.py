import flet as ft
import sqlite3
import bcrypt

def create_login_page(page: ft.Page):
    def login(e):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username.value,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_password = user[1]
            if bcrypt.checkpw(password.value.encode('utf-8'), stored_password):
                if user[2]:  # is_admin
                    page.go("/admin")
                else:
                    page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials"))
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials"))
            page.snack_bar.open = True
            page.update()

    def toggle_password_visibility(_):
        password.password = not password.password
        show_password.icon = ft.icons.VISIBILITY if password.password else ft.icons.VISIBILITY_OFF
        page.update()

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    
    show_password = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        on_click=toggle_password_visibility
    )

    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
            username,
            ft.Row([
                ft.Container(password, expand=True),
                show_password
            ]),
            ft.ElevatedButton("Login", on_click=login),
            ft.ElevatedButton("Register", on_click=lambda _: page.go("/register")),
        ],
    )