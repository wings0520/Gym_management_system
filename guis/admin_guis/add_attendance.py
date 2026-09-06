import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import json
import os
import csv
try:
    from guis.trainer_guis import tracking_attendance
except Exception:
    tracking_attendance = None

def load_all_members():
    if not os.path.exists("data/member_info.json"):
        return []
    try:
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

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
        
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv")], 
                                             title="Save Attendance Report")
    if not file_path:
        return
        
    try:
        with open(file_path, "w", newline='', encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Username", "Name", "Attendance Day"])
            writer.writerows(rows)
        messagebox.showinfo("Success", f"Attendance report saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")


def on_add_attendance(root, admin):
    root.title("Add Attendance Day & Export Report")
    text_label = ttk.Label(root, text="Add Attendance Day & Export Report", font=("Arial", 24))
    text_label.pack(pady=20)

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Member selection
    members = load_all_members()
    member_options = [(m.get("username", ""), m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()) for m in members]
    member_usernames = [u for u, n in member_options]
    member_display = [f"{n} ({u})" for u, n in member_options] # Hiển thị cả tên và username
    
    member_label = ttk.Label(main_frame, text="Select Member:", font=("Arial", 12))
    member_label.pack(pady=(10, 5))
    
    member_var = tk.StringVar(value=member_display[0] if member_display else "")
    member_dropdown = ttk.Combobox(main_frame, textvariable=member_var, values=member_display, 
                                 state="readonly", width=40, font=("Arial", 11))
    member_dropdown.pack(pady=(0, 15))

    # Date picker
    date_label = ttk.Label(main_frame, text="Select Attendance Date:", font=("Arial", 12))
    date_label.pack(pady=(10, 5))
    date_entry = DateEntry(main_frame, width=38, background='darkblue', foreground='white', 
                           borderwidth=2, date_pattern='yyyy-mm-dd', year=datetime.now().year, 
                           month=datetime.now().month, day=datetime.now().day)
    date_entry.pack(pady=(0, 20))

    def add_attendance():
        # Lấy username từ chuỗi hiển thị
        selected_display = member_var.get()
        if not selected_display:
            messagebox.showerror("Error", "Please select a member.")
            return
            
        try:
            # Lấy username từ "Name (username)"
            username = selected_display.split('(')[-1].replace(')', '').strip()
        except Exception:
            messagebox.showerror("Error", "Invalid member selection.")
            return

        date_str = date_entry.get_date().strftime('%Y-%m-%d')
        
        if admin.add_attendance_day(username, date_str):
            messagebox.showinfo("Success", f"Added attendance for {username} on {date_str}")
            try:
                if tracking_attendance and hasattr(tracking_attendance, 'refresh_tracking'):
                    tracking_attendance.refresh_tracking()
            except Exception:
                pass
        else:
            messagebox.showerror("Error", "Failed to add attendance day!")

    # Khung nút
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    add_btn = ttk.Button(button_frame, text="Add Attendance", command=add_attendance, style="Primary.TButton")
    add_btn.pack(side="left", padx=10, ipady=5)

    export_btn = ttk.Button(button_frame, text="Export Attendance Report (CSV)", command=export_attendance_to_csv, style="Success.TButton")
    export_btn.pack(side="left", padx=10, ipady=5)

    back_btn = ttk.Button(main_frame, text="Back to Menu", command=root.destroy, style="Warning.TButton")
    back_btn.pack(side="bottom", pady=10)