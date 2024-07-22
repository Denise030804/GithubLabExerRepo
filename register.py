import flet as ft
import sqlite3

def create_register_page(page: ft.Page):
    def toggle_password_visibility(password_field):
        password_field.password = not password_field.password
        password_field.update()

    def register(e):
        if not all([name.value, age.value, location.value, username.value, password.value, confirm_password.value]):
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required"))
            page.snack_bar.open = True
            page.update()
            return

        if password.value != confirm_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            age_value = int(age.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Age must be a number"))
            page.snack_bar.open = True
            page.update()
            return

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username.value,))
        if c.fetchone():
            page.snack_bar = ft.SnackBar(ft.Text("Username already exists"))
            page.snack_bar.open = True
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                      (username.value, password.value, 0, name.value, age_value, location.value))
            conn.commit()
            page.go("/main")
        conn.close()
        page.update()

    username = ft.TextField(label="Username")
    name = ft.TextField(label="Full Name")
    age = ft.TextField(label="Age")
    location = ft.TextField(label="Location")
    password = ft.TextField(label="Password", password=True)
    confirm_password = ft.TextField(label="Confirm Password", password=True)

    show_password = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        on_click=lambda _: toggle_password_visibility(password)
    )
    show_confirm_password = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        on_click=lambda _: toggle_password_visibility(confirm_password)
    )

    return ft.View(
        "/register",
        [
            ft.AppBar(title=ft.Text("Register"), bgcolor=ft.colors.SURFACE_VARIANT),
            username,
            name,
            age,
            location,
            
            ft.Row([
                ft.Container(password, expand=True),
                show_password
            ]),
            ft.Row([
                ft.Container(confirm_password, expand=True),
                show_confirm_password
            ]),
            ft.ElevatedButton("Register", on_click=register, ),
            ft.ElevatedButton("Back to Login", on_click=lambda _: page.go("/login")),
        ],
    )