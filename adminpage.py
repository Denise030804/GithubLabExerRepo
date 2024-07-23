import flet as ft
import sqlite3
import bcrypt

def create_admin_page(page: ft.Page):
    def update_users_list():
        users_list.controls.clear()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE is_admin=0")
        for user in c.fetchall():
            users_list.controls.append(
                ft.ListTile(
                    title=ft.Text(user[0]),
                    trailing=ft.IconButton(
                        ft.icons.DELETE,
                        on_click=create_delete_handler(user[0])
                    ),
                )
            )
        conn.close()
        page.update()

    def create_delete_handler(username):
        return lambda _: delete_user(username)

    def delete_user(username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        update_users_list()

    def create_user(e):
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
            username.value = ""
            full_name.value = ""
            age.value = ""
            location.value = ""
            password.value = ""
            confirm_password.value = ""
            update_users_list()
        
        conn.close()
        page.update()
    
    def toggle_password_visibility(password_field):
        password_field.password = not password_field.password
        password_field.update()
    
    users_list = ft.ListView(expand=1, spacing=10, padding=20)
    username = ft.TextField(label="Username")
    full_name = ft.TextField(label="Full Name")
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

    update_users_list()

    return ft.View(
        "/admin",
        [
            ft.AppBar(title=ft.Text("Admin Panel"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text("Create New User:", size=20, weight=ft.FontWeight.BOLD),
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
            ft.ElevatedButton("Create User", on_click=create_user),
            ft.Divider(),
            ft.Text("Registered Users:", size=20, weight=ft.FontWeight.BOLD),
            users_list,
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
        ],
    )