import flet as ft

def create_main_page(page: ft.Page):
    return ft.View(
        "/main",
        [
            ft.AppBar(title=ft.Text("Main Page"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Text("Hello", size=32),
                alignment=ft.alignment.center,
                expand=True
            ),
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
        ],
    )