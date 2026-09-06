import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

def load_all_members():
    if not os.path.exists("data/member_info.json"):
        return []
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def on_assigning_workout(root, trainer):
    root.title("Assign Workout")
    tk.Label(root, text="Assign Workout to Member", font=("Arial", 24), bg=root["bg"]).pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Only show members assigned to this trainer
    all_members = load_all_members()
    trainer_member_usernames = set(trainer.member_username if hasattr(trainer, 'member_username') else getattr(trainer, 'member_usernames', []))
    # If trainer.member_username is not set, try to get from trainer_info.json
    if not trainer_member_usernames:
        # Try to get from trainer_info.json by username
        try:
            with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                trainers = json.load(f)
            for t in trainers:
                if t.get("username") == getattr(trainer, "username", None):
                    trainer_member_usernames = set(t.get("member_username", []))
                    break
        except Exception:
            pass
    # Trainer file may store member identifiers as usernames or display names (full name or 'name').
    # Accept any of these forms to be resilient to inconsistent data.
    def member_matches_trainer_list(member, trainer_list):
        uname = (member.get("username") or "").strip()
        full_name = f"{member.get('f_name', '')} {member.get('l_name', '')}".strip()
        alt_name = (member.get("name") or "").strip()
        return (uname in trainer_list) or (full_name in trainer_list) or (alt_name in trainer_list)

    filtered_members = [m for m in all_members if member_matches_trainer_list(m, trainer_member_usernames)]
    # member_options: (username, display_name)
    member_options = []
    for m in filtered_members:
        display = (m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()).strip()
        member_options.append((m.get("username", ""), display))
    member_usernames = [u for u, n in member_options]
    member_label = tk.Label(main_frame, text="Select Member:", font=("Arial", 12), bg=root["bg"])
    member_label.pack(pady=(0, 5))
    member_var = tk.StringVar(value=member_usernames[0] if member_usernames else "")
    member_dropdown = ttk.Combobox(main_frame, textvariable=member_var, values=member_usernames, state="readonly", width=30)
    member_dropdown.pack(pady=(0, 15))

    date_label = tk.Label(main_frame, text="Select Workout Date:", font=("Arial", 12), bg=root["bg"])
    date_label.pack(pady=(0, 5))
    date_entry = DateEntry(main_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, firstweekday='sunday', showweeknumbers=False, selectmode='day')
    date_entry.pack(pady=(0, 15))

    workout_label = tk.Label(main_frame, text="Workout Description:", font=("Arial", 12), bg=root["bg"])
    workout_label.pack(pady=(0, 5))
    workout_entry = tk.Entry(main_frame, font=("Arial", 12), width=50)
    workout_entry.pack(pady=(0, 15))

    def assign_workout():
        username = member_var.get()
        date_str = date_entry.get_date().strftime('%Y-%m-%d')
        workout = workout_entry.get().strip()
        if not username or not workout:
            messagebox.showerror("Error", "Please select a member and enter a workout description.")
            return
        if trainer.assign_workout(username, date_str, workout):
            messagebox.showinfo("Success", f"Assigned workout for {username} on {date_str}")
        else:
            messagebox.showerror("Error", "Failed to assign workout.")

    assign_btn = tk.Button(main_frame, text="Assign Workout", command=assign_workout, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
    assign_btn.pack(pady=10)

    def back_to_menu():
        root.destroy()
    back_btn = tk.Button(main_frame, text="Back to Menu", command=back_to_menu, font=("Arial", 14, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    back_btn.pack(pady=10)
