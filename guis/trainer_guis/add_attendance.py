import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import json
import os
try:
    from guis.trainer_guis import tracking_attendance
except Exception:
    tracking_attendance = None

def load_all_members():
    if not os.path.exists("data/member_info.json"):
        return []
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def export_attendance_to_csv():
    members = load_all_members()
    rows = []
    for m in members:
        username = m.get("username", "")
        name = m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()
        for day in m.get("attendance_days", []):
            rows.append([username, name, day])
    if not rows:
        messagebox.showinfo("No Data", "No attendance data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Attendance Report")
    if not file_path:
        return
    import csv
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Name", "Attendance Day"])
        writer.writerows(rows)
    messagebox.showinfo("Success", f"Attendance report saved to {file_path}")

def on_add_attendance(root, trainer):
    root.title("Add Attendance Day & Export Report")
    text_label = tk.Label(root, text="Add Attendance Day & Export Report", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Only show members assigned to this trainer
    all_members = load_all_members()
    trainer_member_usernames = set(getattr(trainer, 'member_username', []))
    # If not set, try to get from trainer_info.json
    if not trainer_member_usernames:
        try:
            with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                trainers = json.load(f)
            for t in trainers:
                if t.get("username") == getattr(trainer, "username", None):
                    trainer_member_usernames = set(t.get("member_username", []))
                    break
        except Exception:
            pass
    # Accept trainer lists that contain either usernames or display/full names. Match by any of these.
    def member_matches_trainer_list(member, trainer_list):
        uname = (member.get("username") or "").strip()
        full_name = f"{member.get('f_name','')} {member.get('l_name','')}".strip()
        alt_name = (member.get("name") or "").strip()
        return (uname in trainer_list) or (full_name in trainer_list) or (alt_name in trainer_list)

    filtered_members = [m for m in all_members if member_matches_trainer_list(m, trainer_member_usernames)]
    member_options = []
    for m in filtered_members:
        uname = m.get("username", "")
        display = (m.get("name") or f"{m.get('f_name','')} {m.get('l_name','')}").strip()
        member_options.append((uname, display))

    member_usernames = [u for u, n in member_options]
    member_display = [f"{n} ({u})" for u, n in member_options]
    member_label = tk.Label(main_frame, text="Select Member:", font=("Arial", 12), bg=root["bg"])
    member_label.pack(pady=(0, 5))
    # Show readable display strings but extract username when needed
    member_var = tk.StringVar(value=member_display[0] if member_display else "")
    member_dropdown = ttk.Combobox(main_frame, textvariable=member_var, values=member_display, state="readonly", width=30)
    member_dropdown.pack(pady=(0, 15))

    # Date picker
    date_label = tk.Label(main_frame, text="Select Attendance Date:", font=("Arial", 12), bg=root["bg"])
    date_label.pack(pady=(0, 5))
    date_entry = DateEntry(main_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, firstweekday='sunday', showweeknumbers=False, selectmode='day')
    date_entry.pack(pady=(0, 15))

    def add_attendance():
        sel = member_var.get()
        # sel is like 'Display Name (username)'; extract username
        if sel.endswith(')') and '(' in sel:
            username = sel[sel.rfind('(')+1:-1]
        else:
            username = sel
        date_str = date_entry.get_date().strftime('%Y-%m-%d')
        if not username:
            messagebox.showerror("Error", "Please select a member.")
            return
        if trainer.add_attendance_day(username, date_str):
            messagebox.showinfo("Success", f"Added attendance for {username} on {date_str}")
            # notify tracking view to refresh if it's open
            try:
                if tracking_attendance and hasattr(tracking_attendance, 'refresh_tracking'):
                    tracking_attendance.refresh_tracking()
            except Exception:
                pass
        else:
            messagebox.showerror("Error", "Failed to add attendance day!")

    add_btn = tk.Button(main_frame, text="Add Attendance", command=add_attendance, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    add_btn.pack(pady=10)

    export_btn = tk.Button(main_frame, text="Export Attendance Report to CSV", command=export_attendance_to_csv, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=2)
    export_btn.pack(pady=10)

    def back_to_menu():
        root.destroy()
    back_btn = tk.Button(main_frame, text="Back to Menu", command=back_to_menu, font=("Arial", 14, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    back_btn.pack(pady=10)
