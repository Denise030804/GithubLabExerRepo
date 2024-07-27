import flet as ft
import sqlite3
import random
import threading
import time as time_lib
from datetime import datetime, timedelta
from playsound import playsound
from threading import Thread

def initialize_database():
    conn = sqlite3.connect('alarms.db')
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alarms'")
    if not c.fetchone():
        c.execute('''
            CREATE TABLE alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                time TEXT NOT NULL,
                medication TEXT NOT NULL
            )
        ''')

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timers'")
    if not c.fetchone():
        c.execute('''
            CREATE TABLE timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                duration_seconds INTEGER NOT NULL,
                medication TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        c.execute("PRAGMA table_info(timers)")
        columns = [row[1] for row in c.fetchall()]
        if 'start_time' not in columns:
            c.execute("ALTER TABLE timers ADD COLUMN start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")

    conn.commit()
    conn.close()

initialize_database()

def parse_time(time_str):
    time_str = time_str.strip().lower()
    try:
        if 'am' in time_str or 'pm' in time_str:
            return datetime.strptime(time_str, '%I:%M%p').strftime('%H:%M')
        if len(time_str) == 4 and time_str.isdigit():
            return datetime.strptime(time_str, '%H%M').strftime('%H:%M')
        if len(time_str) == 5 and time_str[2] == ':':
            return datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
        if len(time_str) > 4:
            return datetime.strptime(time_str, '%H%M').strftime('%H:%M')
    except ValueError:
        return None
    return None

def play_alarm():
    print("Playing alarm sound")
    try:
        playsound('alarm.mp3', block=False)
    except Exception as e:
        print(f"Error playing sound: {e}")

def create_alarm_page(page, username):
    time_input = ft.TextField(label="Alarm Time (e.g., 1230, 12:30 PM, 1300)")
    medication = ft.TextField(label="Medication")
    seconds_input = ft.TextField(label="Timer (Seconds)")
    minutes_input = ft.TextField(label="Timer (Minutes)")
    hours_input = ft.TextField(label="Timer (Hours)")
    days_input = ft.TextField(label="Timer (Days)")
    medication_input = ft.TextField(label="Medication")

    new_time_input = ft.TextField(label="Alarm Time (e.g., 1230, 12:30 PM, 1300)")
    new_medication = ft.TextField(label="Medication")

    alarms_view = ft.Column()
    timers_view = ft.Column()

    def add_alarm(e):
        time_str = time_input.value
        formatted_time = parse_time(time_str)
        if not formatted_time:
            show_alert("Input Error", "Please provide a valid time format.")
            return

        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM alarms WHERE username=?", (username,))
        alarm_count = c.fetchone()[0]
        if alarm_count >= 8:
            show_alert("Limit Reached", "You cannot add more than 8 alarms. Please delete an existing alarm.")
            return

        c.execute("INSERT INTO alarms (username, time, medication) VALUES (?, ?, ?)",
                  (username, formatted_time, medication.value))
        conn.commit()
        conn.close()
        refresh_alarms()

    def delete_alarm(e, alarm_id):
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("DELETE FROM alarms WHERE id=?", (alarm_id,))
        conn.commit()
        conn.close()
        refresh_alarms()

    def update_alarm(e, alarm_id):
        try:
            time_str = new_time_input.value
            formatted_time = parse_time(time_str)
            if not formatted_time or not new_medication.value:
                show_alert("Update Error", "Please provide valid time and medication.")
                return

            conn = sqlite3.connect('alarms.db')
            c = conn.cursor()
            c.execute("UPDATE alarms SET time=?, medication=? WHERE id=?", 
                      (formatted_time, new_medication.value, alarm_id))
            conn.commit()
            conn.close()

            show_alert("Alarm Updated", "Your changes have been saved.")
            
        except Exception as ex:
            show_alert("Update Error", "Error updating alarm.")

    def check_alarms():
        while True:
            conn = sqlite3.connect('alarms.db')
            c = conn.cursor()
            c.execute("SELECT * FROM alarms WHERE username=?", (username,))
            alarms = c.fetchall()
            conn.close()
            
            current_time = datetime.now().strftime("%H:%M")
            prompts = [
                "Time to take your medication!",
                "Don't forget your meds!",
                "It's medication time!",
                "Please take your prescribed medication."
            ]
            
            for alarm in alarms:
                _, _, alarm_time, alarm_medication = alarm
                if alarm_time == current_time:
                    snack_bar = ft.SnackBar(content=ft.Text(f"{random.choice(prompts)} Medication: {alarm_medication}"))
                    page.snack_bar = snack_bar
                    page.snack_bar.open = True
                    page.update()
                    Thread(target=play_alarm).start()
                    time_lib.sleep(60)  

            time_lib.sleep(30)

    def start_alarm_check():
        alarm_thread = threading.Thread(target=check_alarms, daemon=True)
        alarm_thread.start()

    def refresh_alarms():
        alarms_view.controls.clear()
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("SELECT * FROM alarms WHERE username=?", (username,))
        alarms = c.fetchall()
        conn.close()
        
        for alarm in alarms:
            alarm_id, _, alarm_time, alarm_medication = alarm
            alarms_view.controls.append(ft.Row([
                ft.Text(f"Time: {alarm_time}, Medication: {alarm_medication}"),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, aid=alarm_id: delete_alarm(e, aid)),
                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, aid=alarm_id: navigate_to_edit_alarm(aid))
            ]))
        page.update()

    def navigate_to_edit_alarm(alarm_id):
        def back_to_alarms(e):
            page.views.pop()
            refresh_alarms()

        def save_changes(e):
            update_alarm(e, alarm_id)

        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("SELECT time, medication FROM alarms WHERE id=?", (alarm_id,))
        alarm = c.fetchone()
        conn.close()
        
        if alarm:
            initial_time, initial_medication = alarm
            new_time_input.value = initial_time
            new_medication.value = initial_medication

        edit_page = ft.Column([
            ft.Text("Edit Alarm"),
            new_time_input,
            new_medication,
            ft.Row([
                ft.ElevatedButton(text="Save Changes", on_click=save_changes),
                ft.ElevatedButton(text="Back", on_click=back_to_alarms)
            ])
        ])
        
        page.views.append(edit_page)
        page.update()

    def add_timer(e):
        try:
            seconds = int(seconds_input.value) if seconds_input.value else 0
            minutes = int(minutes_input.value) if minutes_input.value else 0
            hours = int(hours_input.value) if hours_input.value else 0
            days = int(days_input.value) if days_input.value else 0

            total_seconds = seconds + minutes * 60 + hours * 3600 + days * 86400

            if total_seconds <= 0:
                show_alert("Input Error", "Please provide a valid duration.")
                return

            start_time = datetime.now()

            conn = sqlite3.connect('alarms.db')
            c = conn.cursor()
            c.execute("INSERT INTO timers (username, duration_seconds, medication, start_time) VALUES (?, ?, ?, ?)",
                      (username, total_seconds, medication_input.value, start_time))
            conn.commit()
            conn.close()
            refresh_timers()
        
        except ValueError:
            show_alert("Input Error", "Please provide valid numeric values for the timer.")

    def delete_timer(e, timer_id):
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("DELETE FROM timers WHERE id=?", (timer_id,))
        conn.commit()
        conn.close()
        refresh_timers()

    def check_timers():
        while True:
            conn = sqlite3.connect('alarms.db')
            c = conn.cursor()
            c.execute("SELECT * FROM timers WHERE username=?", (username,))
            timers = c.fetchall()
            conn.close()
            
            current_time = datetime.now()
            
            for timer in timers:
                timer_id, _, duration_seconds, medication, start_time = timer
                start_time = datetime.fromisoformat(start_time)
                expiration_time = start_time + timedelta(seconds=duration_seconds)

                if current_time >= expiration_time:
                    snack_bar = ft.SnackBar(
                        content=ft.Text(f"Timer expired! Medication: {medication}"),
                        action="Alright!"
                    )
                    page.snack_bar = snack_bar
                    page.snack_bar.open = True
                    page.update()
                    Thread(target=play_alarm).start()
                    
                    delete_timer(None, timer_id)  

            time_lib.sleep(2)  

    def start_timer_check():
        timer_thread = threading.Thread(target=check_timers, daemon=True)
        timer_thread.start()

    def refresh_timers():
        timers_view.controls.clear()
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute("SELECT * FROM timers WHERE username=?", (username,))
        timers = c.fetchall()
        conn.close()
        
        for timer in timers:
            timer_id, _, duration_seconds, medication, start_time = timer
            expiration_time = datetime.fromisoformat(start_time) + timedelta(seconds=duration_seconds)
            timers_view.controls.append(ft.Row([
                ft.Text(f"Duration: {duration_seconds} seconds, Expiration: {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}, Medication: {medication}"),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, tid=timer_id: delete_timer(e, tid))
            ]))
        page.update()

    def show_alert(title, content):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.ElevatedButton(text="OK", on_click=lambda e: handle_dialog_close())
            ]
        )
        page.dialog = dialog
        page.update()

    def handle_dialog_close():
        if page.dialog:
            page.dialog = None
        page.update()

    start_alarm_check()
    start_timer_check()
    refresh_alarms()
    refresh_timers()

    return ft.Column([
        ft.Text("Manage Alarms"),
        time_input,
        medication,
        ft.ElevatedButton(text="Add Alarm", on_click=add_alarm),
        alarms_view,
        ft.Text("Manage Timers"),
        seconds_input,
        minutes_input,
        hours_input,
        days_input,
        medication_input,
        ft.ElevatedButton(text="Add Timer", on_click=add_timer),
        timers_view,
        ft.ElevatedButton(text="Back to Main Page", on_click=lambda e: page.go("/main"))
    ])