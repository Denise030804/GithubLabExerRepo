import flet as ft
import sqlite3

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
                        on_click=lambda _, u=user[0]: delete_user(u)
                    ),
                )
            )
        conn.close()
        page.update()

    def delete_user(username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        update_users_list()

    def create_user(e):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (new_username.value,))
        if c.fetchone():
            page.snack_bar = ft.SnackBar(ft.Text("Username already exists"))
            page.snack_bar.open = True
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (new_username.value, new_password.value, 0))
            conn.commit()
            new_username.value = ""
            new_password.value = ""
            update_users_list()
        conn.close()
        page.update()

    users_list = ft.ListView(expand=1, spacing=10, padding=20)
    new_username = ft.TextField(label="New Username")
    new_password = ft.TextField(label="New Password", password=True)

    update_users_list()

    return ft.View(
        "/admin",
        [
            ft.AppBar(title=ft.Text("Admin Panel"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text("Create New User:"),
            new_username,
            new_password,
            ft.ElevatedButton("Create User", on_click=create_user),
            ft.Text("Registered Users:"),
            users_list,
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
        ],
    )