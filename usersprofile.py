import flet as ft
import sqlite3

def create_user_profile_page(page: ft.Page, username):
    def load_user_data():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        return user

    def save_changes(e):
        if not all([full_name.value, age.value, location.value]):
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required"))
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
        c.execute("UPDATE users SET full_name=?, age=?, location=? WHERE username=?",
                  (full_name.value, age_value, location.value, username))
        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(ft.Text("Profile updated successfully"))
        page.snack_bar.open = True
        page.update()

    user_data = load_user_data()
    
    full_name = ft.TextField(label="Full Name", value=user_data[3])
    age = ft.TextField(label="Age", value=str(user_data[4]))
    location = ft.TextField(label="Address", value=user_data[5])

    return ft.View(
        "/profile",
        [
            ft.AppBar(title=ft.Text(f"Profile: {username}"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text("Edit Your Profile", size=20, weight=ft.FontWeight.BOLD),
            full_name,
            age,
            location,
            ft.ElevatedButton("Save Changes", on_click=save_changes),
            ft.ElevatedButton("Back to Main", on_click=lambda _: page.go("/main")),
        ],
    )