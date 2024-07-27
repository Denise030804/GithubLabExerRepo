import flet as ft
import sqlite3
import bcrypt

def create_register_page(page: ft.Page):
    def register(e):
        if not all([username.value, full_name.value, age.value, location.value, password.value, confirm_password.value]):
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
            if age_value <= 0:
                raise ValueError("Age must be a positive number")
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
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
            hashed_password = bcrypt.hashpw(password.value.encode('utf-8'), bcrypt.gensalt())
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                (username.value, hashed_password, 0, full_name.value, age_value, location.value))
            conn.commit()
            page.snack_bar = ft.SnackBar(ft.Text("Account has been registered"))
            page.snack_bar.open = True
            page.update()
            
            page.client_storage.set("username", username.value)
            page.go("/main")
        
        conn.close()

    def toggle_password_visibility(password_field, icon_button):
        password_field.password = not password_field.password
        icon_button.icon = ft.icons.VISIBILITY if password_field.password else ft.icons.VISIBILITY_OFF
        page.update()

    username = ft.TextField(label="Username")
    full_name = ft.TextField(label="Full Name")
    age = ft.TextField(label="Age")
    location = ft.TextField(label="Address")
    password = ft.TextField(label="Password", password=True)
    confirm_password = ft.TextField(label="Confirm Password", password=True)

    show_password = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        on_click=lambda _: toggle_password_visibility(password, show_password)
    )
    show_confirm_password = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        on_click=lambda _: toggle_password_visibility(confirm_password, show_confirm_password)
    )

    return ft.View(
        "/register",
        [
            ft.AppBar(title=ft.Text("Register"), bgcolor=ft.colors.SURFACE_VARIANT),
            username,
            full_name,
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
            ft.Row([
                ft.ElevatedButton("Register", on_click=register),
                ft.ElevatedButton("Back to Login", on_click=lambda _: page.go("/login")),
            ]),
        ],
    )