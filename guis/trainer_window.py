import tkinter as tk
from tkinter import messagebox
from utils.create_icon import c_icon #add the function to create the icon
from utils.create_background import c_background #add the function to create the background
from guis.trainer_guis.assigning_workout import on_assigning_workout
from guis.trainer_guis.add_attendance import on_add_attendance
try:
    from guis.trainer_guis import tracking_attendance
except Exception:
    tracking_attendance = None
import json
import os
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import ttk

# Placeholder functions for each feature
def on_assign_workout(root, trainer):
    on_assigning_workout(root, trainer)

def on_attendance_tracking(root, trainer):
    # Use the tracking_attendance UI which supports filtering by trainer
    if tracking_attendance and hasattr(tracking_attendance, 'on_add_attendance'):
        try:
            tracking_attendance.on_add_attendance(root, trainer, getattr(trainer, 'username', trainer))
            return
        except Exception:
            pass
    # Fallback
    root.title("Attendance Tracking")
    tk.Label(root, text="Attendance Tracking (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_adding_attendance(root, trainer):
    on_add_attendance(root, trainer)

def on_view_member_info(root, trainer):
    from guis.trainer_guis.view_member_info import on_view_member_info as view_member_info
    view_member_info(root, trainer)

def on_progress_tracking(root, trainer):
    from guis.trainer_guis.track_member_progress import on_track_member_progress
    on_track_member_progress(root, trainer)

def open_trainer_window(trainer):
    root = tk.Tk() #Create the main window
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root) #set the background of the window
    root.title("Gym Management System - Trainer") #set the title of the window

    # Track the current sub-window
    current_sub_window = None

    def close_sub_window():
        """Close the current sub-window if it exists"""
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def open_assign_workout():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_assign_workout(current_sub_window, trainer)

    def open_attendance_tracking():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_attendance_tracking(current_sub_window, trainer)

    def open_add_attendance():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_adding_attendance(current_sub_window, trainer)

    def open_view_member_info():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_view_member_info(current_sub_window, trainer)

    def open_progress_tracking():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_progress_tracking(current_sub_window, trainer)

    # Top toolbar for trainer actions
    toolbar = tk.Frame(root, bg="", pady=10)
    toolbar.pack(fill="x", padx=20, pady=20)

    btn_assign_workout = tk.Button(toolbar, text="Assign Workout", command=open_assign_workout, width=18)
    btn_assign_workout.pack(side="left", padx=6)

    btn_attendance_tracking = tk.Button(toolbar, text="Attendance Tracking", command=open_attendance_tracking, width=18)
    btn_attendance_tracking.pack(side="left", padx=6)

    btn_add_attendance = tk.Button(toolbar, text="Add Attendance", command=open_add_attendance, width=18)
    btn_add_attendance.pack(side="left", padx=6)

    btn_view_member_info = tk.Button(toolbar, text="View Member Info", command=open_view_member_info, width=18)
    btn_view_member_info.pack(side="left", padx=6)

    btn_progress_tracking = tk.Button(toolbar, text="Progress Tracking", command=open_progress_tracking, width=18)
    btn_progress_tracking.pack(side="left", padx=6)

    btn_exit = tk.Button(toolbar, text="Exit", command=root.destroy, width=12)
    btn_exit.pack(side="right", padx=6)
    
    root.mainloop()
