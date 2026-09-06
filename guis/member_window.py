import tkinter as tk
from utils.create_icon import c_icon
from utils.create_background import c_background
from guis.member_guis.check_info import show_member_info_window
from guis.member_guis.view_subscription import show_member_subscription_window
from guis.member_guis.renew_subscription import show_renew_subscription_window
import os
import json
from guis.member_guis.contact import show_contact_window

# Placeholder functions for each feature
# def on_view_profile(root, member):
#     root.title("View Profile")
#     tk.Label(root, text="View Profile (placeholder)", font=("Arial", 24)).pack(pady=50)

def on_view_subscription(root, member):
    # Use the new function to show subscription info
    username = member.username if hasattr(member, 'username') else member['username']
    show_member_subscription_window(username)

def on_check_workout_schedule(root, member):
    username = member.username if hasattr(member, 'username') else member['username']
    from guis.member_guis.check_workout import show_member_workout_window
    show_member_workout_window(username, window=root)

def create_track_progress_window(parent, member, current_sub_window=None):
    """Create and manage the track progress window"""
    if current_sub_window and current_sub_window.winfo_exists():
        current_sub_window.destroy()
    
    new_window = tk.Toplevel(parent)
    new_window.geometry(f"{parent.winfo_screenwidth()}x{parent.winfo_screenheight()}")
    c_icon(new_window)
    c_background(new_window)
    
    from guis.member_guis.track_progress import on_track_progress
    on_track_progress(new_window, member)
    
    return new_window

def on_track_progress(root, member, current_sub_window=None):
    """Function to handle track progress button click"""
    return create_track_progress_window(root, member, current_sub_window)

def on_renew_subscribe_plan(root, member):
    # Open the renew/subscribe GUI for this member
    username = member.username if hasattr(member, 'username') else member['username']
    show_renew_subscription_window(username, window=root)

def on_contact_trainers_admin(root, member):
    # Use member method to show contact info
    member.contact_trainers_admin()


def open_member_window(member):
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    c_icon(root)
    c_background(root)
    root.title("Gym Management System - Member")

    current_sub_window = None

    def close_sub_window():
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def open_view_profile():
        # Use show_member_info_window directly
        username = member.username if hasattr(member, 'username') else member['username']
        show_member_info_window(username)

    def open_view_subscription():
        # Use the new function to show subscription info
        username = member.username if hasattr(member, 'username') else member['username']
        show_member_subscription_window(username)

    def open_check_workout_schedule():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        on_check_workout_schedule(current_sub_window, member)

    def open_renew_subscribe_plan():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        c_icon(current_sub_window)
        c_background(current_sub_window)
        # Use the new renew subscription window
        on_renew_subscribe_plan(current_sub_window, member)

    def open_contact_trainers_admin():
        # Always use the member's username to show the contact window
        username = member.username if hasattr(member, 'username') else member['username']
        show_contact_window(username)

    # Top toolbar for member actions (responsive)
    toolbar = tk.Frame(root, bg="", pady=10)
    toolbar.pack(fill="x", padx=20, pady=20)

    btn_view_profile = tk.Button(toolbar, text="View Profile", command=open_view_profile, width=22)
    btn_view_profile.pack(side="left", padx=6)

    def open_track_progress():
        nonlocal current_sub_window
        close_sub_window()
        current_sub_window = on_track_progress(root, member, current_sub_window)
        
    btn_track_progress = tk.Button(toolbar, text="Track Progress", command=open_track_progress, width=22)
    btn_track_progress.pack(side="left", padx=6)

    btn_view_subscription = tk.Button(toolbar, text="View Subscription Plan", command=open_view_subscription, width=22)
    btn_view_subscription.pack(side="left", padx=6)

    btn_check_workout = tk.Button(toolbar, text="Check Workout Schedule", command=open_check_workout_schedule, width=22)
    btn_check_workout.pack(side="left", padx=6)

    btn_renew_subscribe = tk.Button(toolbar, text="Renew/Subscribe to New Plan", command=open_renew_subscribe_plan, width=26)
    btn_renew_subscribe.pack(side="left", padx=6)

    btn_contact = tk.Button(toolbar, text="Contact Trainers / Admin", command=open_contact_trainers_admin, width=24)
    btn_contact.pack(side="left", padx=6)

    btn_exit = tk.Button(toolbar, text="Exit", command=root.destroy, width=12)
    btn_exit.pack(side="right", padx=6)

    root.mainloop()
