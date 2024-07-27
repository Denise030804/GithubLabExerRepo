import flet as ft

def create_main_page(page: ft.Page):
    def logout(e):
        page.client_storage.clear()
        page.go("/login")
    
    def handle_close(e):
        dlg_modal.open = False
        page.update()

    def go_to_profile(e):
        page.go("/profile")
    
    def go_to_alarms(e):
        page.go("/alarms")
    
    def open_logout_dialog(e):
        dlg_modal.open = True
        page.update()
    
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to logout?"),
        actions=[
            ft.TextButton("Yes", on_click=logout),
            ft.TextButton("No", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,        
    )
           
    content = ft.Column(
        [
            ft.Container(
                content=ft.Image(
                    src="logo.jpg",
                    fit=ft.ImageFit.COVER,
                ),
                margin=0.01,
                padding=0,
                bgcolor=ft.colors.DEEP_PURPLE,
                height=170,
                width=page.window_width,
            ),
            ft.Container(
                content=ft.Text("Welcome to MemoryMentor", size=40, weight=ft.FontWeight.BOLD, color="white"),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.DEEP_PURPLE_200,
                expand=True,
                border_radius=10,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Empowering independence, a service learning app for Alzheimer's.", 
                                size=25, 
                                weight=ft.FontWeight.BOLD, 
                                color="white", 
                                width=800),
                        ft.Text("Welcome to MemoryMentor! We're here to empower individuals living with Alzheimer's disease and their caregivers. Our mission is to foster independence, enhance memory, and create meaningful connections. Alzheimer's disease is a progressive neurological disorder that leads to the degeneration and death of brain cells, resulting in a continuous decline in thinking, behavioral, and social skills.", 
                            text_align="justify",
                            width=800,
                            font_family="Arial",
                            size=15,
                            color="white"
                        ),                            
                    ],
                ),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.PURPLE,
                expand=True,
                border_radius=10,
            ),
            ft.Divider(height=1, color="white"),
            ft.Container(
                ft.Row(
                    controls=[
                        ft.ElevatedButton("My Profile", width=200, on_click=go_to_profile),
                        ft.Container(width=50),
                        ft.ElevatedButton("My Alarms", width=200, on_click=go_to_alarms),
                        ft.Container(width=50),
                        ft.ElevatedButton("Logout", width=200, on_click=open_logout_dialog),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,                       
                ),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.DEEP_PURPLE_200,
                expand=True,
                border_radius=10,
            ),
        ],
        spacing=0,
        expand=True,
    )

    page.dialog = dlg_modal
    return content